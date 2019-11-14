from IFConstruction import ifConstructor
from Tokenization import tokenizer
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell

if __name__ == "__main__":
	datasetFoldername = "../Documents/latimes"
	tokenizer = tokenization.tokenizer(datasetFoldername)
	initIF.constructIF(tokenizer)
	queryShell.launchShell(rankedQueries.naiveAlgo, documentServer)
