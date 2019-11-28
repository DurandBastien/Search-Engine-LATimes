#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""
import math;
import ast;
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
        print(file, len(glob.invertedFile)) 

    # Write in memory the dataset for wordEmbedding
    embeddingFile = open('./Globals/embeddingDataset', 'wb')
    pickle.dump(documentsForEmbedding, embeddingFile)
    embeddingFile.close()
    print("The dataset for word embedding has been stored in memory.")

    # return documentsForEmbedding

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
def constructIF_diskBased(streamTokenizer, runSize = 1):
    print(">","disk-based inverted file construction with a run size of:", runSize)
    datasetToSortedRuns(streamTokenizer, runSize)
    mergeRunsToIF()
    print(">","Inverted file successfully written on disk")

#write result from each runs on different temporary files 
def datasetToSortedRuns(streamTokenizer, runSize):
    print(">","start parsing dataset in triples (word, docID, number of occurence)")
    print(">","rm IFConstruction/tmp/*")
    os.system("rm IFConstruction/tmp/*")

    docID2ContentFilename = "Globals/docID2ContentIndexes.dict"
    tempfile = "IFConstruction/tmp/file_"
    tempfileCounter = 0 

    runCounter = 0 #count number of document processed in current run
    docFromStream = streamTokenizer.getNextDocAsTokens()
    runTriples = [] #store triples (word, docID, number of occurence) for a whole run before flushing on disk in temporary file 
    docID2Content = {} #in-memory construction before flushing on disk, see Globals.globals.docID2ContentIndexes
    while(docFromStream):
        # print(">", int(glob.numberOfDocuments*100/131897), "%", "Doc number :",glob.numberOfDocuments, end="\r")
        print(">", "Doc number :",glob.numberOfDocuments, end="\r")

        #parse result from tokenizer
        glob.numberOfDocuments += 1 #count number of document processed from beginning
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
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
    docID2Content_file = open(docID2ContentFilename, "w")
    docID2Content_file.write(str(docID2Content))
    docID2Content_file.close()

    # print(int(glob.numberOfDocuments*100/131897), "%", "Doc number :",glob.numberOfDocuments)
    print(">", "Doc number :",glob.numberOfDocuments)

#merge all temporary files containing run triples (see above) in an on-disk inverted files 
def mergeRunsToIF():
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
                    currentEntriesInFiles.append([entry_eval[0], entry_eval[1], entry_eval[2], i])
                #the stack is sorted so it wil pop the right entry 
                currentEntriesInFiles[1:] = sorted(currentEntriesInFiles[1:], reverse=True)
                current_entry = currentEntriesInFiles.pop()

            wordCounter += 1
            #every new word update voc list 
            vocList[current_word] = IF_file.tell()

            # compute score = tf * idf
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
    print(countDoc)  #132626 docs for whole dir


if __name__ == "__main__":
    constructIF()
    print(IF)

# def mergeSortedRuns():
#     tempfile1 = "IFConstruction/tmp/file_1.tmp" 
#     tempfile2 = "IFConstruction/tmp/file_2.tmp"
#     tempfile3 = "IFConstruction/tmp/file_3.tmp" 
#     tempfile4 = "IFConstruction/tmp/file_4.tmp"

#     mergeDone = False
#     switchFiles = True

#     while not mergeDone:

#         if(switchFiles):
#             fileTomerge1 = tempfile1
#             fileTomerge2 = tempfile2
#             destFile1 = tempfile3
#             destFile2 = tempfile4
#         else:
#             fileTomerge1 = tempfile3
#             fileTomerge2 = tempfile4
#             destFile1 = tempfile1
#             destFile2 = tempfile2

#         open(destFile1, "w").close()
#         open(destFile2, "w").close()

#         with open(fileTomerge1, 'r') as file1, open(fileTomerge2, 'r') as file2, open(destFile1, 'a+') as file3, open(destFile2, 'a+') as file4:
#             mergedPairNumber = pairWiseMerge(file1, file2, file3, file4)

#         if(mergedPairNumber == 0):
#             mergeDone = True

#         switchFiles = not switchFiles


# def pairWiseMerge(fileToMerge1, fileToMerge2, destinationFile1, destinationFile2):
#     writefile1 = True
#     entry2 = fileToMerge2.readline()
#     if(entry2 == "" or entry2 == "\n"):
#         return 0
#     word2 = ast.literal_eval(entry2)[0]
#     pairCounter = 0
#     for entry1 in fileToMerge1:
#         if(entry1 != "\n"):
#             word1 = ast.literal_eval(entry1)[0]
#         # print("before while")
#         while((entry2 != "" and entry2 != "\n" and word2 < word1) or (entry2 != "" and entry2 != "\n" and entry1 == "\n")):#or (entry2 != "\n" and entry1 == "")
#             if(writefile1):
#                 destinationFile1.write(entry2)
#             else:
#                 destinationFile2.write(entry2)

#             entry2 = fileToMerge2.readline()
#             if(entry2 != "\n"):
#                 word2 = ast.literal_eval(entry2)[0]

#         # print("after while")

#         if(entry1 == "\n" and entry2 == "\n"):
#             pairCounter += 1
#             print("number of merged pair :", pairCounter, end="\r")
#             if(writefile1):
#                 destinationFile1.write("\n")
#             else:
#                 destinationFile2.write("\n")
#             writefile1 = not writefile1
#             entry2 = fileToMerge2.readline()
#             if(entry2 != "" and entry2 != "\n"):
#                 word2 = ast.literal_eval(entry2)[0]
#             continue

#         if(writefile1):
#             destinationFile1.write(entry1)
#         else:
#             destinationFile2.write(entry1)

#         # print("end for")

#     if(entry2 != ""):
#         for leftEntry in fileToMerge2:
#             if(writefile1):
#                 destinationFile1.write(leftEntry)
#             else:
#                 destinationFile2.write(leftEntry)

#     if(writefile1):
#         destinationFile1.write("\n")
#     else:
#         destinationFile2.write("\n")    

#     print("number of merged pair :", pairCounter)
#     return pairCounter

# # def mergedRunsToIF():
# #     mergedRunsFile = "IFConstruction/tmp/file_1.tmp" 
# #     IFfile = "IFConstruction/tmp/inverted_file" 

# #     open(tempfile1, "w").close()

# #     with open(mergedRunsFile, 'r') as file1, open(IFfile, 'a+') as file2: