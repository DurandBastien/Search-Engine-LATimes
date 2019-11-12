#!/usr/bin/env python
# coding: utf-8

import os
import re


class Tokenization:
    def __init__(self, listfile):
        self.listfile = os.listdir(listfile)
        self.path = listfile

        """
        read certain file whose name specified in the para
        args:
            file: name of the file to read
        """

    def readFile(self, file):
        f = open(self.path + "/" + file, "r")
        content = f.readlines()
        # print(content)
        f.close()
        return content

        """
        extract the info of docID and Paragraph of next document.
        call iteratively to extract the info of all docs
        args:
            content: the content of the whole file
           
        """

    def extractDocumentFromFile(self, content):
        try:
            if content == None:
                raise ValueError("file content empty!")

            nbDocId = 0
            paragraph = ""

            for i in range(0, len(content)):
                if "DOCID" in content[i]:
                    nbDocId = nbDocId + 1
                    if nbDocId == 2:
                        break
                    content[i] = (
                        content[i].replace("<DOCID> ", "").replace(" </DOCID>", "")
                    )
                    docid = content[i]
                elif "<P>" in content[i]:
                    #content[i] = "" #useless
                    i = i + 1
                    while "</P>" not in content[i]:
                        if i + 1 >= len(content):
                            break
                        else:
                            paragraph = paragraph + content[i]
                            i = i + 1
                    #content[i] = "" #useless

            return docid, paragraph

        except ValueError:
            return 0, 0
        
        
        """
        clean the document content by removing punctuation.
        create the list of tokens.
        args:
            paragraph: the content of a specific document
           
        """
        
    def createListOfTokens(self, paragraph):
        
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
mydoc= t.extractDocumentFromFile(content)
print(mydoc)
print(t.createListOfTokens(mydoc[1]))
#print(t.nextDocument(content))
#print(t.nextDocument(content))