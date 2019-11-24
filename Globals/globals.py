#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:02:35 2019

@author: clementguittat
"""

# global invertedFile
invertedFile = {}

# global docID2filename
docID2filename = {}

# global docID2ContentIndexes
docID2ContentIndexes = {}

# global vocabularyDict
vocabularyDict = {}

def loadVocabulary():
	global vocabularyDict
	vocFilename = "Globals/vocabulary.dict"
	with open(vocFilename, "r") as voc_file:
		vocabularyDict = eval(voc_file.readline())

def loadDocID2Content():
	global 	docID2ContentIndexes
	docID2CFilename = "Globals/docID2ContentIndexes.dict"
	with open(docID2CFilename, "r") as docID2ContentIndexes_file:
		docID2ContentIndexes = eval(docID2ContentIndexes_file.readline())

def voc2PostingList(word):
	global vocabularyDict
	IFname = "Globals/IF.dict"
	with open(IFname, "r") as IF_file:
		if(word in vocabularyDict):
			IF_file.seek(vocabularyDict[word])
			return IF_file.readline().strip()

def initmap():
    global invertedFile
    invertedFile = {"you": {1: 3, 2: 2}, "are": {1, 2}, "tuples": {2, 2}}