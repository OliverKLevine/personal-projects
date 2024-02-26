import sys
import json
from datetime import date
from urllib.request import Request, urlopen
from olivers_utils import download_spreadsheet, upload_spreadsheet
import numpy as np
from scipy import stats

def attempt(function, argument):
    try:
        return function(argument)
    except:
        return None
    
def valid_format(format, value):
    try:
        format(value)
        return True
    except: return False

def double(value):
    return float(value.replace(",",""))
def sq_ft(value):
    if value == "duplex": return 2000
    else:
        try: return double(value)
        except: return 1000
def int0(value):
    try: return int(value)
    except: return 0


class house:
    def __init__(self,table_line, header):
        self.header = header
        self.__dict__.update({header[i]:table_line[i] for i in range(len(header))})
        self.update_spreadsheet = False
        self.find_webtype()
        for method in self.finder_methods: self.find_property(method)

    def get_line(self):
        return [self.__dict__[i] for i in self.header]
    
    def find_webtype(self):
        self.web_type = [i for i in ["zillow"] if i in self.link][0]
        self.web_text = None

        if self.web_type == "zillow":
            def get_web_data(self):
                if not self.web_text:
                    print("Requesting data from zillow",file=sys.stderr)
                    r = Request(self.link,headers={"User-Agent":"Mozilla/6.0"})
                    self.web_text = urlopen(r).read().decode("utf-8")
                    self.page_accessed = str(date.today())
                zillow_data = json.loads(self.web_text.split("<input id='hidden-reg-details'")[1].split('type="application/json">')[1].split("}<")[0] + "}")
                zillow_data = json.loads(zillow_data["props"]["pageProps"]["componentProps"]["gdpClientCache"])
                self.zillow_data = zillow_data[list(zillow_data.keys())[0]]["property"]
                self.glance_facts = {item["factLabel"]:item["factValue"] for item in self.zillow_data["resoFacts"]["atAGlanceFacts"]}
            self.get_web_text = get_web_data
            self.finder_methods = {
                "address":lambda x: self.zillow_data["streetAddress"],
                "price":lambda x: self.zillow_data["price"],
                "sq_footage":lambda x: int(self.zillow_data["resoFacts"]["buildingArea"].replace(",","")),
                "bedrooms/equivalent":lambda x: self.zillow_data["resoFacts"]["bedrooms"],
                "bathrooms":lambda x: self.zillow_data["resoFacts"]["bathrooms"],
                "age": lambda x: 2024 -  self.zillow_data["resoFacts"]["yearBuilt"],
                "days_on_market": lambda x: self.zillow_data["daysOnZillow"],
                "neighborhood": lambda x: self.zillow_data["parentRegion"]["name"]
            }
    
    def find_property(self,property):
        if self.__dict__[property]: return
        if not self.web_text: self.get_web_text(self)
        self.__dict__[property] = attempt(self.finder_methods[property],self.web_text)
        self.update_spreadsheet = True
    
    def percentile(self, characteristic, format = double, negative=False):
        array = [format(house.__dict__[characteristic]) for house in self.other_houses if valid_format(double,house.__dict__[characteristic])]
        try:
            p = stats.percentileofscore(
                array,
                format(self.__dict__[characteristic]),
                kind="weak"
            )
        except:
            #print(self.address)
            #print(array)
            return None
        if negative: return 100 - p
        else: return p
    
    def calculate_score(self, all_houses):
        self.other_houses = all_houses#[house for house in all_houses if not self == house]
        old_score = self.score
        scores = {
            "price":self.percentile("price",negative=True),
            "sq_footage":self.percentile("sq_footage",sq_ft)*(1+(int(self.basement)+1)/22),
            "bedrooms":100,
            "bathrooms":100,
            "neighborhood":(self.percentile("zillow_walkability_score")+self.percentile("proximity_to_game_store",negative=True))/2,
            "inside":self.percentile("cuteness_of_inside"),
            "kitchen":self.percentile("kitchen"),
            "outside":self.percentile("cuteness_of_outside"),
        }
        penalties_and_bonuses = {
            "dax_penalty":-1*(10-int(self.__dict__["backyard/dax_score"])),
            "readiness_penalty":-1*(100/self.percentile("readiness")*int(self.age)/100),
            "ev_penalty":-1*((10-double(self.__dict__["ev-ability"]))*(100 - scores["neighborhood"]))/1000,
            "bonuses":int0(self.investment) + int0(self.other)

        }
        if int(self.__dict__["bedrooms/equivalent"]) < 3:
            scores["bedrooms"] = 75
        if int(self.bathrooms) < 2:
            scores["bathrooms"] = 50
        
        weights = {
            "price": 5,
            "sq_footage":10,
            "bedrooms":3,
            "bathrooms":4,
            "neighborhood":10,
            "inside":10,
            "outside":2,
            "kitchen":4
        }

        try: self.score = sum([scores[category]*weights[category] for category in scores])/sum([weights[category] for category in weights]) + sum([penalties_and_bonuses[i] for i in penalties_and_bonuses])
        except:
            self.score = None
            print(scores)

        print(self.address)
        print(self.score)       


        if not self.score == old_score:
            self.update_spreadsheet = True
        


def main():
    pgh_sheet_id = "1ehPYGR5tt4KAE6N2fFQ1NjU0R4fM7aG9vt8S5bYowaQ"
    table = download_spreadsheet(pgh_sheet_id)
    table_header = table[0]
    header = [i.lower().replace(" ","_") for i in table_header]
    table = table[1:]
    houses = [house(line,header) for line in table]
    [house.calculate_score(houses) for house in houses]
    update_sheet = any([house.update_spreadsheet for house in houses])
    if update_sheet:
        table = [table_header] + [house.get_line() for house in houses]
        upload_spreadsheet(pgh_sheet_id, table)

if __name__ == "__main__":
    main()