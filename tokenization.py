#!/usr/bin/env python
# coding: utf-8

# In[30]:


#!/usr/bin/env python
# coding: utf-8

import os
import re


class Tokenization:
    def __init__(self, listfile):
        self.listfile = os.listdir(listfile)
        self.path = listfile

        """
        read certain file whose name specified in the para
        args:
            file: name of the file to read
        """

    def readFile(self, file):
        f = open(self.path + "/" + file, "r")
        content = f.readlines()
        # print(content)
        f.close()
        return content

        """
        extract the info of docID and Paragraph of next document.
        call iteratively to extract the info of all docs
        args:
            content: the content of the whole file
           
        """

    def nextDocument(self, content):
        try:
            if content == None:
                raise ValueError("file content empty!")

            nbDocId = 0
            paragraph = ""

            for i in range(0, len(content)):
                if "DOCID" in content[i]:
                    nbDocId = nbDocId + 1
                    if nbDocId == 2:
                        break
                    content[i] = (
                        content[i].replace("<DOCID> ", "").replace(" </DOCID>", "")
                    )
                    docid = content[i]
                elif "<P>" in content[i]:
                    content[i] = ""
                    i = i + 1
                    while "</P>" not in content[i]:
                        if i + 1 >= len(content):
                            break
                        else:
                            paragraph = paragraph + content[i]
                            i = i + 1
                    content[i] = ""

            return docid, paragraph

        except ValueError:
            return 0, 0


# In[32]:


t = Tokenization("./latimes")
content = t.readFile("la010289")
print(t.nextDocument(content))
print(t.nextDocument(content))
print(t.nextDocument(content))







# In[ ]:




