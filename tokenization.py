#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import re


# In[14]:


class Tokenization:
     
    def __init__(self, listfile):
        self.listfile = os.listdir(listfile)
        self.path = listfile
    
    def readFile(self,file):
        f = open(self.path+'/'+file,"r")
        content = f.readlines()
        #print(content)
        print(self.nextDocument(content,2))
        f.close()
        
    
    def nextDocument(self, content, index):
        docid = content[index].replace('<DOCID> ','')
        docid = docid.replace(' </DOCID>','')
        paragraph = ''
        
        for i in range(index + 1, len(content)):
            if "DOCID" in content[i]:
                nextDocLine = i
                break
            if "<P>" in content[i]:
                i = i + 1
                while "</P>" not in content[i]:
                    if i+1 >= len(content):
                        break
                    else:
                        paragraph = paragraph + content[i]
                        i = i + 1 
                        
                        
        return docid, paragraph
            


# In[15]:


t = Tokenization("./latimes")
print(t.readFile("la010289"))


# In[ ]:





# In[ ]:




