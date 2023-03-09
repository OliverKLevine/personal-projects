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
import aspose.words as aw
from multiprocessing import Pool
import numpy as np
import time

class Paper:
    def __init__(self, name, text):
        self.name = name
        self.text = text

def read_pdf(pathlist):
    text_files_path = "./text_files"
    for path in pathlist:
        doc = aw.Document(path)
        doc.save(text_files_path + path[path.rindex("/")+1:path.rindex(".")] + ".md")


def main():

    file_dirs = {}
    file_dirs["pdf"] = os.path.expanduser("~")
    file_dirs["md"] = os.path.join(os.getcwd(),"text_files")
    slash = "/"
    if("\\" in file_dirs["md"]): slash = "\\"

    zotero = True

    if(zotero): file_dirs["pdf"] += "/Zotero/storage"
    else: pass

    #print(file_dirs["pdf"])

    file_paths = {}
    for file_type in file_dirs:
        for (dir_path, dir_names, file_names) in os.walk(file_dirs[file_type]):
            print((dir_path,dir_names,file_names))
            for file in file_names:
                if(file[file.rindex(".")+1:] == file_type):
                    if not file[:file.rindex(".")] in file_paths: file_paths[file[:file.rindex(".")]] = {}
                    file_paths[file[:file.rindex(".")]][file_type] = dir_path+slash+file

    untranslated = [file_paths[i]["pdf"] for i in file_paths if "txt" not in file_paths[i]]

    print(untranslated)
    
    for file in untranslated:
        doc = aw.Document(file)
        doc.save(file_paths["md"] + file[file.rindex("/")+1:file.rindex(".")] + ".md")


if __name__ == "__main__":
    main()
