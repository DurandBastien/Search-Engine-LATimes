import Globals.globals as glob
import re

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
			content = file.read(docIDinfo[2] - docIDinfo[1])
			docContent[docID] = {"content":content, "metadata":parseMetadata(docID, content)}

	return docContent

def parseMetadata(docID, docContent):
	meta = ""
	meta += "DOCID : " + docID + "\n\n"
	meta += "DATE : "
	meta += re.search(r'(?s)<DATE>[\r\n]<P>[\r\n](.*)</P>[\r\n]</DATE>', docContent).group(1) + "\n"
	meta += "SECTION : "
	meta += re.search(r'(?s)<SECTION>[\r\n]<P>[\r\n](.*)</P>[\r\n]</SECTION>', docContent).group(1) + "\n"
	meta += "HEADLINE : "
	meta += re.search(r'(?s)<HEADLINE>[\r\n]<P>[\r\n](.*)</P>[\r\n]</HEADLINE>', docContent).group(1)

	return meta
	
