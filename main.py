from IFConstruction import ifConstructor
from Tokenization import tokenizer



if __name__ == "__main__":

	datasetFoldername = "../latimes"
	tokenizer = tokenizer.Tokenizer(datasetFoldername)
	ifConstructor.constructIF(tokenizer)

	ifConstructor.giveScores()
	# print(IF["narrowed"])