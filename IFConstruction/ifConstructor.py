#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""

from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f
# import tokenizationMock
import Tokenization.tokenizer

def constructIF(tokenizer):

    #print(tokenizer.listfile)
    for file in tokenizer.listfile[:10]:
        content = tokenizer.readFile(file)
        index = 0
        #print(file)
        while index != len(content):
            mydoc= tokenizer.extractDocumentFromFile(content,index)
            d2f[mydoc[0]] = [file, mydoc[2], mydoc[3]]
            docId = mydoc[0]
            index = mydoc[3]
            tokens = tokenizer.createListOfTokens(mydoc[1])
            tokens = tokenizer.removeStopWords(tokens)
            tokens = tokenizer.replaceWordsByStem(tokens)

            for word in tokens:
                if (word in IF):
                    if (docId in IF[word]):
                        IF[word][docId] += 1
                    else:
                        IF[word][docId] = 1
                else:
                    IF[word] = {docId: 1}
        print(file, len(IF)) 

def constructIFFromStreamTokenizer(streamTokenizer):
    counter = 0
    docFromStream = streamTokenizer.getNextDocAsTokens()
    while(docFromStream):
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
        d2f[docID] = [filename, docIndexStart, docIndexEnd]
        for word in tokens.split():
            if (word in IF):
                if (docID in IF[word]):
                    IF[word][docID] += 1
                else:
                    IF[word][docID] = 1
            else:
                IF[word] = {docID: 1}
        docFromStream = streamTokenizer.getNextDocAsTokens()
        if(counter == 9):
            break
        counter+=1
def constructIF_diskBased(streamTokenizer, runSize):
    runCounter = 0
    docFromStream = streamTokenizer.getNextDocAsTokens()
    while(docFromStream):
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
        runTriples = []
        if(runCounter < runSize):
            docWiseDict = {}
            for word in tokens:
                if (word in docWiseDict):
                    docWiseDict[word] += 1
                else:
                    docWiseDict = 1
            for word in docWiseDict:
                runTriples.append([word, docID, docWiseDict[word]])
        else:
            #flush runTriples
            runCounter = 0

        docFromStream = streamTokenizer.getNextDocAsTokens()


if __name__ == "__main__":
    constructIF()
    print(IF)