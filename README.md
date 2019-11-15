# Search-Engine-LATimes

This is a framework to execute search queries on a dataset consisting of LA Times records.

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


## Second iteration

- Tokenization
- Inverted files construction
- Search algorithm
