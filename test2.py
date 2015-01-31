#!/usr/bin/env python

from __future__ import print_function

import mylib
import gc, weakref

def fatal(O):
    print('Dies',O)

C=mylib.Cell()
RC=weakref.ref(C, fatal)
print('CC',C.elem) # None

E=mylib.Elem()
RE=weakref.ref(E, fatal)
print('MM',E) # None

print('RR E')
for R in gc.get_referrers(E):
    print('Q',type(R))
for R in gc.get_referents(E):
    print('W',type(R))
print('RR C')
for R in gc.get_referrers(C):
    print('Q',type(R))
for R in gc.get_referents(C):
    print('W',type(R))
del R

C.elem = E

print('RR E')
for R in gc.get_referrers(E):
    print('Q',type(R))
for R in gc.get_referents(E):
    print('W',type(R))
print('RR C')
for R in gc.get_referrers(C):
    print('Q',type(R))
for R in gc.get_referents(C):
    print('W',type(R))
del R

print('CC',C.elem)

del E
gc.collect()

print('Boom?',C.elem)
for R in gc.get_referrers(C.elem):
    print('Q',type(R))

