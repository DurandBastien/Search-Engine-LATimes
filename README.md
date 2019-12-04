# Search-Engine-LATimes

This is a framework to execute search queries on a dataset consisting of LA Times records.

The framework is divided into different folders representing functionalities:
  - Document server: fetch the content of documents in the dataset so the user can get an output to its query
  - Globals: folder where we gather all global variables or built files used in our application. 
  - IFConstruction: contains functions to build an in-memory or disk-based inverted file and other configuration files.  
  - QueryMaker: used to emulate a query shell and also contain functions to pre-process queries
  - SearchAlgorithms: folder where you will find the 3 different algorithms used to find the best documents according to the keywords in the given query. 
  - Tokenization: contains the two types of tokenizer, one in python and one in cpp 

## Get started

You need the dataset.

To be able to run the code you will need to install:
  - nltk
  - gensim

We provide ready to use configuration files (inverted file..) here : https://fex.insa-lyon.fr/get?k=rx0QON6MxKBHMnvyk8F. Unzip the folder in Globals/ so you get four subfolders in Globals/ and the word embedding model :
/Globals
  / nostemm_nolemm_notfidf
  / nostemm_nolemm_tfidf
  / stemm_nolemm_tfidf
  / stemm_lemm_tfidf
  embeddingModel
  
Each subfolder contains :
  - an inverted file
  - a vocabulary file

If you don't save those files, you will have to tell the framework to construct them but it takes time.
 
In this case, to be able to run the construction of the disk-based version of the inverted file:
  - a c++ tokenizer is used, this tokenizer is wrapped to be called in python,
  - to compile the wrapper you will need the python.h header which, for instance, is provided in the python3-dev package on linux (apt-get install python3-dev),
  - then to compile the c++ object and its wrapper, go to Tokenization/TokenizationCpp then "make clean" and "make tokenizer_py_module"

Eventually, before runing the code, make sure you have set proper paths in the main function :
  - path to the dataset
  - path to the vocabulary file
  - path to the inverted file 

## Tests

We have experimented different methods to improve our search engine for disjounctive queries. You will find our consistency and performance tests in the NAME file. You can run the tests but you will also see the expected results we have obtained.
  
Finally, details of our working process and the sequential updates we made to build the framework are detailed in the following sections.

## Iterations

### First iteration

- Tokenization
  - Reading the dataset
    - Initialize tokeniker with the list of files 
    - Extract documents from files representing by an id
    - Extract tokens from documents using white space as delimiter
  - Pre-processing on tokens
    - Remove punctuation and stop words	
- Inverted file construction
  - Construction in-memory using the tokenizer described above
  - Inverted file: HashMap(keys = word, value = Posting List)
  - Posting List: HashMap(key = docID, value = score(word, docID))
  - Loop through files and update global HashMap using number of word occurence in document as score
- Search algorithm
  - naive algorithm to be able to test the project : 
    - We go through all the Posting List associated with the keywords in the query. 
    - Then we compute the score of each document by adding the value of a document in every Posting List. 
- Making queries
    - simple shell which takes a search algorithm and performs user's queries with it
    - print the 10 best results as a list of doc ID
    - then print the content of the document corresponding to the chosen doc ID

### Second iteration

- Tokenization
  - Reading the dataset
    - C++ Tokenizer behaving as a stream, yielding document after document
    - First, it opens the folder, then it reads the dataset as if it was one file
    - Next element in the stream is : [filename, doc ID, tokens in doc, doc start index in file, doc end index in file]
  - Pre-processing on tokens (using nltk)
    - Replace words by their lemma
    - Replace words by their stem
- Inverted files construction
  - disk-based construction using the tokenizer described above
  - construction splitted in runs, each run process a bunch of documents, the size of a run (e.g. the number of documents) is given beforehand
  - each run computes and writes an alphabeticaly sorted list of triples (word, doc ID, number of occurrences) in a temporary file  
  - once the whole dataset has been read, the temporary files are merged to produce an inverted file on disk
  - each entry of the inverted file are (word, posting list) and each posting list are sorted by decreasing score 
  - in the meantime two hashmaps are constructed in-memory, one to map doc IDs to the place where is stores their content on disk (e.g. filename and indexes) and one to map a word to the place in the inverted file where its posting list is stored
- Search algorithm
  - implementation of the fagin algorithm :
    - retrieve all the posting lists associated with the keywords in the query
    - instantiate the dict M as all the documents seen at least once in a Posting List but not in all the Posting List
    - M : HashMap (key = docId, value = pair(updated score of the document, number of PostingList seen which contains the document ) )
    - instantiate the list C as all the documents seen in every Posting List
    - First, we go through the first element of every PostingList. If this element is a document we've never seen, we will add it to M. Otherwise, if this element has been seen in every PostingList we will add it to C and remove it from M, else we will just update the value of the score of this document in M and increment the "number of times seen" variable.
    - Then we will go on with the second element of every PostingList and so on. 
    - After this loop process, we will go through the remaining elements in M and compute their final score by taking into account every Posting List in order to be sure that their score are not bigger than those in C. 
- Making queries
  - Pre-processing on queries before applying the search algorithm
    - Convert into list of tokens
    - Remove stop words
    - Apply stemming/lemmatization if needed

### Third iteration

- Inverted files construction
  - Compute score = tf * idf = (1 + log(number of occurrences)) * log(total number of documents/(length of posting list))) 
- Making queries
  - Instead of yielding a list of doc ID as a query result, it fetchs metadata from the documents (date, headline, section)
  - Apply word embedding on queries to extend them with synonyms (using gensim)
    - Construct the dataset with stemming/lemmatization if needed and store it in memory
    - Train the model with 100 dimensions and store it in memory
    - Compute the most similar function (based on cosinus similarity) on query's tokens to extract the most relevant synonyms
  - Convert query into list of tokens with associated scores to make the original query's tokens more important than the synonyms added
    - In case of duplicated tokens, we have chosen to add up their scores
- Search Algorithm: 
  - When computing the score of a document, we take into account the weight of the keyword in the query (not the same weight if it was present more than once in the querry or if it was an added synonym word) 
  

# Authors:
  - Bastien DURAND
  - Clément GUITTAT
  - Yang HUA
  - Alexandra VERRIER
