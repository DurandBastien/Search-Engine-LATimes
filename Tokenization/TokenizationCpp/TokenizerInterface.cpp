#include <Python.h>
// #include </usr/include/python3.5/Python.h>
#include <iostream>
#include <string>
#include "Tokenizer.h"

using namespace std;


PyObject* construct(PyObject* self, PyObject* args){
    // Arguments passed from Python
    const char* foldername_;   

    // Process arguments passes from Python
    PyArg_ParseTuple(args, "s",
                     &foldername_);

    // Allocate new object
    Tokenizer* tokenizer = new Tokenizer(foldername_);

    // Create a Python capsule with a pointer to object
    PyObject* tokenizerCapsule = PyCapsule_New((void *)tokenizer, "TokenizerPtr", NULL);
    PyCapsule_SetPointer(tokenizerCapsule, (void *)tokenizer);
    // cout << "construct" << endl;
    // Return the Python capsule with the pointer toobject
    return Py_BuildValue("O", tokenizerCapsule);   // "O" means "Python object"
}

PyObject* getNextDocAsTokens(PyObject* self, PyObject* args){
    // Arguments passed from Python
    PyObject* tokenizerCapsule_; 

    // Process arguments
    PyArg_ParseTuple(args, "O",
    				 &tokenizerCapsule_);
 	
    // Get the pointer to object
    Tokenizer* tokenizer = (Tokenizer*)PyCapsule_GetPointer(tokenizerCapsule_, "TokenizerPtr");

    int docStart;
    int docEnd;
    string docID;
    string buffer;     
    if(tokenizer->get_nextDoc(docID, buffer, docStart, docEnd)){
        string tokens = tokenizer->parseText2Tokens(buffer);
        return Py_BuildValue("sssii", tokenizer->getCurrentFilename().c_str(), docID.c_str(), tokens.c_str(), docStart, docEnd);
    }else
        return Py_BuildValue("");
}

PyObject* delete_object(PyObject* self, PyObject* args)
{
/*
 *  C++/PYTHON OBJECT DESTRUCTOR.
 */
    // Arguments passed from Python
    PyObject* tokenizerCapsule_;   // Capsule with the pointer to `Car` object

    // Process arguments
    PyArg_ParseTuple(args, "O",
                     &tokenizerCapsule_);

    // Get the pointer to object
    Tokenizer* tokenizer = (Tokenizer*)PyCapsule_GetPointer(tokenizerCapsule_, "TokenizerPtr");

    // Delete the object
    delete tokenizer;

    // Return nothing
    return Py_BuildValue("");
}

static PyMethodDef cTokenizerFunctions[] =
{
/*
 *  Structures which define functions ("methods") provided by the module.
 */
    {"construct",                   // C++/Py Constructor
      construct, METH_VARARGS,
     "Create Tokenizer object"},

    {"getNextDocAsTokens",                     // C++/Py wrapper 
      getNextDocAsTokens, METH_VARARGS,
     "get the next tokens"},

    {"delete_object",               // C++/Py Destructor
      delete_object, METH_VARARGS,
     "Delete Tokenizer object"},

    {NULL, NULL, 0, NULL}      // Last function description must be empty.
                               // Otherwise, it will create seg fault while
                               // importing the module.
};


static PyModuleDef cTokenizerModule =
{
/*
 *  Structure which defines the module.
 *
 *  For more info look at: https://docs.python.org/3/c-api/module.html
 *
 */
   PyModuleDef_HEAD_INIT,
   "cTokenizer",               // Name of the module.

   NULL,                 // Docstring for the module - in this case empty.

   -1,                   // Used by sub-interpreters, if you do not know what
                         // it is then you do not need it, keep -1 .

   cTokenizerFunctions         // Structures of type `PyMethodDef` with functions
                         // (or "methods") provided by the module.
};


PyMODINIT_FUNC PyInit_cTokenizer(void)
{
/*
 *   Function which initialises the Python module.
 *
 *   Note:  This function must be named "PyInit_MODULENAME",
 *          where "MODULENAME" is the name of the module.
 *
 */
    return PyModule_Create(&cTokenizerModule);
}