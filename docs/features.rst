Features
========


PyUseOCL features includes:

..  py:currentmodule:: pyuseocl.model


*   a **python-based AST** for *structural part* of "use" models.
    The structural content of ``.use`` class models is made avaible in
    python in the form of abstract syntax trees.
    The :py:mod:`pyuseocl.model` API provides
    classes such as
    :py:class:`Class`, :py:class:`Attribute`, :py:class:`Association`,
    :py:class:`Invariant`, etc. PyUseOCL is just based on hand-craft raw
    surface parser, so the content of operations and invariants is not
    made available.

..  py:currentmodule:: pyuseocl.evaluation

*   an **model evaluation API**. The result of evaluation ``.soil`` files (i.e.
    object models) against ``.use`` file (i.e. class model) is made available
    as a set of python objects (see :py:mod:`pyuseocl.evaluation`).


*   support for **assertions**. Assertions like the following can be added in .soil
    files as comments::

        -- @assert MyClass::MyInvariant1 OK
        -- @assert MyClass::MyInvariant2 Failed
        -- @assert MyClass::MyInvariant6 OK

    An evaluator is then is available to check which assertions are OK, KO or are
    failure. If needed, the result is readily available via an API
    (see :py:mod:`pyuseocl.assertion`)

*   a simple testing framework providing for instance a class
    :py:mod:`~pyuseocl.tester.TestSuite`.


..  _`USE OCL`: http://sourceforge.net/projects/useocl/
