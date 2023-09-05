import os
import sys
import json

def main(qsf_json, out_qsf):
    with open(qsf_json, "r") as input:
        qsf = json.load(input)
    
    qsf["SurveyEntry"]["SurveyID"] = None
    qsf["SurveyEntry"]["SurveyName"] = None
    qsf["SurveyEntry"]["SurveyOwnerID"] = None
    qsf["SurveyEntry"]["CreatorID"] = None
    qsf["SurveyEntry"]["SurveyActiveResponseSet"] = None

    for x in range(len(qsf["SurveyElements"])-1,0,-1):
        if qsf["SurveyElements"][x]["Element"] == "NT":
            qsf["SurveyElements"].pop(x)
    
    with open(out_qsf,"w") as output:
        json.dump(qsf, output)

if __name__ == "__main__":
    main(*sys.argv[1:])