#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math;

"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f


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