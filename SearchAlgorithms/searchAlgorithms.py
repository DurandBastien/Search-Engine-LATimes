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
    if(not IF):
        return []
    listDocumentsScoreSeenforAtLeastOneWord = []
    listDocumentsScoreSeenforAllWords = []
    
    
        
            

# Fonction de classement des documents selon leur score 
def ranking(finalDic):
    # for docId, freq  in sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]:
        # print("document ID:", docId, " freq:", freq)
    return sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]
    
if __name__ == "__main__":
    IF = {"you": {1: 3, 2: 2, 3:1}, "are": {4: 6, 1: 2, 3:2}, "tuples": {3:3, 2: 2}, "hello": {3:10, 2: 5, 1: 4}}
    naiveAlgo("you tuples")
    