#include <string>
#include <vector>
#include <dirent.h>
#include <iostream>
#include <fstream>

class Tokenizer
{
public:
	Tokenizer(std::string&);
	std::string get_nextTokens(std::string&);

private:
	char* foldername;
	DIR *folder = NULL;
    struct dirent *dirEntity;
    std::ifstream currentFile;

	void openDir();
	bool openNextFile();
	bool gotoNextOccurence(std::string&);
	std::string parseDocID(std::string&);
};

