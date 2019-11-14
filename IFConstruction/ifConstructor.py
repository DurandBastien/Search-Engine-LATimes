#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""

from Globals.globals import invertedFile as IF
# import tokenizationMock
import Tokenization.tokenizer

def constructIF(tokenizer):

    for file in tokenizer.listfile:
        content = tokenizer.readFile(file)
        index = 0;
        while index != len(content):
            mydoc= tokenizer.extractDocumentFromFile(content,index)
            docId = mydoc[2]
            tokens = tokenizer.createListOfTokens(mydoc[1])
            tokens = tokenizer.removeStopWords(tokens)

            for word in tokens:
                if (word in IF):
                    if (docId in IF[word]):
                        IF[word][docId] += 1
                    else:
                        IF[word][docId] = 1
                else:
                    IF[word] = {docId: 1}
            
if __name__ == "__main__":
    constructIF()
    print(IF)