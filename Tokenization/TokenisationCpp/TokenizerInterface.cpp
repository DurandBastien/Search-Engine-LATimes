#include </usr/include/python3.5/Python.h>
#include <iostream>
#include <string>
#include "Tokenizer.h"

using namespace std;


PyObject* construct(PyObject* self, PyObject* args){
    // Arguments passed from Python
    string foldername_;   

    // Process arguments passes from Python
    PyArg_ParseTuple(args, "s",
                     &foldername_);

    // Allocate new object
    Tokenizer* tokenizer = new Tokenizer(foldername_);

    // Create a Python capsule with a pointer to object
    PyObject* tokenizerCapsule = PyCapsule_New((void *)tokenizer, "TokenizerPtr", NULL);
    PyCapsule_SetPointer(tokenizerCapsule, (void *)tokenizer);

    // Return the Python capsule with the pointer toobject
    return Py_BuildValue("O", tokenizerCapsule);   // "O" means "Python object"
}

PyObject* getNextTokens(PyObject* self, PyObject* args){
    // Arguments passed from Python
    PyObject* tokenizerCapsule_;
    string buffer;      

    // Process arguments
    PyArg_ParseTuple(args, "Os",
    				 &tokenizerCapsule_,
                     &buffer);
 	
    // Get the pointer to object
    Tokenizer* tokenizer = (Tokenizer*)PyCapsule_GetPointer(tokenizerCapsule_, "TokenizerPtr");

    string docID = tokenizer->get_nextTokens(buffer);

    return Py_BuildValue("ss", docID.c_str(), buffer.c_str());
}