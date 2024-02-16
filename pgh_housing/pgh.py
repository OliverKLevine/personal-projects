import sys
import json
from datetime import date
from urllib.request import Request, urlopen
from olivers_utils import download_spreadsheet, upload_spreadsheet

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
        self.__dict__[property] = self.finder_methods[property](self.web_text)
        self.update_spreadsheet = True

def main():
    pgh_sheet_id = "1ehPYGR5tt4KAE6N2fFQ1NjU0R4fM7aG9vt8S5bYowaQ"
    table = download_spreadsheet(pgh_sheet_id)
    table_header = table[0]
    header = [i.lower().replace(" ","_") for i in table_header]
    table = table[1:]
    houses = [house(line,header) for line in table]
    update_sheet = any([house.update_spreadsheet for house in houses])
    if update_sheet:
        table = [table_header] + [house.get_line() for house in houses]
        upload_spreadsheet(pgh_sheet_id, table)

if __name__ == "__main__":
    main()