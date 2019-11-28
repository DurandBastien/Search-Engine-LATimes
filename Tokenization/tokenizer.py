#!/usr/bin/env python
# coding: utf-8


import os
import re
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

class Tokenizer:
    def __init__(self, listfile):
        self.listfile = os.listdir(listfile)
        self.path = listfile
        print("Tokenizer successfully created")

    def readFile(self, file):
        """
        read certain file whose name specified in the para
        args:
            file: name of the file to read
        """
        # print("reading ", file)


        f = open(self.path + "/" + file, "r")
        content = f.readlines()
        # print(content)
        f.close()
        return content

       

    def extractDocumentFromFile(self, content, indexFile):
        """
        extract the info of docID and Paragraph of next document.
        call iteratively to extract the info of all docs
        args:
            content: the content of the whole file
            indexFile: where we want to begin the document analysis
            
        return:
            docid: the id of the doc extracted from file
            paragraph: the content extracted from file
            i : the index the next iteration will begin
           
        """
        #print("document extraction, index ", indexFile)
        try:
            if content == None:
                raise ValueError("file content empty!")

            nbDocId = 0
            paragraph = ""
            docid = ""
            i = -1 
            docIndexInFile = -1           
            for i in range(indexFile, len(content)):
                if "DOCID" in content[i]:
                    
                    nbDocId = nbDocId + 1
                    if nbDocId == 2:
                        break
                    content[i] = (
                        content[i].replace("<DOCID> ", "").replace(" </DOCID>", "").strip()
                    )
                    docid = content[i]
                    docIndexInFile = i
                elif "<P>" in content[i]:
                    i = i + 1
                    while "</P>" not in content[i]:
                        if i + 1 >= len(content):
                            break
                        else:
                            paragraph = paragraph + content[i]
                            i = i + 1
                    
            if nbDocId == 0:
                i = len(content)
            return docid, paragraph, docIndexInFile, i

        except ValueError:
            return 0, 0, -1    
    
def removeStopWords(tokens):
    """
    remove stop words
    args:
        paragraph: the para that we remove stop words
    """
    
    listStopWords = [ "ourselves", "hers", "between", "yourself", 
                        "but", "again", "there", "about", "once", "during", 
                        "out", "very", "having", "with", "they", "own", "an",
                        "be", "some", "for", "do", "its", "yours", "such", "into",
                        "of", "most", "itself", "other", "off", "is", "s", "am",
                        "or", "who", "as", "from", "him", "each", "the", "themselves", 
                        "until", "below", "are", "we", "these", "your", "his", "through", 
                        "don", "nor", "me", "were", "her", "more", "himself", "this", "down",
                        "should", "our", "their", "while", "above", "both", "up", "to",
                        "ours", "had", "she", "all", "no", "when", "at", "any", "before",
                        "them", "same", "and", "been", "have", "in", "will", "on", "does",
                        "yourselves", "then", "that", "because", "what", "over", "why", "so",
                        "can", "did", "not", "now", "under", "he", "you", "herself", "has",
                        "just", "where", "too", "only", "myself", "which", "those", "i",
                        "after", "few", "whom", "t", "being", "if", "theirs", "my", "against",
                        "a", "by", "doing", "it", "how", "further", "was", "here", "than" ]
    for word in listStopWords:

        # remove the stop word in the tokens
        tokens = [value for value in tokens if value != word]
    
    return tokens
    
def replaceWordsByStem(tokens):
    stemmer = PorterStemmer()
    stemTokens = [stemmer.stem(token) for token in tokens]
    return stemTokens

def replaceWordsByLemma(tokens):
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(tokens)):
        #Extract the type of word to find the correct lemma
        tag = nltk.pos_tag([tokens[i]])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        POS = tag_dict.get(tag, wordnet.NOUN)
        #Replace the word by its lemma
        tokens[i] = lemmatizer.lemmatize(tokens[i], POS)
    return tokens  

def createListOfTokens(paragraph):
        """
        clean the document content by removing punctuation.
        create the list of tokens.
        args:
            paragraph: the content of a specific document
           
        """
        paragraph = paragraph.lower()
        #remove punctuation
        paragraph = paragraph.replace("\n","")
        paragraph = paragraph.replace(";","").replace(",","").replace("\"","")
        paragraph = paragraph.replace("/", "").replace("(", "").replace(")", "").replace("\\","")
        
            
        #create tokens using space character as separator
        tokens = paragraph.split(" ")
        while "" in tokens:
            tokens.remove("")
        
        return tokens

def lookForSynonymes(listOfText):
    model = Word2Vec(listOfText, min_count=5, size=50, workers=3, window=3, sg=1)
    print(model)

if __name__ == "__main__":
    t = Tokenizer("../../latimes-sous-partie")

    for file in t.listfile:
        print("curremt file name:", file)
        content = t.readFile(file)
        index = 0
        while index != len(content):
            mydoc= t.extractDocumentFromFile(content,index)
            index = mydoc[3]
            tokens = t.createListOfTokens(mydoc[1])
            print("before removing stop words:",len(tokens))
            tokens = t.removeStopWords(tokens)
            print(len(tokens))
