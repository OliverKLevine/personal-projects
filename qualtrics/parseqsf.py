import os
import sys
import json

def main(blank_qsf, input_questions, out_qsf = False, keep_questions = False):
    if not out_qsf: out_qsf = blank_qsf
    with open(blank_qsf, "r") as input:
        qsf = json.load(input)
    if not keep_questions:
        
    
    with open(out_qsf,"w") as output:
        json.dump(qsf, output)
    

    

def qsf_to_json(qsf_in, json_out):
    with open(qsf_in,"r") as input:
        qsf = json.load(input)
    with open(json_out,"w") as output:
        json.dump(qsf, output, indent=4)

if __name__ == "__main__":
    if sys.argv[1] == "export_json":
        qsf_to_json(sys.argv[2:])
    else: main(*sys.argv[1:])