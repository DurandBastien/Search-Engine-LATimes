#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:28:26 2019

@author: clementguittat
"""

import sys
import heapq
sys.path.insert(1, '/Users/clementguittat/Documents/INSA LYON/5A/QueryText/Search-Engine-LATimes')

from collections import Counter, OrderedDict
from SearchAlgorithms.minHeap import PQNode
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
    for keyword,_ in query:
        postingList = glob.voc2PostingList(keyword)
        if (postingList != None):
            finalDic = dict(Counter(finalDic) + Counter(postingList)) # additionne les valeurs des deux dictionnaires avec la même clé
    return [doc[0] for doc in ranking(finalDic)]

# Fonction de classement des documents selon leur score 
def ranking(finalDic):
    # for docId, freq  in sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]:
        # print("document ID:", docId, " freq:", freq)
    return sorted(finalDic.items(), key=lambda x: x[1], reverse=True)[:10]

def faginAlgo(query):
    M = dict();
    C = []
    nbTopElements = 10
    listWordsQuery = query
    IF = glob.vocList2PostingLists([x[0] for x in listWordsQuery])
    nbOfElementsInQuery = len(listWordsQuery)
    listEndedPL = set()
    indexWord = 0
    indexPL = 0
    print(nbOfElementsInQuery)
    while(len(C) < nbTopElements and len(listEndedPL) < nbOfElementsInQuery):
        keyword, scorePower = listWordsQuery[indexWord]
        if (keyword in IF):
            if indexPL < len(IF[keyword]): # si on a pas parcouru toute la taille d'une des PLliste on continue
                docId = list(IF[keyword])[indexPL] #docID pour l'indexe de la PLliste du terme à parcourir
                score = IF[keyword][docId]*scorePower #le score de ce docID multiplié par l'importance du mot dans la query, dépend notamment si synonyme ou mot de la requete 
                if (docId in M):
                    previousScore, nbTimesSeen = M[docId]
                    M[docId] = (previousScore + score, nbTimesSeen + 1) # on utilise la somme pour calculer les scores des documents 
                    if (nbTimesSeen + 1 == nbOfElementsInQuery): #si on a toruvé un document qui est dans toutes les PLlistes alors on l'ajoute à C
                        C.append((docId, previousScore + score))
                        print(C)
                        del M[docId]
                else : # si c'est la première fois qu'on rencontre ce document on ajoute l'ajoute à M avec son score et nbdefoisvu à 1 
                    if (nbOfElementsInQuery == 1): #si on a trouvé un document qui est dans toutes les PLlistes alors on l'ajoute à C
                        C.append((docId, score))
                    else :
                        M[docId] = (score, 1)
            else: # si on a parcouru une des PLlistes en entier, on break car on sait qu'on aura plus rien à ajouter à C 
                listEndedPL.add(indexWord)
        indexWord = indexWord+1
        if (indexWord == nbOfElementsInQuery):#si on a parcouru tous les mots de la query, alors on peut passer au niveau suivant dans les PLlistes, on incrémente l'index indexPL pour regarder le prochain élement de chaque PLliste 
            indexWord = 0
            indexPL = indexPL+1
 
    dictScore = dict()
    for ID in M.keys(): #on parcourt tous les documents restants dans M pour vérifier que leur score ne soit pas supérieur à ceux déjà dans C  
        for keyword, _ in listWordsQuery: # on va parcourir toutes les PLlistes et trouver le score pour un document en les additionnant. On est alors disjonctif en utilisant l'additionnant car un docuement ne comportant pas un terme ne sera pas pénalisé mais si bcp dans un document alors quand même sélectionné
            if (keyword in IF):
                if ID in IF[keyword]:
                    if ID in dictScore:
                        dictScore[ID] = dictScore[ID] + IF[keyword][ID]
                    else: 
                        dictScore[ID] = IF[keyword][ID]

    for key,value in dictScore.items():
        C.append((key, value))
    C = sorted(C, key=lambda x:x[1], reverse=True)[:nbTopElements]
    return [doc[0] for doc in C]


def threshold(query):
    '''
    :param query: query string
    :return: the topk results
    '''
    listWordsQuery = query
    IF = glob.vocList2PostingLists([x[0] for x in listWordsQuery])

    dictMerge = {}
    nbTop = 10
    for keyword, power in listWordsQuery:
        if (keyword in IF):
            for k in IF[keyword].keys():
                if k in dictMerge:
                    dictMerge[k] = dictMerge[k] + IF[keyword][k] * power
                else:
                    dictMerge[k] = IF[keyword][k] * power


    heap = []
    indexPL = 0

    if(len((x[0] for x in listWordsQuery) & IF.keys())==1 and IF[listWordsQuery[0][0]]=={}):
        return []

    while True:
        threshold = 0
        for keyword, power in listWordsQuery:
            if keyword in IF.keys():
                if indexPL < len(IF[keyword]):  # si on a pas parcouru toute la taille d'une des PLliste on continue
                    docId = list(IF[keyword])[indexPL]  # docID pour l'indexe de la PLliste du terme à parcourir
                    score = IF[keyword][docId] * power
                    scoreAll = dictMerge[docId] # le score de ce docID ds tout PL
                    newNode = PQNode(docId,scoreAll)
                    if newNode not in heap:
                        heapq.heappush(heap, newNode)
                    threshold = threshold + score

        indexPL = indexPL + 1
        if getKthElement(nbTop,heap).value > threshold:
            res = []
            for node in heapq.nlargest(nbTop,heap):
                res.append(node.key)
            return res



def getKthElement(k,heap):

    res = heapq.nlargest(k, heap)[-1]
    return res

def testPQNode():
    '''
    to test if PQnode works as a minHeap

    '''
    input = [PQNode(1, 4), PQNode(7, 4), PQNode(6, 9), PQNode(2, 5)]
    hinput = []
    for item in input:
        heapq.heappush(hinput, item)
    print(getKthElement(1, input))

    while (hinput):
        print(heapq.heappop(hinput))



if __name__ == "__main__":
    
    ##naiveAlgo("you tuples")
    faginAlgo(["january"])


    #threshold("you are")