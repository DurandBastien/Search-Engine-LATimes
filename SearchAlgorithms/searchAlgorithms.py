#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:28:26 2019

@author: clementguittat
"""

import sys
sys.path.insert(1, '/Users/clementguittat/Documents/INSA LYON/5A/QueryText/Search-Engine-LATimes')
from collections import Counter
from Globals.globals import invertedFile as IF

# Algo naif 
# Fonctionnement pour 1 mot-clé dans la requête => 
# on calcule le nombre d'occurences dans chacun des documents. Le score associé à chacun des documents correspond à ce nb d'occurences
# puis je classe les documents par rapport à leur score  

#Fonctionnement pour plusieurs mot-clé dans la requête =>
# pour chaque mot-clé on calcule le score associé au document. Puis pour chaque document, on calcule son score global sur la requête en additionnant le score obtenu par mot-clé
# puis je classe les documents par rapport à leur score 
def naiveAlgo(query):
    if(not IF):
        return []
    finalDic = dict();
    for keyword in query.split():
        if (keyword in IF):
            finalDic = dict(Counter(finalDic) + Counter(IF[keyword])) # additionne les valeurs des deux dictionnaires avec la même clé
    return ranking(finalDic)

def faginAlgo(query):
    IFOther = {"you": [(1, 3), (2, 2), (3,1)], "are": [(4, 6), (1, 2), (3,2)]}
    IFID2Term = {1 : {"you": 3, "are": 2}, 2: {"you": 2}, 3: {"you":1, "are": 2}, 4: {"are":6}}
    if(not IFOther):
        return []
    M = dict();
    C = []
    nbTopElements = 2
    listWordsQuery = query.split()
    nbOfElementsInQuery = len(listWordsQuery)
    indexWord = 0
    indexPL = 0
    while(len(C) < nbTopElements):
        keyword = listWordsQuery[indexWord]
        if (keyword in IFOther):
            if indexPL < len(IFOther[keyword]):
                docId, score = IFOther[keyword][indexPL]
                if (docId in M):
                    previousScore, nbTimesSeen = M[docId]
                    M[docId] = (previousScore + score, nbTimesSeen + 1)
                    if (nbTimesSeen + 1 == nbOfElementsInQuery):
                        C.append((docId, previousScore + score))
                        del M[docId]
                else :
                    M[docId] = (score, 1)
        indexWord = indexWord+1
        if (indexWord == nbOfElementsInQuery):
            indexWord = 0
            indexPL = indexPL+1

    dictScore = dict()
    for ID in M.keys():
        termScoreMap = IFID2Term[ID]
        dictScore[ID] = sum(termScoreMap.values())
    for key,value in dictScore.items():
        C.append((key, value))
    C = sorted(C, key=lambda x:x[1], reverse=True)[:nbTopElements]
    
        #for value in IFID2Term.values():
            #for scoresDoc in value.values():
                #print(dictScore)
                #if(ID in dictScore):
                  #  dictScore[ID] = dictScore[ID] + scoresDoc
               # else:
                  #  dictScore[ID] = scoresDoc
        
        

# Fonction de classement des documents selon leur score 
def ranking(finalDic):
    # for docId, freq  in sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]:
        # print("document ID:", docId, " freq:", freq)
    return sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]
    
if __name__ == "__main__":
    IF = {"you": {1: 3, 2: 2, 3:1}, "are": {1: 2, 3:2, 4: 6}, "tuples": {2: 2, 3:3}, "hello": {1: 4, 2: 5, 3:10}}
    ##naiveAlgo("you tuples")
    faginAlgo("you are")
    