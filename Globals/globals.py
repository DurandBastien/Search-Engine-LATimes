#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:02:35 2019

@author: clementguittat
"""

global invertedFile
invertedFile = {}


global docID2filename
docID2filename = {}

def initmap():
    invertedFile = {"you": {1: 3, 2: 2}, "are": {1, 2}, "tuples": {2, 2}}