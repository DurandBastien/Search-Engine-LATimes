from IFConstruction import ifConstructor
from Tokenization import tokenizer
#from Tokenization.TokenizationCpp import tokenizer as tokenizerCpp
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f

if __name__ == "__main__":

	datasetFoldername = "../latimesTest"
	#datasetFoldername = "/home/bastien/Documents/latimes/"
	tokenizer = tokenizer.Tokenizer(datasetFoldername)

	'''#Test Lemma et Stem :
	test = ['cats','words','be','is', 'caring', 'feet', 'unacceptable', 'realized']
	print(test)
	print(tokenizer.replaceWordsByStem(test))
	print(tokenizer.replaceWordsByLemma(test))'''

	ifConstructor.constructIF(tokenizer)
	#tokenizer = tokenizerCpp.Tokenizer(datasetFoldername)
	#ifConstructor.constructIFFromStreamTokenizer(tokenizer)
	# print(IF["chernobyl"])
	# searchAlgorithms.naiveAlgo("chernobyl")
	documentServer.foldername = datasetFoldername
	queryShell.launchShell(searchAlgorithms.naiveAlgo, documentServer)
