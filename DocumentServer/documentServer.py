import sys
sys.path.append('../')
from Globals.globals import docID2filename as d2f

foldername = ""

def serveDocuments(docIDList):
	docContent = {}
	for docID in docIDList:
		docContent[docID] = None
		if(docID in d2f):
			docIDinfo = d2f[docID]
			file = open(foldername+"/"+docIDinfo[0], "r")
			file.seek(docIDinfo[1])
			docContent[docID] = file.read(docIDinfo[2] - docIDinfo[1])

	return docContent

if __name__ == "__main__":
	foldername = "/home/bastien/Documents/latimes/"
	d2f["LA010189-0001"] = ["la010189", 3, 50]
	returnedDocument = serveDocuments(["LA010189-0001"])
	print(returnedDocument["LA010189-0001"])


