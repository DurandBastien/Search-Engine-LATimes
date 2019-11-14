# Compiler and Python interpreter
CPYTHON3 = python3.7
CPP = g++

# C++ example
HEADERS = Tokenizer.h
OBJECTS = Tokenizer.o 

# Python module
MODULE_SOURCE = Tokenizer.cpp TokenizerInterface.cpp
MODULE_COMPILE_SCRIPT = compile_tokenizer.py

%.o: %.cpp $(HEADERS)
		$(CPP) -c $<

# Build Python module
tokenizer_py_module: $(MODULE_SOURCE) $(MODULE_COMPILE_SCRIPT) $(HEADERS)
	$(CPYTHON3) $(MODULE_COMPILE_SCRIPT) build_ext --inplace

# Clean up the current directory
.PHONY: clean
clean:
	rm -fR build
	rm -f *.so
	rm -f *.o
	rm -fR __pycache__