#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:02:35 2019

@author: clementguittat
"""

import sys
import gensim 
import pickle

from collections import OrderedDict
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma, removeStopWords

numberOfDocuments = 0 #global variable incremented when dataset read 

invertedFile = {} #global variable used when IF build in-memory

docID2ContentIndexes = {} #global variable used to map the docID to the place where the content is stored on disk

vocabularyDict = {} ##global variable used to map a word found in the dataset to the place its posting list is stored on disk

embeddingDataset = []

IF_filename = ""

#read vocabulary already stored on disk and initialize global vocabularyDict with it
def loadVocabulary(vocFilename, IF_filename_):
	global vocabularyDict
	global IF_filename
	IF_filename = IF_filename_
	# vocFilename = "Globals/vocabulary.dict"
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

def loadEmbeddingDataset():
	global 	embeddingDataset
	embeddingDatasetFilename = "Globals/embeddingDataset"
	try:
		with open(embeddingDatasetFilename, "r") as embData_file:
			for line in embData_file:
				embeddingDataset.append(eval(line.strip()))
	except OSError:
		print("Could not open/read file:", embeddingDatasetFilename)
		sys.exit()	
	
#use VocabularyDict to get on disk the posting list associated to the given word
def voc2PostingList(word):
	global invertedFile
	if(len(invertedFile.keys()) > 0):
		if(word in invertedFile):
			return invertedFile[word]
		else:
			return {}
	else:
		global vocabularyDict
		global IF_filename
		# IFname = "Globals/IF.dict"
		if(word in vocabularyDict):
			try:
				with open(IF_filename, "r") as IF_file:	
					IF_file.seek(vocabularyDict[word])
					return eval(IF_file.readline().strip())[1]
			except OSError:
				print("Could not open/read file:", IF_filename)
				sys.exit()	
		else:
			return {}

def vocList2PostingLists(words):
	global invertedFile
	result = {}
	if(len(invertedFile.keys()) > 0):
		for w in words:	
			if(w in invertedFile):
				result[w] = invertedFile[w]
			else:
				result[w] = {}
	else:
		global vocabularyDict
		global IF_filename
		# IFname = "Globals/IF.dict"
		wordsToFetch = []
		for w in words:
			wordsToFetch.append([w])
			if(w in vocabularyDict):
				wordsToFetch[-1].append(vocabularyDict[w])
			else:
				wordsToFetch[-1].append(None)
		wordsToFetch.sort(key=lambda x:(x[1] is None, x[1]))
		try:
			with open(IF_filename, "r") as IF_file:
				for entry in wordsToFetch:
					if(entry[1] != None):
						IF_file.seek(entry[1])
						result[entry[0]] = eval(IF_file.readline().strip())[1]
					else:
						result[entry[0]] = {}
		except OSError:
			print("Could not open/read file:", IF_filename)
			sys.exit()	
	return result


# def initmap():
#     invertedFile = {"you": {1: 3, 2: 2}, "are": {1: 2}, "tuples": {2: 2}}

def constructEmbeddingDataset(tokenizer, stemming = False, lemmatization = False):
	documentsForEmbedding = []
	
	for file in tokenizer.listfile:
		content = tokenizer.readFile(file)
		print(file)
		index = 0
		while index != len(content):
			mydoc= tokenizer.extractDocumentFromFile(content,index)
			index = mydoc[3]
			tokens = createListOfTokens(mydoc[1])
			tokens = removeStopWords(tokens)
			if lemmatization:
				tokens = replaceWordsByLemma(tokens)
			elif stemming:
				tokens = replaceWordsByStem(tokens)
			if index != len(content):
				documentsForEmbedding.append(tokens)

	# Write in memory the dataset for wordEmbedding
	embeddingFile = open('./Globals/embeddingDataset', 'wb')
	pickle.dump(documentsForEmbedding, embeddingFile)
	embeddingFile.close()
	print("The dataset for word embedding has been stored in memory.")

def trainModelForEmbedding(listOfDocuments):
	model = gensim.models.Word2Vec(
		listOfDocuments,
		size = 100,
		window = 10,
		min_count = 1,
		workers = 10,
		iter = 10
	)

	# Write in memory the model for wordEmbedding
	embeddingFile = open('./Globals/embeddingModel', 'wb')
	pickle.dump(model, embeddingFile)
	embeddingFile.close()
	print("Model for embedding has been stored in memory.")
