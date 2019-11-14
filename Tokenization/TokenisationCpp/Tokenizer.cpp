#include "Tokenizer.h"
#include <cstring>

using namespace std;

Tokenizer::Tokenizer(string& foldername_){
	foldername = new char[foldername_.size() + 1];
	strcpy(foldername, foldername_.c_str());
	openDir();
	cout << "ok" << endl;
	readdir(folder);
	cout << "ok" << endl;
	readdir(folder);
	cout << "ok" << endl;
	openNextFile();
	cout << "ok" << endl;
}

string Tokenizer::get_nextTokens(string& tokens){
	// cout << "get_nextTokens" << endl;
	string docDelimiter = "<DOC>";
	if(gotoNextOccurence(docDelimiter) == false){
		if(openNextFile() == false)
			return NULL;
		else
			gotoNextOccurence(docDelimiter);
	}
	string line;
	getline(currentFile, line);
	string docID = parseDocID(line);
	getline(currentFile, line);
	while(line[0] != '<' || line.substr(1,5) != "/DOC>"){
		tokens += line;
		getline(currentFile, line);
	}

	return docID;
}

void Tokenizer::openDir(){
    if ((folder = opendir(foldername)) == NULL)
    	cerr << "Can't open " << foldername << endl;
}

bool Tokenizer::openNextFile(){
	dirEntity = readdir(folder);
	if(dirEntity != NULL){
		string filename(foldername);
		filename += string(dirEntity->d_name);
		cout << filename << endl;
		currentFile.open(filename);
		if(!currentFile.is_open())
			cerr << "Can't open " << filename << endl;
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
	return line.substr(8, delimPos-8);
}