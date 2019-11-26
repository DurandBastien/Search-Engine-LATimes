import sys


from IFConstruction import ifConstructor
import Globals.globals as glob
from DocumentServer import documentServer
from SearchAlgorithms import searchAlgorithms
from QueryMaker import queryShell

from Tokenization import tokenizer


#Here try out whatever you want
def test():
	datasetFoldername = "../latimesTest"

	tokenizer_ = tokenizer.Tokenizer(datasetFoldername)

	documents = ifConstructor.constructIF(tokenizer_, stemming = False, lemmatization = True, wordEmbedding = True)

	# print(glob.invertedFile)

	documentServer.foldername = datasetFoldername
	algorithm = searchAlgorithms.naiveAlgo

	queryShell.launchShell(algorithm, documentServer,applyStemming = False, applyLemmatization = True, wordEmbedding = True, documentsForEmbedding = documents)


	'''#Test Lemma et Stem :
	test = ['cats','words','be','is', 'caring', 'feet', 'unacceptable', 'realized']
	print(test)
	print(tokenizer.replaceWordsByStem(test))
	print(tokenizer.replaceWordsByLemma(test))'''


if __name__ == "__main__":

	argv = sys.argv

	#default behavior = up to date solution
	if(len(argv) <= 1):

		datasetFoldername = "../latimes"

		# datasetFoldername = "/home/bastien/Documents/latimes"
		
		#TO DELETE WHEN MODEL WILL BE CHARGED IN MEMORY
		tokenizer_ = tokenizer.Tokenizer(datasetFoldername)
		documents = ifConstructor.constructIF(tokenizer_, stemming = False, lemmatization = True, wordEmbedding = True)

		constructIF = False
		
		if(constructIF):
			tokenizer_ = tokenizerCpp.Tokenizer(datasetFoldername)
			#set runSize such that :
			#the total number of documents in the dataset divided by runSize is less than the allowed number of simultaneously opened files on your machine (usually 1024) 
			ifConstructor.constructIF_diskBased(tokenizer_, runSize = 150)  
		
		diskBasedIF = True

		if(diskBasedIF):
			glob.loadVocabulary()
			glob.loadDocID2Content()
		
		
		documentServer.foldername = datasetFoldername

		algorithm = searchAlgorithms.threshold

		queryShell.launchShell(algorithm, documentServer, applyStemming = False, applyLemmatization = True, wordEmbedding = True, documentsForEmbedding = documents)

	elif(argv[1] == "test"):
		test()
	else:
		print("unknown arg")


