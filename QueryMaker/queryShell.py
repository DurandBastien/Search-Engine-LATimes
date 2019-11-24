import sys
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma

#launch a shell to make queries answered with the given search algorithm and document server
def launchShell(searchAlgorithm, documentServer):
	while 1:
		print("\nEnter \'quit()\' to exit")
		print("Enter search query:")
		query = sys.stdin.readline()
		if "quit()" not in query:
			processedQuery = processQueryString(query, lemmatization = False)
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

	