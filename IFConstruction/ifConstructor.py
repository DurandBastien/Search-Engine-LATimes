#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math;

"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma


def constructIF(tokenizer):
    global countDoc
    countDoc = 0


    for file in tokenizer.listfile[:4]:
        content = tokenizer.readFile(file)
        index = 0
        while index != len(content):
            mydoc= tokenizer.extractDocumentFromFile(content,index)

            countDoc = countDoc + 1
            d2f[mydoc[0]] = [file, mydoc[2], mydoc[3]]
            docId = mydoc[0]
            index = mydoc[3]
            tokens = createListOfTokens(mydoc[1])
            tokens = tokenizer.removeStopWords(tokens)
            tokens = replaceWordsByStem(tokens)
            #tokens = replaceWordsByLemma(tokens)


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




def giveScores():
    """
    calculate and replace the occurence of word in the doc with score

    """
    for word in IF:
        for docId in IF[word]:
            IF[word][docId] = (1 + math.log(IF[word][docId])) * math.log(countDoc / (1 + len(IF[word])))
    print(countDoc)  #132626 docs for whole dir


if __name__ == "__main__":
    constructIF()
    print(IF)
