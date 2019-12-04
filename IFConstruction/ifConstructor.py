import math
import ast
import os
from collections import OrderedDict 
import Globals.globals as glob
from Tokenization.tokenizer import createListOfTokens, replaceWordsByStem, replaceWordsByLemma, removeStopWords
import pickle

def constructIF(tokenizer, stemming = False, lemmatization = False, wordEmbedding = False):
    global countDoc
    countDoc = 0
    documentsForEmbedding = []

    for file in tokenizer.listfile:
        content = tokenizer.readFile(file)
        index = 0
        while index != len(content):
            mydoc= tokenizer.extractDocumentFromFile(content,index)

            countDoc = countDoc + 1
            glob.docID2ContentIndexes[mydoc[0]] = [file, mydoc[2], mydoc[3]]
            docId = mydoc[0]
            index = mydoc[3]
            tokens = createListOfTokens(mydoc[1])
            tokens = removeStopWords(tokens)
            if lemmatization:
                tokens = replaceWordsByLemma(tokens)
            elif stemming:
                tokens = replaceWordsByStem(tokens)

            if wordEmbedding and index != len(content):
                documentsForEmbedding.append(tokens)


            for word in tokens:
                if (word in glob.invertedFile):
                    if (docId in glob.invertedFile[word]):
                        glob.invertedFile[word][docId] += 1
                    else:
                        glob.invertedFile[word][docId] = 1
                else:
                    glob.invertedFile[word] = {docId: 1}
        # print(file, len(glob.invertedFile)) 

    # Write in memory the dataset for wordEmbedding
    embeddingFile = open('./Globals/embeddingDataset', 'wb')
    pickle.dump(documentsForEmbedding, embeddingFile)
    embeddingFile.close()
    print("The dataset for word embedding has been stored in memory.")

#in-memory inverted file construction using a stream-like tokenizer
def constructIFFromStreamTokenizer(streamTokenizer):
    docFromStream = streamTokenizer.getNextDocAsTokens()
    while(docFromStream):
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
        glob.docID2ContentIndexes[docID] = [filename, docIndexStart, docIndexEnd]
        for word in tokens.split():
            if (word in glob.invertedFile):
                if (docID in glob.invertedFile[word]):
                    glob.invertedFile[word][docID] += 1
                else:
                    glob.invertedFile[word][docID] = 1
            else:
                glob.invertedFile[word] = {docID: 1}
        docFromStream = streamTokenizer.getNextDocAsTokens()

#disk based inverted file construction using a stream-like tokenizer
#runSize is the number of documents processed in one run
#pre-condition : runSize > (document number)/(allowed number of files open on machine)
def constructIF_diskBased(streamTokenizer, runSize = 1, buildDocId2Content = False, score_tf_idf = True):
    print(">","disk-based inverted file construction with a run size of:", runSize)
    datasetToSortedRuns(streamTokenizer, runSize, buildDocId2Content)
    mergeRunsToIF(score_tf_idf)
    print(">","Inverted file successfully written on disk")

#write result from each runs on different temporary files 
def datasetToSortedRuns(streamTokenizer, runSize, buildDocId2Content):
    print(">","start parsing dataset in triples (word, docID, number of occurence)")
    print(">","rm IFConstruction/tmp/*")
    os.system("rm IFConstruction/tmp/*")

    embDatasetFilename = "Globals/embeddingDataset"
    open(embDatasetFilename, "w").close()
    docID2ContentFilename = "Globals/docID2ContentIndexes.dict"
    tempfile = "IFConstruction/tmp/file_"
    tempfileCounter = 0 

    runCounter = 0 #count number of document processed in current run
    docFromStream = streamTokenizer.getNextDocAsTokens()
    runTriples = [] #store triples (word, docID, number of occurence) for a whole run before flushing on disk in temporary file 
    docID2Content = {} #in-memory construction before flushing on disk, see Globals.globals.docID2ContentIndexes

    with open(embDatasetFilename, "a+") as embDatasetFile:
        while(docFromStream):
            print(">", int(glob.numberOfDocuments*100/131897), "%", "Doc number :",glob.numberOfDocuments, end="\r")

            #parse result from tokenizer
            glob.numberOfDocuments += 1 #count number of document processed from beginning
            filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
            embDatasetFile.write(str(tokens.split())+"\n")

            if(buildDocId2Content):
                docID2Content[docID] = [filename, docIndexStart, docIndexEnd]

            #check if end of run reached 
            if(runCounter < runSize):
                #build inverted file for the current document
                docWiseDict = {} 
                for word in tokens.split():
                    if (word in docWiseDict):
                        docWiseDict[word] += 1
                    else:
                        docWiseDict[word] = 1
                #unroll doc-wise inverted file in triples and add to list 
                for word in docWiseDict:
                    runTriples.append([word, docID, docWiseDict[word]])
                runCounter += 1
            #end of run reached     
            else:
                #alphabetical then docID sorting in order to make merging easier later
                runTriples.sort()
                #flush sorted runTriples
                tempfileCounter += 1
                with open(tempfile+str(tempfileCounter), "w") as file:
                    file.write(run_ToString(runTriples))

                runTriples = []
                runCounter = 0

            docFromStream = streamTokenizer.getNextDocAsTokens()

    #last run probably uncomplete
    if(runTriples[0]):
        runTriples.sort()
        #flush sorted runTriples
        tempfileCounter += 1
        with open(tempfile+str(tempfileCounter), "w") as file:
            file.write(run_ToString(runTriples))

    #flush docID2Content for further system initializations, see Globals
    if(buildDocId2Content):
        docID2Content_file = open(docID2ContentFilename, "w")
        docID2Content_file.write(str(docID2Content))
        docID2Content_file.close()

    print(int(glob.numberOfDocuments*100/131897), "%", "Doc number :",glob.numberOfDocuments)

#merge all temporary files containing run triples (see above) in an on-disk inverted files 
def mergeRunsToIF(score_tf_idf):
    print(">","start merging runs' results")
    IFname = "Globals/IF.dict"
    vocabularyFilename = "Globals/vocabulary.dict"

    #list and open temp files
    tmpFoldername = "IFConstruction/tmp/"
    listfile = os.listdir(tmpFoldername)
    
    openedFiles = [open(tmpFoldername+filename, "r") for filename in listfile]

    print(">", len(openedFiles), "temporary files opened")

    #a sorted stack-like list is used to know which temp file has to be read
    #a stack element consists in a line read and parsed in a triple plus the temp file ID
    #stack initialized with guardian
    currentEntriesInFiles = [None]

    #read first line of each temp file
    for i, file in enumerate(openedFiles):
        entry = file.readline()
        if(entry != "" or entry != "\n"):
            #parse triple
            entry_eval = ast.literal_eval(entry)
            currentEntriesInFiles.append([entry_eval[0], entry_eval[1], entry_eval[2], i])
    #the stack is sorted so it wil pop the right entry 
    currentEntriesInFiles[1:] = sorted(currentEntriesInFiles[1:], reverse=True)

    #erase file
    open(IFname, "w").close()
    
    #the vocabulary list is build in-memory before flushing on disk for further system initializations, see Globals
    vocList = {}
    with open(IFname, "a+") as IF_file:
        wordCounter = 0
        current_entry = currentEntriesInFiles.pop()
        #while there's still a temp file to read
        while(len(currentEntriesInFiles) > 0):
            current_word = current_entry[0]
            posting_list = []
            print(">", "Word processed :",wordCounter, end="\r")

            #check if guardian showing up, if not then check if a new word showed up from the stack
            while(current_entry != None and current_word == current_entry[0]):
                posting_list.append([current_entry[1], current_entry[2]])

                #read temp file poped from stack
                entry = openedFiles[current_entry[3]].readline()
                if(entry != "" and entry != "\n"):
                    #parse triple
                    entry_eval = ast.literal_eval(entry)
                    currentEntriesInFiles.append([entry_eval[0], entry_eval[1], entry_eval[2], current_entry[3]])
                #the stack is sorted so it wil pop the right entry 
                currentEntriesInFiles[1:] = sorted(currentEntriesInFiles[1:], reverse=True)
                current_entry = currentEntriesInFiles.pop()

            wordCounter += 1
            #every new word update voc list 
            vocList[current_word] = IF_file.tell()

            # compute score = tf * idf
            if(score_tf_idf):
                for j in range(len(posting_list)):
                    tf = 1 + math.log(posting_list[j][1])
                    idf = math.log(glob.numberOfDocuments/(len(posting_list))) #note that a posting list is never empty
                    posting_list[j][1] = round(tf * idf, 3)

            #sort posting list by decreasing number of occurrence
            posting_list.sort(key=lambda x:x[1], reverse = True)
            #then create ordered dict from the sorted posting list
            posting_list_dict = OrderedDict({ i : j for i,j in posting_list })
            #flush word and posting list on disk
            IF_file.write(str([current_word, posting_list_dict])+"\n")

        print(">", "Word processed :",wordCounter)

    #flush voc list on disk for further inializations, see Globals
    vocab_file = open(vocabularyFilename, "w")
    vocab_file.write(str(vocList))
    vocab_file.close()


def run_ToString(run):
    run_str = ""
    for entry in run:
        run_str += str(entry) 
        run_str += "\n"
    run_str += "\n"
    return run_str

def giveScores(nbOfOccurence):
    """
    calculate and replace the occurence of word in the doc with score

    """
    for word in IF:
        for docId in IF[word]:
            IF[word][docId] = (1 + math.log(IF[word][docId])) * math.log(countDoc / (1 + len(IF[word])))
    print(countDoc)  #132626 docs for whole directory


if __name__ == "__main__":
    constructIF()
    print(IF)
