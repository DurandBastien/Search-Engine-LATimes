try:
    import cTokenizer
except:
    strErr = "\n\n cTokenizer module not found, "
    strErr += "run `$ make tokenizer_py_module`! \n"
    raise RuntimeError(strErr)

class Tokenizer():

    def __init__(self, foldername):

        # Construct the Tokenizer object and store a Python capsule with
        # a C++ pointer to the object
                
        self.tokenizerCapsule = cTokenizer.construct(foldername)

    def getNextTokens(self):
        """
        Python wrapper for Tokenizer::get_nextTokens
        """
        cTokenizer.getNextTokens(self.tokenizerCapsule)

    def __delete__(self):
        cTokenizer.delete_object(self.tokenizerCapsule)