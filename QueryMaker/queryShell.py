import sys
import pickle
import os.path
from os import path
import Globals.globals as glob
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma, removeStopWords
from Tokenization import tokenizer

def launchShell(searchAlgorithm, documentServer, applyStemming = False, applyLemmatization = False, wordEmbedding = False):
	'''
    launch shell to proceed a search algorithm on dataset
    args:
        searchAlgorithm: the algorithm we want to use to find relevant documents for a user query
		documentServer: module to retrieve content of document from a document id
		applyStemming: boolean value to choose to apply or not stemming on query
		applyLemmatization: boolean value to choose to apply or not lemmatization on query
		wordEmbedding: boolean value to choose to extend queries with synonyms or not
	'''
	if wordEmbedding:
		if not path.exists('./Globals/embeddingModel'):
			if not path.exists('./Globals/embeddingDataset'):
				datasetFoldername = "../latimesTest"
				tokenizer_ = tokenizer.Tokenizer(datasetFoldername)
				glob.constructEmbeddingDataset(tokenizer_, stemming = applyStemming, lemmatization = applyLemmatization)
			embeddingFile = open('./Globals/embeddingDataset', 'rb')
			embeddingDataset = pickle.load(embeddingFile)
			embeddingFile.close()
			glob.trainModelForEmbedding(embeddingDataset)
		# Load word embedding model from memory
		embeddingFile = open('./Globals/embeddingModel', 'rb')
		model = pickle.load(embeddingFile)
		embeddingFile.close()
		
		print("\nEnter the number of synonyms you want for request\'s words")
		nbSynonyms = int(sys.stdin.readline())

	while 1:
		print("\nEnter \'quit()\' to exit")
		print("Enter search query:")
		query = sys.stdin.readline()
		if "quit()" not in query:
			# Preprocessing on the query
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
					stemming = applyStemming,
					lemmatization = applyLemmatization)
			# Execution of the search algorithm on the query
			queryResult = searchAlgorithm(processedQuery)
			if(queryResult):
				returnedDocuments = documentServer.serveDocuments(queryResult)
				metadata = processReturnedDocuments(returnedDocuments)
				print("\n")
				print("result:\n")
				print(metadata, "\n")
				if(returnedDocuments):
					print("choose docID")
					chosenDocId = sys.stdin.readline()
					print("\n")
					if(chosenDocId.strip() in returnedDocuments):
						print(returnedDocuments[chosenDocId.strip()],"\n")
					else:
						print("doc ID not in result")
			else:
				print("no result\n")
		else:
			break

def processQueryString(query, stemming = False, lemmatization = False, embedding = False, embeddingModel = None, nbOfSynonyms = 0):
	'''
    Preprocessing on the query to be compatible to the search algorithm requirements
    args:
        query: a string represennting the user query
		stemming: boolean value to choose to apply or not stemming on query
		lemmatization: boolean value to choose to apply or not lemmatization on query
		embedding: boolean value to choose to extend the query with synonyms or not
		embeddingModel: the model to be able to process word embedding
		nbOfSynonyms: an integer representing the number of words answered by the model for each word in th query
	'''
	query = createListOfTokens(query)
	query = removeStopWords(query)

	if lemmatization:
		query = replaceWordsByLemma(query)
	elif stemming:
		query = replaceWordsByStem(query)
	
	if embedding:
		for i in range(0, len(query)):
			synonyms = findSynonyms(embeddingModel, query[i], nbOfSynonyms)
			for newWord in synonyms:
				query.append(newWord[0])

	print('Your query :', query)
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