#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""

from globals import invertedFile as IF
import tokenizationMock

def initialiseIF():
    docId, tupleWords = tokenizationMock.nextDocument();
    for word in tupleWords:
        if (word in IF):
            if (docId in IF[word]):
                IF[word][docId] += 1
            else:
                IF[word][docId] = 1
        else:
            IF[word] = {docId: 1}
            
if __name__ == "__main__":
    initialiseIF()
    print(IF)