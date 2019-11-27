import sys
import pickle


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

	ifConstructor.constructIF(tokenizer_, stemming = False, lemmatization = True, wordEmbedding = True)

	# print(glob.invertedFile)

	documentServer.foldername = datasetFoldername
	algorithm = searchAlgorithms.naiveAlgo

	queryShell.launchShell(algorithm, documentServer,applyStemming = False, applyLemmatization = True, wordEmbedding = True, documentsForEmbedding = embeddingDataset)



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

		datasetFoldername = "../latimes"

		# datasetFoldername = "/home/bastien/Documents/latimes"
		
		#TO DELETE WHEN MODEL WILL BE CHARGED IN MEMORY
		#tokenizer_ = tokenizer.Tokenizer(datasetFoldername)
		#ifConstructor.constructIF(tokenizer_, stemming = False, lemmatization = True, wordEmbedding = True)
		
		embeddingFile = open('./Globals/embeddingDataset', 'rb')
		embeddingDataset = pickle.load(embeddingFile)
		embeddingFile.close()

		constructIF = False
		
		if(constructIF):
			tokenizer_ = tokenizerCpp.Tokenizer(datasetFoldername)
			#set runSize such that :
			#the total number of documents in the dataset divided by runSize is less than the allowed number of simultaneously opened files on your machine (usually 1024) 
			ifConstructor.constructIF_diskBased(tokenizer_, runSize = 150)
			#AJOUTER GENERATION EMBEDDING DATASET DANS constructIF_diskBased
			glob.trainModelForEmbedding(embeddingDataset)

		diskBasedIF = True

		if(diskBasedIF):
			glob.loadVocabulary()
			glob.loadDocID2Content()
		
		
		documentServer.foldername = datasetFoldername

		algorithm = searchAlgorithms.threshold

		queryShell.launchShell(algorithm, documentServer, applyStemming = False, applyLemmatization = True, wordEmbedding = True, documentsForEmbedding = embeddingDataset)

	elif(argv[1] == "test"):
		test()
	else:
		print("unknown arg")
