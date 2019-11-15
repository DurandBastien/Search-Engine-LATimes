import sys


def launchShell(searchAlgorithm, documentServer):
	while 1:
		print("\n")
		print("Enter search query:")
		query = sys.stdin.readline()
		processedQuery = processQueryString(query)
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
				print(returnedDocuments[chosenDocId],"\n")
		else:
			print("no result\n")

def processQueryString(query):
	return query

def processReturnedDocuments(returnedDocuments):
	return returnedDocuments

	