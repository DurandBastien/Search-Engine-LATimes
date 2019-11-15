from IFConstruction import ifConstructor
from Tokenization import tokenizer
from SearchAlgorithms import searchAlgorithms
from DocumentServer import documentServer
from QueryMaker import queryShell
from Globals.globals import invertedFile as IF

if __name__ == "__main__":
	datasetFoldername = "../../latimes/latimes"
	tokenizer = tokenizer.Tokenizer(datasetFoldername)
	ifConstructor.constructIF(tokenizer)
	print(IF)
	# queryShell.launchShell(searchAlgorithms.naiveAlgo, documentServer)
