#include "Tokenizer.h"
#include <cstring>
#include <sstream>
#include <algorithm>

using namespace std;

Tokenizer::Tokenizer(string foldername_){
	foldername = new char[foldername_.size() + 1];
	strcpy(foldername, foldername_.c_str());
	openDir();
	readdir(folder);
	readdir(folder);
	openNextFile();
}

Tokenizer* Tokenizer::get_nextDoc(string& docID, string& docContent, int& docStartPosition, int& docEndPosition){
	// cout << "get_nextTokens" << endl;
	string docDelimiter = "<DOC>";
	if(gotoNextOccurence(docDelimiter) == false){
		if(openNextFile() == false)
			return NULL;
		else
			gotoNextOccurence(docDelimiter);
	}
	string line;
	getline(currentFile, line);//<DOC>
	getline(currentFile, line);//<DOCNO> LA070689-0001 </DOCNO>
	docStartPosition = currentFile.tellg();
	docID = parseDocID(line);
	getline(currentFile, line);//<DOCID> 78471 </DOCID>
	while(line[0] != '<' || line.substr(1,5) != "/DOC>"){
		docContent += line;
		getline(currentFile, line);
	}
	docEndPosition = currentFile.tellg();
	return this;
}

void Tokenizer::openDir(){
    if ((folder = opendir(foldername)) == NULL)
    	cerr << "Can't open " << foldername << endl;
}

bool Tokenizer::openNextFile(){
	currentFile.close();
	currentFile.clear();
	dirEntity = readdir(folder);
	if(dirEntity != NULL){
		currentFilename = string(dirEntity->d_name);
		// cout << foldername+currentFilename << endl;
		currentFile.open(foldername+currentFilename);
		if(!currentFile.is_open())
			cerr << "Can't open " << foldername+currentFilename << endl;
	}else{
		cerr << "Can't read " << foldername << endl;
		return false;
	}
	return true;
}

bool Tokenizer::gotoNextOccurence(string& stringOccurence){
	// cout << "gotoNextOccurence" << endl;
	string line;
	while(getline(currentFile, line)){
        if(line.find(stringOccurence)!=string::npos)
            return true;
    }
	return false;
}

string Tokenizer::parseDocID(string& line){
	int delimPos = (int)line.find("</");
	return line.substr(8, delimPos-10);
}

string Tokenizer::getCurrentFilename(){
	return currentFilename;
}

string Tokenizer::parseText2Tokens(string& text){
	string tokens;
	toLowerCase(text);
	stringstream ssText(text);
	string word;
	while(ssText >> word){
		if(!isTag(word) && !isStopWord(word)){
			removePunctuation(word);
			if(word.size() > 0)
				tokens += (word + " ");
		}
	}
	return tokens;
}

bool Tokenizer::isTag(std::string& word){
	return (word.find("<") != string::npos);
}

bool Tokenizer::isStopWord(string& word){
	return (stopWords.find(word) != stopWords.end());
}

void Tokenizer::removePunctuation(string& word){  
    for (int i = 0, len = word.size(); i < len; i++) { 
        if (ispunct(word[i])){ 
            word.erase(i--, 1); 
            len = word.size(); 
        } 
    } 
      
}

void Tokenizer::toLowerCase(string& text){
	std::for_each(text.begin(), text.end(), [](char & c){
		c = ::tolower(c);
	});
}