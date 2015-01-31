py++ example
============

Example demonstrating use of py++ wrapper generator.
Also building with distutils.

The structures being wrapped are defined in [mylib.h](mylib.h).
These include C arrays of POD types and shared_ptr<> to a polymorphic class.

See [test.py](test.py) and [test2.py](test2.py) for example usage.

Tested with python 2.7 and 3.2.

Dependencies
------------

* python-dev
* libboost-python-dev
* python-py++
