import Globals.globals as glob

foldername = ""

#use global docID2ContentIndexes to fetch on disk content of documents with id given 
def serveDocuments(docIDList):
	docContent = {}
	for docID in docIDList:
		docContent[docID] = None
		if(docID in glob.docID2ContentIndexes):
			docIDinfo = glob.docID2ContentIndexes[docID]
			file = open(foldername+"/"+docIDinfo[0], "r")
			file.seek(docIDinfo[1])
			docContent[docID] = file.read(docIDinfo[2] - docIDinfo[1])

	return docContent


