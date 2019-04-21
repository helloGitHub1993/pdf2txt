#!/usr/bin/env python
#coding=utf-8

import sys
import importlib
import os
importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


#Get the file names in current directory
def file_name(file_dir):
    L=[]
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.pdf':
                L.append(os.path.join(root,file))
    return L


#Parsing PDF docs and saved as txt docs
def parse(path):
    tmp = file[i].split('/')
    #The output files will be kept in "res" directory,so please make a "res" directory before run this program
    res_name = './res/' + os.path.splitext(tmp[len(tmp)-1])[0] + '.txt'
    fp = open(path, 'rb') 
    #Create a pdf parser
    praser = PDFParser(fp)
    # Create a pdf doc
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)

    # init
    doc.initialize()

    #Check whether the doc provides TXT conversion 
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # Create pdf resource manager
        rsrcmgr = PDFResourceManager()
        # Create a pdf device object
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create a pdf interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages(): 
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(res_name, 'a',encoding='utf-8') as f:
                        results = x.get_text()
                        print(results)
                        f.write(results + '\n')

if __name__=="__main__":
    file = file_name("./")
    for i in range(len(file)):
       path = file[i]
       parse(path)
