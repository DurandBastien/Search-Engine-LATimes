try:
    from Tokenization.TokenizationCpp import cTokenizer
    # import cTokenizer
except:
    strErr = "\n\n cTokenizer module not found, "
    strErr += "run `$ make tokenizer_py_module`! \n"
    raise RuntimeError(strErr)

class Tokenizer():

    def __init__(self, foldername):

        # Construct the Tokenizer object and store a Python capsule with
        # a C++ pointer to the object
                
        self.tokenizerCapsule = cTokenizer.construct(foldername)

    def getNextDocAsTokens(self):
        """
        Python wrapper for Tokenizer::get_nextTokens
        """
        return cTokenizer.getNextDocAsTokens(self.tokenizerCapsule)

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
