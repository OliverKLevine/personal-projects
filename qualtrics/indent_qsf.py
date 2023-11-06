import json
import sys


def main():
    input_file = sys.argv[1]
    with open(input_file,"r") as input:
        qsf = json.load(input)
    output_file = f"{input_file.split('.')[0]}_qsf.json"
    if len(sys.argv) > 2: output_file = sys.argv[2]
    with open(output_file,"w") as output:
        json.dump(qsf, output, indent=4)

if __name__ == "__main__":
    main()