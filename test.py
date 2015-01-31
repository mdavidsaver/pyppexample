#!/usr/bin/env python

from __future__ import print_function

import mylib
import weakref

def fatal(O):
    print('Dies',O)

L=mylib.Line()
print('Empty line')
print(L.tostring())

# Four "cells", initially NULL elements
L.cells.append(mylib.Cell())
L.cells.append(mylib.Cell())
L.cells.append(mylib.Cell())
L.cells.append(mylib.Cell())


print('NULL elem',L.cells[0].elem)

# first cell is generic
CC = (L.cells[0], L.cells[1])
E = L.cells[0].elem = mylib.Elem()
E.name = 'elem1'

# second cell is special
S = L.cells[1].elem = mylib.Special()
S.name = 'elem2'
S.foo = 'test'
S.vals[0] = 42

# Drop python references to Elem and Special
# to ensure they are "owned" by C++ and
# won't be free'd

RE = weakref.ref(E, fatal)
RS = weakref.ref(S, fatal)
del E, S
import gc
gc.collect()

print('Non-empty line')
print(L.tostring())

# sub-class element in python
class PyElem(mylib.Elem):
    def __init__(self):
        super(PyElem,self).__init__()
        self.bar = 14
    def printstr(self):
        return("Python element %s\n bar: %s\n"%(self.name, self.bar))

P = L.cells[2].elem = PyElem()
P.name = 'elem3'

print('Py line')
print(L.tostring())
