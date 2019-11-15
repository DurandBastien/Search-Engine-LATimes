from IFConstruction import ifConstructor
from Tokenization import tokenizer
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f

if __name__ == "__main__":
	datasetFoldername = "/home/bastien/Documents/latimes"
	tokenizer = tokenizer.Tokenizer(datasetFoldername)
	ifConstructor.constructIF(tokenizer)

	# print(IF["chernobyl"])
	# searchAlgorithms.naiveAlgo("chernobyl")
	documentServer.foldername = datasetFoldername
	queryShell.launchShell(searchAlgorithms.naiveAlgo, documentServer)
