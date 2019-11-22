#include <string>
// #include <vector>
#include <dirent.h>
#include <iostream>
#include <fstream>
#include <unordered_set>

class Tokenizer
{
public:
	Tokenizer(std::string);
	Tokenizer* get_nextDoc(std::string&, std::string&, int&, int&);
	std::string getCurrentFilename();
	std::string parseText2Tokens(std::string&);

private:
	char* foldername;
	DIR *folder = NULL;
    struct dirent *dirEntity;
    std::ifstream currentFile;
    std::string currentFilename;
    std::unordered_set<std::string> stopWords =
    {"ourselves", "hers", "between", "yourself", 
                         "but", "again", "there", "about", "once", "during", 
                         "out", "very", "having", "with", "they", "own", "an",
                         "be", "some", "for", "do", "its", "yours", "such", "into",
                         "of", "most", "itself", "other", "off", "is", "s", "am",
                         "or", "who", "as", "from", "him", "each", "the", "themselves", 
                         "until", "below", "are", "we", "these", "your", "his", "through", 
                         "don", "nor", "me", "were", "her", "more", "himself", "this", "down",
                         "should", "our", "their", "while", "above", "both", "up", "to",
                         "ours", "had", "she", "all", "no", "when", "at", "any", "before",
                         "them", "same", "and", "been", "have", "in", "will", "on", "does",
                         "yourselves", "then", "that", "because", "what", "over", "why", "so",
                         "can", "did", "not", "now", "under", "he", "you", "herself", "has",
                         "just", "where", "too", "only", "myself", "which", "those", "i",
                         "after", "few", "whom", "t", "being", "if", "theirs", "my", "against",
                         "a", "by", "doing", "it", "how", "further", "was", "here", "than"};


	void openDir();
	bool openNextFile();
	bool gotoNextOccurence(std::string&);
	std::string parseDocID(std::string&);
	bool isTag(std::string&);
	bool isStopWord(std::string&);
	void removePunctuation(std::string&);
	void toLowerCase(std::string&);
};

