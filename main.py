import sys
import pickle
#import os.path
#from os import path


from IFConstruction import ifConstructor
import Globals.globals as glob
from DocumentServer import documentServer
from SearchAlgorithms import searchAlgorithms
from QueryMaker import queryShell

from Tokenization import tokenizer
from Tokenization.TokenizationCpp import tokenizer as tokenizerCpp


#Here try out whatever you want
def test1():
	datasetFoldername = "../../latimes/latimes"

	tokenizer_ = tokenizer.Tokenizer(datasetFoldername)

	ifConstructor.constructIF(tokenizer_, stemming = False, lemmatization = True, wordEmbedding = True)

	# print(glob.invertedFile)

	documentServer.foldername = datasetFoldername
	algorithm = searchAlgorithms.naiveAlgo

	queryShell.launchShell(algorithm, documentServer,applyStemming = False, applyLemmatization = True, wordEmbedding = True)

def test2():
	print(tokenizer.replaceWordsByLemma(['jumped', 'jumping', 'are', 'is', 'message']))
	# glob.loadVocabulary()
	# print(glob.vocList2PostingLists(["zzz"]))
	# algo = searchAlgorithms.naiveAlgo
	# print(algo([("january", 3)]))

if __name__ == "__main__":

	''' 
	ATTENTION : regénérer word embedding model sur l'intégralité du dataset
	Nettoyer code
	Intégrer génération embedding model lorsqu'on regénère l'IF avec les
	options stemming et lematization appropriées
	'''

	argv = sys.argv

	#default behavior = up to date solution
	if(len(argv) <= 1):

		# datasetFoldername = "../latimes"
		# datasetFoldername = "../latimesTest"
		datasetFoldername = "/home/bastien/Documents/latimes"

		constructIF = True

		if(constructIF):
			tokenizer_ = tokenizerCpp.Tokenizer(datasetFoldername, lemmatization_ = False, stemming_ = False)
			#set runSize such that :
			#the total number of documents in the dataset divided by runSize is less than the allowed number of simultaneously opened files on your machine (usually 1024) 
			ifConstructor.constructIF_diskBased(tokenizer_, runSize = 1000, score_tf_idf = True)
			# glob.loadEmbeddingDataset()
			# glob.trainModelForEmbedding(glob.embeddingDataset)

		diskBasedIF = True

		if(diskBasedIF):
			glob.loadVocabulary()
			glob.loadDocID2Content()

		documentServer.foldername = datasetFoldername

		algorithm = searchAlgorithms.faginAlgo

		queryShell.launchShell(algorithm, documentServer, applyStemming = False, applyLemmatization = True, wordEmbedding = True)

	elif(argv[1] == "test"):
		# test1()
		test2()
	else:
		print("unknown arg")
