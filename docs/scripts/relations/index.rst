.. .. coding=utf-8

.. highlight:: RelationScript

.. index::  ! .res, ! RelationScript
    pair: Script ; RelationScript

.. _RelationScript:

RelationScript
==============

Examples
--------

::

    relation TheEmployees(_u_,v,e,r)
        | Employees and their roles and properties
        intention
            (u,v,e,r) in TheEmployees <=>
            | the employee e is ... with u ... v ... and
            | has role r within the company.
        examples
            (19, 30, 'noe', 'gardener')
            (24, -5, 'marie', 'manager')
        constraints
            key u
            dom(u) = dom(v) = Integer
            dom(e) = dom(c) = Date
            dom(d) = Real ?
            3NF
        transformation
            from C1
            from C2
            rules R1
            | Columns C1.u and Columns C2.v
            | have been "merged" as following ...

    TheEmployees[v] C= TheOffices[v]

RelationScript
--------------

RelationScript allows to express "schemas_" in the sense of the
`relational data model`_.

.. note::
    Note that the term "relation model" should not
    be confused with "relational data model". A relation model defines
    relations, just like usecase models defines usecases, class models
    defines classes, object models defines objects, and so on.

Concepts
--------

RelationScript is based on the following concepts:

* schema (called relation model),
* relations,
* columns,
* key and foreign keys,
* constraints on domains,
* functional dependencies.
* normal forms,

Relations
---------

Declaration of relations can expressed in a single line using the simple
notation typically used in textbooks. Column names are separated
by commas. While key attributes, usually underlined in textbooks,
are here enclosed in underscores such as ``_a_``).

::

    R3(_a_,_b_,c,d)

In the example above the column ``a`` and ``b`` are key participants.
This means that there are part of some key, but there is no indication
of what are the keys. This could be a key (a,b), or two keys (a) and (b).
If necessary the body of the relation will define what are the keys.

Relation intention
------------------

The intention of a relation can be defined informally somehow inside the
documentation of the relation.

::

    R4(_a_,c,d)
        | The list of X with their c and d.
        | In this relation the person a is ... with c ... and d ...

It can also be defined for "formally" in the intention section.

::

    R4(_a_,c,d)
        | The list of X with their c and d.
        intention
            (a,c,d) <=> the person a is ... with c ... and d ...



Constraints on domain
---------------------

The domain of the attributes can be defined as following.

::

    R(a,b,c,d)
        dom(a) = String
        dom(b) = dom(c) = Date
        dom(d) = Real ?

A basic type followed by '?' means that this domain is extended
with the ``null value`` ; the corresponding attribute is optional.

Basic type includes:
* ``String``,
* ``Real``,
* ``Boolean``,
* ``Integer``,
* ``Date``,
* ``DateTime``
* ``Time``.


Integrity constraints
---------------------

Integrity constraints (and in particular
`Referential integrity constraints`_) can be defined using
an ascii-based notation for set operators and relational algebra:

::

    R1[d] C= R2[d1]
    R1[d1,d1] C= R2[d1,d2]
    R[X] u R[z] = {}
    R[X] n R[z] = Persons[X]

The "ascii" notations are

*   ``C=`` and ``C`` stand for set inclusion,
*   ``u`` and ``n`` stand for set intersection and union,
*   ``R[x,y]`` stand for relation projection (as defined in relational
    algebra),
*   ``{}`` is the empty set.

Functional dependencies
-----------------------

`Functional dependencies`_ and the associated concepts can be defined as
following:

::

    R(a,b,c,d)
        key a,b
        a,b -> c,d
        prime a
        prime b
        /prime c
        a -/> c
        c -ffd> d
        a -/ffd> b
        {a}+ = {a,b,c}


Normal forms
------------

::

    R(a,b,c,d)
        3NF

Transformation
--------------

::

    import quality model Database from `../quality/database.qas`

    R(a,b,c,d)
        transformation
            from C1
            from C2
            rules R1
            | Columns C1.c and Columns C2.c
            | have been "merged" as following ...

Dependencies
------------

The graph below show all language dependencies:

..  image:: media/language-graph-res.png
    :align: center


..  _schemas:
    https://en.wikipedia.org/wiki/Database_schema

..  _`relational data model`:
    https://en.wikipedia.org/wiki/Relational_model

..  _`Referential integrity constraints`:
    https://en.wikipedia.org/wiki/Referential_integrity

..  _`Functional dependencies`:
    https://en.wikipedia.org/wiki/Functional_dependency