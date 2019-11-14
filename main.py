from IFConstruction import ifConstructor
from Tokenization import tokenizer
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell

if __name__ == "__main__":
	datasetFoldername = "/home/bastien/Documents/latimes"
	tokenizer = tokenizer.Tokenizer(datasetFoldername)
	ifConstructor.constructIF(tokenizer)
	# queryShell.launchShell(searchAlgorithms.naiveAlgo, documentServer)
