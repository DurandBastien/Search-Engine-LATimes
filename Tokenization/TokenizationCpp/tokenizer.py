from Tokenization.tokenizer import replaceWordsByLemma
from Tokenization.tokenizer import replaceWordsByStem

try:
    from Tokenization.TokenizationCpp import cTokenizer
    # import cTokenizer
except:
    strErr = "\n\n cTokenizer module not found, "
    strErr += "run `$ make tokenizer_py_module`! \n"
    # raise RuntimeError(strErr)

class Tokenizer():

    def __init__(self, foldername, lemmatization_ = False, stemming_ = False):

        # Construct the Tokenizer object and store a Python capsule with
        # a C++ pointer to the object
                
        self.tokenizerCapsule = cTokenizer.construct(foldername)
        self.lemmatization = lemmatization_
        self.stemming = stemming_

    def getNextDocAsTokens(self):
        """
        Python wrapper for Tokenizer::get_nextTokens
        """
        res = cTokenizer.getNextDocAsTokens(self.tokenizerCapsule)
        if(res == None):
            return res
        if(self.stemming):
            res = list(res)
            lemm_words = replaceWordsByStem(res[2].split())
            res[2] = " ".join(lemm_words)
            return res
        elif(self.lemmatization):
            res = list(res)
            lemm_words = replaceWordsByLemma(res[2].split())
            res[2] = " ".join(lemm_words)
            return res
        else:
            return res

    def __delete__(self):
        cTokenizer.delete_object(self.tokenizerCapsule)


if __name__ == "__main__":
    tok = Tokenizer("/home/bastien/Documents/latimes/")
    result = []
    # file = ""
    # counter = 0
    result = tok.getNextDocAsTokens()
    # while(result is not None):
    #     if(result[0] != file):
    #         file = result[0]
    #         counter+=1
    #     result = tok.getNextTokens()

    print(result)
