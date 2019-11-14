import sys


def launchShell(searchAlgorithm, documentServer):
	while 1:
		print("\n")
		print("Enter search query:")
		query = sys.stdin.readline()
		processedQuery = processQueryString(query)
		queryResult = searchAlgorithm(processedQuery)
		returnedDocuments = documentServer.serveDocuments(queryResult)
		metadata = processReturnedDocuments(returnedDocuments)
		print("\n")
		print("result:")
		print("\n")
		print(metadata)
		print("\n")
		if(returnedDocuments):
			print("choose docID")
			chosenDocId = sys.stdin.readline()
			print("\n")
			print(returnedDocuments[chosenDocId])
			print("\n")

def processQueryString(query):
	return query

def processReturnedDocuments(returnedDocuments):
	return "metadata"
	