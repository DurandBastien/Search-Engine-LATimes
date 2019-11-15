#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:28:26 2019

@author: clementguittat
"""

from collections import Counter
from Globals.globals import invertedFile as IF

def naiveAlgo(query):
    if(not IF):
        return []
    finalDic = dict();
    for keyword in query.split():
        if (keyword in IF):
            finalDic = dict(Counter(finalDic) + Counter(IF[keyword]))
    print(finalDic)
    listValues = list(finalDic.values())
    listKeys = list(finalDic.keys())
    bestDoc = listKeys[listValues.index(max(listValues))]
    return [bestDoc]
    
if __name__ == "__main__":
    IF = {"you": {1: 3, 2: 2}, "are": {1: 2}, "tuples": {2: 2}}
    naiveAlgo("you tuples")
    