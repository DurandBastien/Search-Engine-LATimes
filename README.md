# Search-Engine-LATimes

This is a framework to execute search queries on a dataset consisting of LA Times records.
To be able to run this code you will need to execute:
  - pip install nltk

## First iteration

- Tokenization
  - Reading the dataset
    - Initialize tokeniker with the list of files 
    - Extract documents from files representing by an id
    - Extract tokens from documents using white space as delimiter
  - Pre-processing on tokens
    - remove punctuation and stop words	
- Inverted file construction
  - Construction in-memory using the tokenizer described above
  - Inverted file: HashMap(keys = word, value = Posting List)
  - Posting List: HashMap(key = docID, value = score(word, docID))
  - Loop through files and update global HashMap using number of word occurence in document as score
- Search algorithm
  - naive algorithm to be able to test the project : 
    - we go through all the Posting List associated with the keywords in the query. 
    - Then we compute the score of each document by adding the value of a document in every Posting List. 
- Making queries
    - simple shell which takes a search algorithm and performs user's queries with it
    - print the 10 best results as a list of doc ID
    - then print the content of the document corresponding to the chosen doc ID

## Second iteration

- Tokenization (using nltk)
  - Reading the dataset
    - C++ Tokenizer behaving as a stream, yielding document after document
    - First, it opens the folder, then it reads the dataset as if it was one file
    - Next element in the stream is : [filename, doc ID, tokens in doc, doc start index in file, doc end index in file]
  - Pre-processing on tokens
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
    - M : HashMap (key = docId, value = pair(updated score of the document, number of PostingList who contains the document ) )
    - instantiate the list C as all the documents seen in every Posting List
- Making queries


## Third iteration

- Inverted files construction
  - compute score = tf * idf = (1 + log(number of occurrences)) * log(total number of documents/(length of posting list))) 
- Making queries
  - instead of yielding a list of doc ID as a query result, it fetchs metadata from the documents (date, headline, section) 



## Test phase
- conditions générales : une requête commune (gobbledygook ->16 files, scrumptious -> 15 files, internet -> 3 files)
- Consistency (marquer résultat obtenu sur une même requête) (test end to end)
  - top 10 sur naive algorithm
    - sans stem, sans lem, sans wordEmbeding
    - avec stem, sans lem, sans wordEmbeding
    - sans stem, avec lem, sans wordEmbeding
    - sans stem, avec lem, avec wordEmbeding (3 synonymes)
  - top 10 sur fagin
    - sans stem, sans lem, sans wordEmbeding
    - avec stem, sans lem, sans wordEmbeding
    - sans stem, avec lem, sans wordEmbeding
    - sans stem, avec lem, avec wordEmbeding (3 synonymes)
  - top 10 sur threshold
    - sans stem, sans lem, sans wordEmbeding
    - avec stem, sans lem, sans wordEmbeding
    - sans stem, avec lem, sans wordEmbeding
    - sans stem, avec lem, avec wordEmbeding (3 synonymes)
- Performance (marquer temps exécution en commentaire)
  - temps de construction:
    - IF in RAM (pas de stem, lem ni embedding)
    - IF disk based (pas de stem, lem ni embedding)
  - temps d'exécution pour une même requête:
    - naive algo
    - fagin algo
    - threshold algo
