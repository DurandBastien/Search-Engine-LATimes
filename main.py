import sys

from IFConstruction import ifConstructor
import Globals.globals as glob
from DocumentServer import documentServer
from SearchAlgorithms import searchAlgorithms
from QueryMaker import queryShell
from Tokenization.TokenizationCpp import tokenizer as tokenizerCpp

from QueryMaker.queryShell import processQueryString

def applyFaginOnQuery(processedQuery):
    queryResult = searchAlgorithms.faginAlgo(processedQuery)
    if(queryResult):
        returnedDocuments = documentServer.serveDocuments(queryResult)
        print("\n")
        print("results:\n")
        for idx, doc in enumerate(returnedDocuments.keys()):
            print(idx+1,"----------------------------------")
            print(returnedDocuments[doc]["metadata"]),
            print("----------------------------------")
            '''if(returnedDocuments):
                print("choose docID")
                chosenDocId = sys.stdin.readline()
                print("\n")
                if(chosenDocId.strip() in returnedDocuments):
                    print(returnedDocuments[chosenDocId.strip()]["content"],"\n")
                else:
                    print("doc ID not in result")'''
    else:
        print("no result\n")

if __name__ == "__main__":

	'''argv = sys.argv

	#default behavior = up to date solution
	if(len(argv) <= 1):

		datasetFoldername = "../../latimes/latimes" # CHANGE HERE THE PATH DATASET

		vocabulary_filename = "Globals/IF_files/vocabulary.dict"
		IF_filename = "Globals/IF_files/IF_stemm_lemm_tfidf.dict"

		constructIF = False
		trainWordEmbModel = False

		if(constructIF):
			tokenizer_ = tokenizerCpp.Tokenizer(datasetFoldername, lemmatization_ = False, stemming_ = True)
			#set runSize such that :
			#the total number of documents in the dataset divided by runSize is less than the allowed number of simultaneously opened files on your machine (usually 1024) 
			ifConstructor.constructIF_diskBased(tokenizer_, runSize = 10000, score_tf_idf = True)
			if(trainWordEmbModel):
				glob.loadEmbeddingDataset()
				glob.trainModelForEmbedding(glob.embeddingDataset)

		diskBasedIF = True

		if(diskBasedIF):
			glob.loadVocabulary(vocabulary_filename, IF_filename)
			glob.loadDocID2Content()

		documentServer.foldername = datasetFoldername

		algorithm = searchAlgorithms.faginAlgo

		queryShell.launchShell(algorithm, documentServer, applyStemming = False, applyLemmatization = True, wordEmbedding = True)

	else:
		print("unknown arg")'''

	glob.loadVocabulary("./Globals/stemm_nolemm_tfidf/vocabulary.dict","./Globals/stemm_nolemm_tfidf/IF.dict")

	query = "Chocolate and feet"

	# Apply stemming on the query
	processedQuery = processQueryString(query,stemming = True)
	print(processedQuery)
	# Apply fagin algorithm
	applyFaginOnQuery(processedQuery)
