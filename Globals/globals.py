#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:02:35 2019

@author: clementguittat
"""

from collections import OrderedDict

invertedFile = {} #global variable used when IF build in-memory

docID2ContentIndexes = {} #global variable used to map the docID to the place where the content is stored on disk

vocabularyDict = {} ##global variable used to map a word found in the dataset to the place its posting list is stored on disk

#read vocabulary already stored on disk and initialize global vocabularyDict with it
def loadVocabulary():
	global vocabularyDict
	vocFilename = "Globals/vocabulary.dict"
	try:
		with open(vocFilename, "r") as voc_file:
			vocabularyDict = eval(voc_file.readline())
	except OSError:
		print("Could not open/read file:", vocFilename)
		sys.exit()

#read doc ID to content mapping already stored on disk and initialize global docID2ContentIndexes with it
def loadDocID2Content():
	global 	docID2ContentIndexes
	docID2CFilename = "Globals/docID2ContentIndexes.dict"
	try:
		with open(docID2CFilename, "r") as docID2ContentIndexes_file:
			docID2ContentIndexes = eval(docID2ContentIndexes_file.readline())
	except OSError:
		print("Could not open/read file:", docID2CFilename)
		sys.exit()	
	
#use VocabularyDict to get on disk the posting list associated to the given word
def voc2PostingList(word):
	global invertedFile
	if(len(invertedFile.keys()) > 0):
		if(word in invertedFile):
			return invertedFile[word]
		else:
			return None
	else:
		global vocabularyDict
		IFname = "Globals/IF.dict"
		if(word in vocabularyDict):
			try:
				with open(IFname, "r") as IF_file:	
					IF_file.seek(vocabularyDict[word])
					return eval(IF_file.readline().strip())[1]
			except OSError:
				print("Could not open/read file:", IFname)
				sys.exit()	
		else:
			return None

# def initmap():
#     invertedFile = {"you": {1: 3, 2: 2}, "are": {1: 2}, "tuples": {2: 2}}
