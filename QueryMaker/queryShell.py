import sys
import gensim 
import gensim.downloader as api
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma

def launchShell(searchAlgorithm, documentServer, wordEmbedding = False, documentsForEmbedding = []):
	if wordEmbedding:
		model = trainModelForEmbedding(documentsForEmbedding)
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
					lemmatization = True,
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

def processQueryString(query, stemming = False, lemmatization = False, embedding = False, embeddingModel = None, nbOfSynonyms = 0):
	query = createListOfTokens(query)

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

def trainModelForEmbedding(listOfDocuments):
	model = gensim.models.Word2Vec(
		listOfDocuments,
		size = 50,
		window = 10,
		min_count = 5,
		workers = 10,
		iter = 5
	)
	model = model.wv
	model = api.load("glove-wiki-gigaword-100")
	return model

def findSynonyms(model, myWord, nbOfSynonyms):
	try:
		synonyms = model.most_similar (positive=myWord, topn=nbOfSynonyms) 
	except:
		print(myWord, 'is not in the vocabulary')
		synonyms = []
	return synonyms