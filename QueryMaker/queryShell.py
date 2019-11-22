import sys
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma

def launchShell(searchAlgorithm, documentServer):
	while 1:
		print("\nEnter \'quit()\' to exit")
		print("Enter search query:")
		query = sys.stdin.readline()
		print("quit()" not in query)
		if "quit()" not in query:
			processedQuery = processQueryString(query, lemmatization = True)
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
					print(returnedDocuments[chosenDocId.strip("\n")],"\n")
			else:
				print("no result\n")
		else:
			break

def processQueryString(query, stemming = False, lemmatization = False):
	query = createListOfTokens(query)
	if lemmatization:
		query = replaceWordsByLemma(query)
	elif stemming:
		query = replaceWordsByStem(query)
	print(query)
	return query

def processReturnedDocuments(returnedDocuments):
	return returnedDocuments.keys()

	