'''
State of the union:
This program currently opens all the pdfs in my zotero library, grabs all the text from "References" to the end of the pdf, and dumps it in string format into "Paper" object. 
Paper object currently does nothing except store name and text string.
Added multiprocessing & made code more efficient. End result: time to open and read PDFs reduced from 20s to 3s.

Next step: parse the text string in each Paper object to a list of Reference objects. 
- This list should be global (ie if the same paper is referenced in two different papers, only one reference object should be created for it, storing its association with both papers that cited it.)
- Should this be the same object as Paper?
    - Should I pass it the first page so it can figure out its own reference? Go looking for reference in Zotero?
        - Yes, this will probably be needed to get title, author firstnames, etc.

Desired features:
- Author object that can contain refs to all papers published under their name, and authorship order (identify people who are Big NamesTM)

text files wtf
'''

import sys
import os
import PyPDF2
from multiprocessing import Pool
import numpy as np
import time

class Paper:
    def __init__(self, name, text):
        self.name = name
        self.text = text

def read_pdf(pathlist):
    print(len(pathlist))
    text_files_path = "./text_files"
    for path in pathlist:
        with open(path, "rb") as f:
            pdf = PyPDF2.PdfFileReader(f,strict=False)
            pagecount = pdf.numPages
            string = ""
            for x in range(0,pagecount):
                string += pdf.getPage(x).extractText()
            txt_path = os.path.basename(path)
            txt_path = os.path.join(text_files_path,txt_path[:txt_path.rindex(".")] + ".txt")
            with open(txt_path,"w") as out_file:
                out_file.write(string)

def main():

    directories = {}
    directories["pdf"] = os.getcwd()
    directories["txt"] = os.path.join(directories["pdf"],"text_files")
    slash = "/"
    if("\\" in directories["pdf"]): slash = "\\"
    directories["pdf"] = directories["pdf"][:directories["pdf"].index("Users")+6+directories["pdf"][directories["pdf"].index("Users")+6:].index(slash)]

    zotero = True

    if(zotero): directories["pdf"] += "/Zotero/Storage/"
    else: pass

    print(directories["pdf"])

    file_paths = {}
    for type in directories:
        for (dir_path, dir_names, file_names) in os.walk(directories[type]):
            for file in file_names:
                if(file[file.rindex(".")+1:] == type):
                    if not file[:file.rindex(".")] in file_paths: file_paths[file[:file.rindex(".")]] = {}
                    file_paths[file[:file.rindex(".")]][type] = dir_path+slash+file

    untranslated = [file_paths[i]["pdf"] for i in file_paths if "txt" not in file_paths[i]]

    print(untranslated)

    papers = []
    '''for pdf in progressBar(pdf_paths, prefix = 'Progress:', suffix = 'Complete', length = 50):
        papers.append(read_pdf(pdf))'''

    num_p = 4
    '''Note 2/7/23: 
        With my current Zotero library, the ideal number of processes is 4:
        # processes:time(s), one trial each:
        - ['1:9.793448099999296', '2:5.566195700000208', '3:3.867462300000625', '4:2.8168375000004744', '5:2.91246080000019', '6:2.8354879000007713', '7:2.913536699999895', '8:2.958448400000634', '9:2.8906716999999844', '10:2.891614999999547', '11:2.9242064000000028', '12:2.858286499999849', '13:2.8211081999997987', '14:2.8489654999993945', '15:3.071777699999984', '16:3.0568671999999424', '17:3.097930599999927', '18:3.139920399999937', '19:3.1246350000001257', '20:3.0756861999998364']
        
        Remember to recheck occasionally. check with:
            def trial(num_p,p_input):
                start = time.perf_counter()
                with Pool(num_p) as p:
                    papers = p.map(read_pdf, p_input)
                    pass
                finish = time.perf_counter()
                return(finish-start)

            processing = []
            for x in range(1,21):
                processing.append(str(x) + ":" +str(trial(x, p_input)))
                print(processing[len(processing)-1])

            print(processing)
        '''
    p_input = np.array_split(untranslated,num_p)
    with Pool(num_p) as p:
        p.map(read_pdf, p_input)
    print("done")

if __name__ == "__main__":
    main()
