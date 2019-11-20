#include <iostream> 

#include "Tokenizer.h"

using namespace std; 
int main() 
{ 
  string foldername = "/home/bastien/Documents/latimes/";
  Tokenizer tok(foldername);
  string tokens1;
  string tokens2;
  cout << tok.get_nextTokens(tokens1) << endl;
  cout << tokens1 << endl;
  cout << tok.get_nextTokens(tokens2) << endl;
  cout << tokens2 << endl;
  return 0; 
} 