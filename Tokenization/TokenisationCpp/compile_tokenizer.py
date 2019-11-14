try:
    from distutils.core import setup, Extension
except:
    raise RuntimeError("\n\nPython distutils not found!\n")

# Definition of extension modules
cTokenizer = Extension('cTokenizer',
                 sources = [ 'TokenizerInterface.cpp'])

# Compile Python module
setup (ext_modules = [cTokenizer],
       name = 'cTokenizer',
       description = 'cTokenizer Python module',
       version = '1.0')