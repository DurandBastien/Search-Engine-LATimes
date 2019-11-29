import sys
import pickle
import os.path
from os import path
import Globals.globals as glob
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma, removeStopWords
from Tokenization import tokenizer

def launchShell(searchAlgorithm, documentServer, applyStemming = False, applyLemmatization = False, wordEmbedding = False):
	if wordEmbedding:
		# Load word embedding model
		if not path.exists('./Globals/embeddingModel'):
			if not path.exists('./Globals/embeddingDataset'):
				datasetFoldername = "../latimesTest"
				tokenizer_ = tokenizer.Tokenizer(datasetFoldername)
				glob.constructEmbeddingDataset(tokenizer_, stemming = applyStemming, lemmatization = applyLemmatization)
			embeddingFile = open('./Globals/embeddingDataset', 'rb')
			embeddingDataset = pickle.load(embeddingFile)
			embeddingFile.close()
			glob.trainModelForEmbedding(embeddingDataset)
		embeddingFile = open('./Globals/embeddingModel', 'rb')
		model = pickle.load(embeddingFile)
		print(model)
		embeddingFile.close()

		print("\nEnter the number of synonyms you want for request\'s words")
		nbSynonyms = int(sys.stdin.readline())

	while 1:
		print("\nEnter \'quit()\' to exit")
		print("Enter search query:")
		query = sys.stdin.readline()
		if "quit()" not in query:
			if wordEmbedding:
				processedQuery = processQueryString(
					query,
					stemming = applyStemming,
					lemmatization = applyLemmatization,
					embedding = True,
					embeddingModel = model,
					nbOfSynonyms = nbSynonyms)
			else:
				processedQuery = processQueryString(
					query,
					lemmatization = True)
			queryResult = searchAlgorithm(processedQuery)
			if(queryResult):
				returnedDocuments = documentServer.serveDocuments(queryResult)
				# metadata = processReturnedDocuments(returnedDocuments)
				print("\n")
				print("results:\n")
				for idx, doc in enumerate(returnedDocuments.keys()):
					print(idx+1,"----------------------------------")
					print(returnedDocuments[doc]["metadata"]),
				print("----------------------------------")
				if(returnedDocuments):
					print("choose docID")
					chosenDocId = sys.stdin.readline()
					print("\n")
					if(chosenDocId.strip() in returnedDocuments):
						print(returnedDocuments[chosenDocId.strip()]["content"],"\n")
					else:
						print("doc ID not in result")
			else:
				print("no result\n")
		else:
			break

def processQueryString(query, stemming = False, lemmatization = False, embedding = False, embeddingModel = None, nbOfSynonyms = 0):
	query = createListOfTokens(query)
	query = removeStopWords(query)

	if lemmatization:
		query = replaceWordsByLemma(query)
	elif stemming:
		query = replaceWordsByStem(query)
	
	if embedding:
		for i in range(0, len(query)):
			synonyms = findSynonyms(embeddingModel, query[i], nbOfSynonyms)
			print(synonyms)
			for newWord in synonyms:
				query.append(newWord[0])

	print(query)
	return query

def processReturnedDocuments(returnedDocuments):
	return returnedDocuments.keys()

def findSynonyms(model, myWord, nbOfSynonyms):
	word_vectors = model.wv
	try:
		synonyms = model.wv.most_similar (positive=[myWord], topn=nbOfSynonyms) 
	except:
		print(myWord, 'is not in the vocabulary')
		synonyms = []
	return synonyms