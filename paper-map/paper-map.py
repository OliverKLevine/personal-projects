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
'''

import sys
import os
import PyPDF2
from multiprocessing import Pool
import numpy as np
import time

pdf_dir = os.getcwd()
slash = "/"
if("\\" in pdf_dir): slash = "\\"
pdf_dir = pdf_dir[:pdf_dir.index("Users")+6+pdf_dir[pdf_dir.index("Users")+6:].index(slash)]

zotero = True

if(zotero): pdf_dir += "/Zotero/Storage/"
else: pass

print(pdf_dir)

class Paper:
    def __init__(self, name, text):
        self.name = name
        self.text = text

pdf_paths = []
for (dir_path, dir_names, file_names) in os.walk(pdf_dir):
    for file in file_names:
        if(file[len(file)-4:] == ".pdf"):
            pdf_paths.append(dir_path+slash+file)

def read_pdf(pathlist):
    papers = []
    for path in pathlist:
        f = open(path, "rb")
        pdf = PyPDF2.PdfFileReader(f,strict=False)
        pagecount = pdf.numPages
        string = ""
        references = True
        for x in range(pagecount-1,0,-1):
            pagetext = pdf.getPage(x).extractText()
            if("References" in pagetext):
                string = pagetext[pagetext.index("References"):] + string
                break
            else: string = pagetext + string
        papers.append(Paper(file[:len(file)-4],string))
        f.close()
    return(papers)

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
p_input = np.array_split(pdf_paths,num_p)
with Pool(num_p) as p:
    papers = p.map(read_pdf, p_input)
papers = [paper for sublist in papers for paper in sublist]

