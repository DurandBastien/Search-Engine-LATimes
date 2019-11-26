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
  - naive algorithm to be able to test the project

## Second iteration

- Tokenization (using nltk)
  - Reading the dataset
    - C++ Tokenizer behaving as a stream whith cursor jumping from one document to another
    - First open the folder then open a new file if needed as documents are requested
    - Next element in the stream is : [filename, doc ID, tokens in doc, doc start index in file, doc end index in file]
  - Pre-processing on tokens
    - Replace words by their lemma
    - Replace words by their stem
- Inverted files construction
  - disk-based construction using the tokenizer described above
  - construction splitted in runs, each run process a bunch of documents, the size of a run (e.g. the number of documents) is given beforehand
  - each run computes and writes an alphabeticaly sorted list of triples (word, doc ID, number of occurrence) in a temporary file  
  - once the whole dataset has been read, the temporary files are merged to produce an inverted file on disk
  - each entry of the inverted file are (word, posting list) and each posting list are sorted by decreasing score 
  - in the meantime two hashmaps are constructed in-memory, one to map doc IDs to the place where is stores their content on disk (e.g. filename and indexes) and one to map a word to the place in the inverted file where its posting list is stored
- Search algorithm
