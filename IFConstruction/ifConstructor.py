#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math;
import ast;
import os
from collections import OrderedDict 

from Tokenization import tokenizer

"""
Created on Fri Nov  8 11:03:25 2019

@author: clementguittat
"""
from Globals.globals import invertedFile as IF
from Globals.globals import docID2filename as d2f


def constructIF(tokenizer):
    global countDoc
    countDoc = 0


    for file in tokenizer.listfile[:4]:
        content = tokenizer.readFile(file)
        index = 0
        while index != len(content):
            mydoc= tokenizer.extractDocumentFromFile(content,index)

            countDoc = countDoc + 1
            d2f[mydoc[0]] = [file, mydoc[2], mydoc[3]]
            docId = mydoc[0]
            index = mydoc[3]
            tokens = tokenizer.createListOfTokens(mydoc[1])
            tokens = tokenizer.removeStopWords(tokens)
            tokens = tokenizer.replaceWordsByStem(tokens)

            for word in tokens:
                if (word in IF):
                    if (docId in IF[word]):
                        IF[word][docId] += 1
                    else:
                        IF[word][docId] = 1
                else:
                    IF[word] = {docId: 1}
        print(file, len(IF)) 

def constructIFFromStreamTokenizer(streamTokenizer):
    counter = 0
    docFromStream = streamTokenizer.getNextDocAsTokens()
    while(docFromStream):
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
        d2f[docID] = [filename, docIndexStart, docIndexEnd]
        for word in tokens.split():
            if (word in IF):
                if (docID in IF[word]):
                    IF[word][docID] += 1
                else:
                    IF[word][docID] = 1
            else:
                IF[word] = {docID: 1}
        docFromStream = streamTokenizer.getNextDocAsTokens()
        if(counter == 9):
            break
        counter+=1

def constructIF_diskBased(streamTokenizer, runSize = 1):
    datasetToSortedRuns(streamTokenizer, runSize)
    mergeRunsToIF()

def datasetToSortedRuns(streamTokenizer, runSize = 1):
    os.system("rm IFConstruction/tmp/*")

    docID2ContentFilename = "Globals/docID2ContentIndexes.dict"
    tempfile = "IFConstruction/tmp/file_"
    tempfileCounter = 0 

    runCounter = 0
    docFromStream = streamTokenizer.getNextDocAsTokens()
    runTriples = []
    docCounter = 1
    docID2Content = {}
    while(docFromStream):
        print(">", int(docCounter*100/131897), "%", "Doc number :",docCounter, end="\r")
        # print(">", "Doc number :",docCounter, end="\r")

        docCounter += 1
        filename, docID, tokens, docIndexStart, docIndexEnd = docFromStream
        docID2Content[docID] = [filename, docIndexStart, docIndexEnd]
        if(runCounter < runSize):
            docWiseDict = {}
            for word in tokens.split():
                if (word in docWiseDict):
                    docWiseDict[word] += 1
                else:
                    docWiseDict[word] = 1
            for word in docWiseDict:
                runTriples.append([word, docID, docWiseDict[word]])
            runCounter += 1
        else:
            runTriples.sort()
            #flush sorted runTriples
            tempfileCounter += 1
            with open(tempfile+str(tempfileCounter), "w") as file:
                file.write(run_ToString(runTriples))

            runTriples = []
            runCounter = 0

        docFromStream = streamTokenizer.getNextDocAsTokens()

    if(runTriples[0]):
        runTriples.sort()
        #flush sorted runTriples
        tempfileCounter += 1
        with open(tempfile+str(tempfileCounter), "w") as file:
            file.write(run_ToString(runTriples))

    docID2Content_file = open(docID2ContentFilename, "w")
    docID2Content_file.write(str(docID2Content))
    docID2Content_file.close()

    print(int(docCounter*100/131897), "%", "Doc number :",docCounter)
    # print(">", "Doc number :",docCounter)

def mergeRunsToIF():
    print("start merging")
    IFname = "Globals/IF.dict"
    vocabularyFilename = "Globals/vocabulary.dict"

    tmpFoldername = "IFConstruction/tmp/"
    listfile = os.listdir(tmpFoldername)
    
    openedFiles = [open(tmpFoldername+filename, "r") for filename in listfile]
    currentEntriesInFiles = [None]

    for i, file in enumerate(openedFiles):
        entry = file.readline()
        if(entry != "" or entry != "\n"):
            entry_eval = ast.literal_eval(entry)
            currentEntriesInFiles.append([entry_eval[0], entry_eval[1], entry_eval[2], i])
    currentEntriesInFiles[1:] = sorted(currentEntriesInFiles[1:], reverse=True)

    open(IFname, "w").close()
    
    vocList = {}
    with open(IFname, "a+") as IF_file:#, open(vocabularyFilename, "a+") as vocab_file:

        current_entry = currentEntriesInFiles.pop()
        while(len(currentEntriesInFiles) > 0):
            current_word = current_entry[0]
            posting_list = []
            while(current_entry != None and current_word == current_entry[0]):
                posting_list.append([current_entry[1], current_entry[2]])

                entry = openedFiles[current_entry[3]].readline()
                if(entry != "" and entry != "\n"):
                    # print(entry)
                    entry_eval = ast.literal_eval(entry)
                    currentEntriesInFiles.append([entry_eval[0], entry_eval[1], entry_eval[2], i])
                currentEntriesInFiles[1:] = sorted(currentEntriesInFiles[1:], reverse=True)
                current_entry = currentEntriesInFiles.pop()
            # vocab_file.write(str([current_word, IF_file.tell()])+"\n")
            vocList[current_word] = IF_file.tell()
            posting_list.sort(key=lambda x:x[1], reverse = True)
            posting_list_dict = OrderedDict({ i : j for i,j in posting_list })
            IF_file.write(str([current_word, posting_list_dict])+"\n")
            # print(current_word)
            # print(currentEntriesInFiles)
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

def giveScores():
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