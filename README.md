# Search-Engine-LATimes

This is a framework to execute search queries on a dataset consisting of LA Times records.
To be able to run this code you will need to execute:
  - pip install nltk

## First iteration

- Tokenizer
  - Initialize tokeniker with the list of files 
  - Extract documents from files representing by an id
  - Extract tokens from documents
  - Pre-processing on tokens (remove punctuation and sto words)	
- Inverted files construction
  - Inverted file: HashMap(keys = word, value = Posting List)
  - Posting List: HashMap(key = docID, value = score(word, docID))
  - Loop through files and update global HashMap using number of word occurence in document as a score
  - Issue: can't fit in memory
- Search algorithm
  - naive algorithm to be able to test the project

## Second iteration

- Tokenization (using nltk)
  - Replace words by their lemma
  - Replace words by their stem
- Inverted files construction
- Search algorithm
