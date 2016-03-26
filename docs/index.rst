PyUseOCL's Documentation
========================

**PyUseOCL** is a python wrapper around the excellent `USE OCL`_ tool
(see also `ScribesTools/UseOCL`_).
OCL_ refers here to the Object Constraint Language, a part of
the UML_ standard. `USE OCL`_ is a java-based environment
based on OCL_.


By parsing different kind of output of the `USE OCL`_ command line tool,
PyUseOCL provides an "poor-man" integration means for python programs
(through the PyUseOCL API). PyUseOCL is mostly intended for
automation. PyUseOCL also provides a few features out of the box
via the a very simple command line.


..  toctree::
    :maxdepth: 8

    features
    quickStart
    cli
    api


References
==========

*   :ref:`genindex`
*   :ref:`modindex`

..  _`USE OCL`: http://sourceforge.net/projects/useocl/

..  _OCL: http://en.wikipedia.org/wiki/Object_Constraint_Language

..  _UML: http://en.wikipedia.org/wiki/Unified_Modeling_Language

..  _OCL specification: http://www.omg.org/spec/OCL/

..  _`ScribesTools/UseOCL`:
    http://scribestools.readthedocs.org/en/latest/useocl/index.html
