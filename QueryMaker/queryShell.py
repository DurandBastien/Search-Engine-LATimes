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
				datasetFoldername = "../../latimes/latimes"
				tokenizer_ = tokenizer.Tokenizer(datasetFoldername)
				glob.constructEmbeddingDataset(tokenizer_, stemming = applyStemming, lemmatization = applyLemmatization)
			embeddingFile = open('./Globals/embeddingDataset', 'rb')
			embeddingDataset = pickle.load(embeddingFile)
			embeddingFile.close()
			glob.trainModelForEmbedding(embeddingDataset)
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

def createTokensWithScore(listOfTokens):
	tokenWithScore = []
	for token in listOfTokens:
		mytoken = (token, 3)
		tokenWithScore.append(mytoken)
	return tokenWithScore

def deleteDuplicatesInQuery(queryWithScore):
	myWords = [token[0] for token in queryWithScore]
	wordsWithoutDuplicates = []
	for i in range(len(myWords)):
		if myWords[i] not in myWords[:i]:
			indices = [k for k in range(len(myWords)) if myWords[k]==myWords[i]]
			myScore = 0
			for indice in indices:
				myScore += queryWithScore[indice][1]
			wordsWithoutDuplicates.append((myWords[i], myScore))
	return wordsWithoutDuplicates
	
def processQueryString(query, stemming = False, lemmatization = False, embedding = False, embeddingModel = None, nbOfSynonyms = 0):
	query = createListOfTokens(query)
	query = removeStopWords(query)

	if lemmatization:
		query = replaceWordsByLemma(query)
	elif stemming:
		query = replaceWordsByStem(query)
	
	queryWithScore = createTokensWithScore(query)
	
	if embedding:
		for i in range(0, len(query)):
			synonyms = findSynonyms(embeddingModel, query[i], nbOfSynonyms)
			for newWord in synonyms:
				queryWithScore.append((newWord[0],1))
	queryWithScore = deleteDuplicatesInQuery(queryWithScore)
	print(queryWithScore)
	return queryWithScore

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