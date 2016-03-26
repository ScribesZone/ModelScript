.. .. coding=utf-8

Command Line Interface
======================

PyUseOCL provides a **very** simple Command Line Interface (CLI).

Compiling a class model
-----------------------

To compile a class model use::

    python pyuse.py MyClassModel.use

This command launchs the use tool, parse the result and provide output
in a slightly different format. Not a big deal.

Evaluating some states
----------------------

To evaluate one or more object files against a model use::

    python pyuse.py MyClassModel.use MyState1.soil MyState2.soil ...

This evaluate the assertions in each state files and report which
one pass or not.



