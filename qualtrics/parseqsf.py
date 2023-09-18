import os
import sys
import json

def main(qsf_json, blank_qsf, out_qsf, switch = False):
    if switch:
        qsf_json, out_qsf = out_qsf, qsf_json
    with open(qsf_json, "r") as input:
        qsf = json.load(input)
    
    if not switch:
        qsf["SurveyEntry"]["SurveyID"] = "SV_cHXMOV5X1K2nWgm"
        for x in range(len(qsf["SurveyElements"])-1,-1,-1):
            qsf["SurveyElements"][x]["SurveyID"] = "SV_cHXMOV5X1K2nWgm"
    
        with open(out_qsf,"w") as output:
            json.dump(qsf, output)
    else:
        with open(out_qsf,"w") as output:
            json.dump(qsf, output, indent=4)

def qsf_to_json(qsf_in, json_out):
    with open(qsf_in,"r") as input:
        qsf = json.load(input)
    with open(json_out,"w") as output:
        json.dump(qsf, output, indent=4)

if __name__ == "__main__":
    if sys.argv[1] == "export_json":
        qsf_to_json(sys.argv[2:])
    else: main(*sys.argv[1:])