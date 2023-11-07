import os
import sys
import json
from olivers_utils import relaxed_bool, getdict, setdict

class Survey:
    def __init__(self, qsf, input_questions, keep_questions = False):
        with open(qsf, "r") as input:
            self.qsf = json.load(input)
        for item in self.qsf["SurveyEntry"]:
            name = item.replace("Survey","")
            self.__dict__[name] = self.qsf["SurveyEntry"][item]
        self.elements = getdict(self.qsf,["SurveyElements"])
        self.blocks = self.Blocks(self)
        self.flow = self.Flow(self)
        self.count = self.Question_Count(self)
        if not keep_questions:
            self.blocks.empty()
            self.count.empty()
            self.flow.empty()
            self.questions = []
        else: self.questions = [element for element in self.elements if element["Element"] == "SQ"]
        setdict(self.qsf,["SurveyElements"],[element for element in self.elements if element["Element"] != "SQ"])
        self.elements = getdict(self.qsf,["SurveyElements"])

        with open(input_questions,"r") as input:
            text = input.read()

        text = text.split("[[Block:")[1:]
        for block in text:
            self.blocks.add_block(block)

        self.blocks.extract()
        self.count.extract()
        self.flow.extract()
        for x in range(len(self.questions)):
            if isinstance(self.questions[x],self.Question):
                self.questions[x] = self.questions[x].extract()

    class Blocks:
        def __init__(self, survey):
            self.survey = survey
            abbrev = "BL"
            self.index = self.survey.elements.index([element for element in self.survey.elements if element["Element"] == abbrev][0])
            self.__dict__.update(self.survey.elements[self.index])
        
        def empty(self):
            trash = [block for block in self.Payload if block["Type"] == "Trash"]
            self.Payload = {}
            if len(trash) > 0:
                self.Payload["0"] = trash[0]

        def add_block(self, block_text):
            name = block_text.split("]]")[0].strip()
            info = [self.Payload[blindex] for blindex in self.Payload if self.Payload[blindex]["Description"] == name]
            if len(info) > 0: info = info[0]
            else: info = {
                "Description":name,
                "Type":"Standard",
                "BlockElements":[]
            }
            description = block_text.split("]]")[1].split("[[")[0].strip()
            if description: pass#add description later
            strindex = str(len(self.Payload))
            if not "ID" in info:
                info["ID"] = f'BL_{"".join(["0" for x in range(15-len(strindex))])}{len(self.Payload)}'

            try: 
                block_text = block_text.split("[[Question:")[1:]
            except:
                info.pop("BlockElements")
                self.Payload.insert(-1,info)
                return

            for question in block_text:
                question = self.survey.Question(self.survey,info,question)
                info["BlockElements"].append(question.block_info)

            self.Payload[strindex] = info
            self.survey.flow.add_block(info)
            

        def extract(self):
            index = self.__dict__.pop("index")
            self.__dict__.pop("survey").elements[index] = self.__dict__

    class Flow:
        def __init__(self, survey):
            self.survey = survey
            abbrev = "FL"
            self.index = self.survey.elements.index([element for element in self.survey.elements if element["Element"] == abbrev][0])
            self.__dict__.update(self.survey.elements[self.index])
        
        def empty(self):
            self.Payload["Flow"] = []
            self.Payload["Properties"]["Count"] = 1

        def add_block(self, block):
            self.Payload["Flow"].append({
                "ID": block["ID"],
                "Type": "Block",
                "FlowID": f"FL_{int(block['ID'].split('_')[-1])+1}"
            })
            self.Payload["Properties"]["Count"] += 1
            

        def extract(self):
            index = self.__dict__.pop("index")
            self.__dict__.pop("survey").elements[index] = self.__dict__

    class Question_Count:
        def __init__(self, survey):
            self.survey = survey
            abbrev = "QC"
            self.index = self.survey.elements.index([element for element in self.survey.elements if element["Element"] == abbrev][0])
            self.__dict__.update(self.survey.elements[self.index])
        
        def empty(self):
            self.SecondaryAttribute = 0

        def plus(self):
            self.SecondaryAttribute += 1
            return self.SecondaryAttribute

        def extract(self):
            index = self.__dict__.pop("index")
            self.SecondaryAttribute = str(self.SecondaryAttribute)
            self.__dict__.pop("survey").elements[index] = self.__dict__

    class Question:
        def __init__(self, survey,block_info,question_text):
            self.survey = survey
            question_types = question_text.split("]]")[0].split(":")
            qtype = {"MC":"MC","TE":"TE","CS":"CS","ConstantSum":"CS","Slider":"Slider","Text":"DB","Matrix":"Matrix"}[question_types[0]]

            self.count = survey.count.plus()
            self.name = question_text.split("\n")[1].strip()
            selectors = {
                "MC": {True:"MAVR",False:"SAVR"}["MultipleAnswer" in question_types],
                "TE": {True:"SL",False:"ML"}["Short" in question_types],
                "Matrix":"Likert",
                "Slider":"HSLIDER",
                "CS":"VRTL",
                "DB":"TB"#left off here
            }
            configurations = {
                "MC":{"QuestionDescriptionOption": "UseText"},
                "TE":{"QuestionDescriptionOption": "UseText"},
                "Matrix":{
                    "QuestionDescriptionOption": "UseText",
                    "TextPosition": "inline",
                    "ChoiceColumnWidth": 25,
                    "RepeatHeaders": "none",
                    "WhiteSpace": "OFF",
                    "MobileFirst": True
                    },
                "Slider":{
                    "QuestionDescriptionOption": "UseText",
                    "CSSliderMin": 0,
                    "CSSliderMax": 100,
                    "GridLines": 10,
                    "SnapToGrid": False,
                    "NumDecimals": "0",
                    "ShowValue": True,
                    "CustomStart": False,
                    "NotApplicable": False,
                    "MobileFirst": True
                },
                "CS":{"QuestionDescriptionOption": "UseText"},
                "DB":{"QuestionDescriptionOption": "UseText"}
            }

            self.info = {
                "SurveyID":survey.ID,
                "Element":"SQ",
                "PrimaryAttribute":f"QID{self.count}",
                "SecondaryAttribute":self.name,
                "TertiaryAttribute":None,
                "Payload":{
                    "QuestionText":f"{self.name}<br>",
                    "DataExportTag":f"Q{self.count}",
                    "QuestionType":qtype,
                    "Selector":selectors[qtype],
                    "Configuration": configurations[qtype],
                    "QuestionDescription":self.name,
                    "Validation": {
                        "Settings": {
                            "ForceResponse": "OFF",
                            "Type": "None"
                        }
                    },
                    "Language": [],
                    "NextChoiceId": 4,
                    "NextAnswerId": 1,
                    "QuestionID":f"QID{self.count}"
                }
            }
            self.Payload = getdict(self.info,["Payload"])
            if qtype == "CS" or qtype == "MC": self.Payload["SubSelector"] = "TX"

            if "[[Choices]]" in question_text:
                choices = [choice.strip() for choice in question_text.split("[[Choices]]")[1].split("[[")[0].split("\n") if choice.strip()]
                choice_dict = {}
                orders = []
                for x in range(len(choices)):
                    choice_dict[str(x+1)] = {"Display":choices[x]}
                    if choices[x].strip().lower() == "other (specify below)":
                        choice_dict[str(x+1)].update({"TextEntry": "true","TextEntrySize": "Small"})
                    orders.append(str(x+1))
                self.Payload["Choices"] = choice_dict
                self.Payload["ChoiceOrder"] = orders

            if "[[Answers]]" in question_text:
                answers = [answer.strip() for answer in question_text.split("[[Answers]]")[1].split("[[")[0].split("\n") if answer.strip()]
                answer_dict = {}
                orders = []
                for x in range(len(answers)):
                    answer_dict[str(x+1)] = {"Display":answers[x]}
                    orders.append(str(x+1))
                self.Payload["Answers"] = answer_dict
                self.Payload["AnswerOrder"] = orders

            self.block_info = {
                "Type":"Question",
                "QuestionID":self.info["PrimaryAttribute"]
            }
            self.survey.elements.append(self.info)

        def extract(self):
            return self.info

        
        


def main(blank_qsf, input_questions, out_qsf = False, keep_questions = False):
    keep_questions = relaxed_bool(keep_questions)
    if not out_qsf: out_qsf = input_questions.replace(".txt",".qsf")
    
    survey = Survey(blank_qsf, input_questions, keep_questions)


    with open(out_qsf,"w") as output:
        json.dump(survey.qsf, output, indent=4)
    

    

def qsf_to_json(qsf_in, json_out):
    with open(qsf_in,"r") as input:
        qsf = json.load(input)
    with open(json_out,"w") as output:
        json.dump(qsf, output, indent=4)

if __name__ == "__main__":
    if sys.argv[1] == "export_json":
        qsf_to_json(sys.argv[2:])
    else: main(*sys.argv[1:])