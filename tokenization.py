#!/usr/bin/env python
# coding: utf-8

import os
import re


class Tokenization:
    def __init__(self, listfile):
        self.listfile = os.listdir(listfile)
        self.path = listfile

       

    def readFile(self, file): 
        """
        read certain file whose name specified in the para
        args:
            file: name of the file to read
        """
        
        f = open(self.path + "/" + file, "r")
        content = f.readlines()
        # print(content)
        f.close()
        return content


    def extractDocumentFromFile(self, content, indexFile):
        """
        extract the info of docID and Paragraph of next document.
        call iteratively to extract the info of all docs
        args:
            content: the content of the whole file
            indexFile: where we want to begin the document analysis
           
        """
        try:
            if content == None:
                raise ValueError("file content empty!")

            nbDocId = 0
            paragraph = ""
            docid = ""
            i = -1            
            
            for i in range(indexFile, len(content)):
                if "DOCID" in content[i]:
                    nbDocId = nbDocId + 1
                    if nbDocId == 2:
                        break
                    content[i] = (
                        content[i].replace("<DOCID> ", "").replace(" </DOCID>", "")
                    )
                    docid = content[i]
                elif "<P>" in content[i]:
                    i = i + 1
                    while "</P>" not in content[i]:
                        if i + 1 >= len(content):
                            break
                        else:
                            paragraph = paragraph + content[i]
                            i = i + 1
                    
            if nbDocId == 0:
                i = len(content)
                
            return docid, paragraph, i

        except ValueError:
            return 0, 0, -1
        
        
        
    def createListOfTokens(self, paragraph):
        """
        clean the document content by removing punctuation.
        create the list of tokens.
        args:
            paragraph: the content of a specific document
           
        """
        
        #remove punctuation
        paragraph = paragraph.replace("\n","")
        paragraph = paragraph.replace(";","").replace(",","").replace("\"","")
        paragraph = paragraph.replace("/", "").replace("(", "").replace(")", "")
        
        #create tokens using space character as separator
        tokens = paragraph.split(" ")
        while "" in tokens:
            tokens.remove("")
        
        return tokens


t = Tokenization("./latimes")
content = t.readFile("la010289")
index = 0
while index != len(content):
    mydoc= t.extractDocumentFromFile(content, index)
    index = mydoc[2]
    print(index, mydoc[0])
#print(t.createListOfTokens(mydoc[1]))