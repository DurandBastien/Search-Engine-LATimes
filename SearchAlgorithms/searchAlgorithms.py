#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:28:26 2019

@author: clementguittat
"""

# import sys
# sys.path.insert(1, '/Users/clementguittat/Documents/INSA LYON/5A/QueryText/Search-Engine-LATimes')
from collections import Counter, OrderedDict
import Globals.globals as glob

# Algo naif 
# Fonctionnement pour 1 mot-clé dans la requête => 
# on calcule le nombre d'occurences dans chacun des documents. Le score associé à chacun des documents correspond à ce nb d'occurences
# puis je classe les documents par rapport à leur score  

#Fonctionnement pour plusieurs mot-clé dans la requête =>
# pour chaque mot-clé on calcule le score associé au document. Puis pour chaque document, on calcule son score global sur la requête en additionnant le score obtenu par mot-clé
# puis je classe les documents par rapport à leur score 
def naiveAlgo(query):
    # if(not glob.invertedFile):
    #     return []
    finalDic = dict()
    for keyword in query:
        postingList = glob.voc2PostingList(keyword)
        if (postingList != None):
            finalDic = dict(Counter(finalDic) + Counter(postingList)) # additionne les valeurs des deux dictionnaires avec la même clé
    return [doc[0] for doc in ranking(finalDic)]

def faginAlgo(query):
    IFOther = {"you": {1: 3, 2: 2, 3: 1, 4:1, 5:1}, "are": {4: 6, 1: 2, 3: 2, 5:1} }
    if(not IFOther):
        return []
    M = dict();
    C = []
    nbTopElements = 3
    listWordsQuery = query.split()
    nbOfElementsInQuery = len(listWordsQuery)
    indexWord = 0
    indexPL = 0
    while(len(C) < nbTopElements):
        keyword = listWordsQuery[indexWord]
        if (keyword in IFOther):
            if indexPL < len(IFOther[keyword]): # si on a pas parcouru toute la taille d'une des PLliste on continue 
                docId = list(IFOther[keyword])[indexPL] #docID pour l'indexe de la PLliste du terme à parcourir 
                score = IFOther[keyword][docId] #le score de ce docID
                if (docId in M):
                    previousScore, nbTimesSeen = M[docId]
                    M[docId] = (previousScore + score, nbTimesSeen + 1) # on utilise la somme pour calculer les scores des documents 
                    if (nbTimesSeen + 1 == nbOfElementsInQuery): #si on a toruvé un document qui est dans toutes les PLlistes alors on l'ajoute à C
                        C.append((docId, previousScore + score))
                        del M[docId]
                else : # si c'est la première fois qu'on rencontre ce document on ajoute l'ajoute à M avec son score et nbdefoisvu à 1 
                    M[docId] = (score, 1)
            else: # si on a parcouru une des PLlistes en entier, on break car on sait qu'on aura plus rien à ajouter à C 
                print("in")
                break
        indexWord = indexWord+1
        if (indexWord == nbOfElementsInQuery):#si on a parcouru tous les mots de la query, alors on peut passer au niveau suivant dans les PLlistes, on incrémente l'index indexPL pour regarder le prochain élement de chaque PLliste 
            indexWord = 0
            indexPL = indexPL+1
 
    dictScore = dict()
    for ID in M.keys(): #on parcourt tous les documents restants dans M pour vérifier que leur score ne soit pas supérieur à ceux déjà dans C  
        for keyword in listWordsQuery: # on va parcourir toutes les PLlistes et trouver le score pour un document en les additionnant. On est alors disjonctif en utilisant l'additionnant car un docuement ne comportant pas un terme ne sera pas pénalisé mais si bcp dans un document alors quand même sélectionné
            if (keyword in IFOther):
                if ID in IFOther[keyword]:
                    if ID in dictScore :
                        dictScore[ID] = dictScore[ID] + IFOther[keyword][ID]
                    else: 
                        dictScore[ID] = IFOther[keyword][ID]

    for key,value in dictScore.items():
        C.append((key, value))
    C = sorted(C, key=lambda x:x[1], reverse=True)[:nbTopElements]
    return [doc[0] for doc in C]
    

# Fonction de classement des documents selon leur score 
def ranking(finalDic):
    # for docId, freq  in sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]:
        # print("document ID:", docId, " freq:", freq)
    return sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]
    
if __name__ == "__main__":
    IF = {"you": {1: 3, 2: 2, 3:1}, "are": {1: 2, 3:2, 4: 6}, "tuples": {2: 2, 3:3}, "hello": {1: 4, 2: 5, 3:10}}
    ##naiveAlgo("you tuples")
    faginAlgo("you are")
    