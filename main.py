from IFConstruction import ifConstructor
from Tokenization import tokenizer
from Tokenization.TokenizationCpp import tokenizer as tokenizerCpp
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell
import Globals.globals as glob
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f
from collections import OrderedDict 


if __name__ == "__main__":
	datasetFoldername = "/home/bastien/Documents/test_latimes/"
	# tokenizer = tokenizer.Tokenizer(datasetFoldername)
	# ifConstructor.constructIF(tokenizer)
	# tokenizer = tokenizerCpp.Tokenizer(datasetFoldername)
	# ifConstructor.constructIFFromStreamTokenizer(tokenizer)
	# ifConstructor.constructIF_diskBased(tokenizer, runSize = 150)
	# glob.init()
	glob.loadVocabulary()
	glob.loadDocID2Content()
	ordDict = eval(glob.voc2PostingList("worse"))[1]
	print(ordDict)
	documentServer.foldername = datasetFoldername
	print(ordDict.keys())
	print(documentServer.serveDocuments([["156304", 2]]))
	# print(IF["chernobyl"])
	# searchAlgorithms.naiveAlgo("chernobyl")
	# documentServer.foldername = datasetFoldername
	# queryShell.launchShell(searchAlgorithms.naiveAlgo, documentServer)