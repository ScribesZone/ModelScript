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

    relation model CyberStore
    import glossary model from '../glossaries/glossaries.gls'
    import qa model from '../qa/relations.qas'

    relation Employee(_firstname_, salary, address, department)
        | All the employee in the store.
        intention
            (n, s, a, d) in Employee <=>
            | the `Employee` identified by her/his firstname <n>
            | earns <s> € per cycle. She/he lives
            | at the address <a> and works in the `Department` <d>.
        examples
            ('John', 120, 'Randwick', 'Toys')
        constraints
            dom(firstname) = String
            dom(salary) = Integer
            dom(address, department) = String
            key firstname
            firstname -> salary
            firstname -> address, department

    relation Leaders(_department_:String, boss:s)
        | The department leaders.
        intention
            (p, d) in Leaders <=>
            The `Leader` of the `Department` <d> is the person <p>.
        constraints
            key department
        transformation
            from Leader
            rule Class2Relation

    constraints
        Leaders[department] = Employee[department]
        Leaders[boss] C= Employee[firstname]

    constraint SalaryDifference
        | The difference of salary in a department must not exceed 100%.

    dataset DS1
        | Employees and leaders of Alpha Super store.
        Employee
            ('John', 120, 'Randwick', 'Toys')
            ('Mary', 130, 'Wollongong', 'Furniture')
            ('Peter', 110, 'Randwick', 'Garden')
            ('Tom', 120, 'Botany Bay', 'Toys')
        Leaders
            ('John', 'Toys')
            ('Mary', 'Furniture')
            ('Peter', 'Garden')

    negative dataset NDS1
        | Octavia and bookstore do not exist.
        | Violation of referential integrity constraints.
        Employee
            ('John', 120, 'Randwick', 'Toys')
            ('Mary', 130, 'Wollongong', 'Furniture')
        Leaders
            ('Octavia', 'Bookstore')

    query JohnBoss(boss)
        | The department leaders.
        (Employe:(firstname='John')[department] * Leaders)[boss]


RelationScript
--------------

RelationScript allows to express "schemas_" in the sense of the
`relational data model`_.

.. note::
    Note that the term "relation model" should not
    be confused with "relational data model". A relation model defines
    relations, just like usecase models defines usecases, class models
    defines classes, object models defines objets, and so on.

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
* datasets,
* queries.

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

    relation R4(_a_,c,d)
        | The list of X with their c and d.
        | In this relation the person a is ... with c ... and d ...

It can also be defined for "formally" in the intention section.

::

    relation R4(_a_,c,d)
        | The list of X with their c and d.
        intention
            (a,c,d) in R4 <=>
            | the person a is ... with c ... and d ...



Constraints on domain
---------------------

The domain of the attributes can be defined as following.

::

    relation R(a,b,c,d)
        constraints
            dom(a) = String
            dom(b) = dom(c) = Date
            dom(d) = Real ?

A basic type followed by '?' means that this domain is extended
with the ``null value`` ; the corresponding attribute is optional.

RelationalScript come with various datatype. Each datatype comes with
a shortcut notations that can be helpful when writing relation on a
single line.

=============== ==============
Datatype        Shortcut
=============== ==============
String          s
Real            r
Boolean         b
Integer         i
Date            d
DateTime        dt
Time            s
=============== ==============



Integrity constraints
---------------------

Integrity constraint, and in particular `Referential integrity constraints`_,
can be named or anonymous. They can be defined using plain text or using
the `relational algebra`_ notation when applicable.

::

    constraint Parent
        | Les parents d'une personne doivent être
        | plus agés que cette personne, d'au moins 7 ans.

    constraint FK_34h
        | The h of the relation R3 is one of the h of R4.
        R3[h] C= R4[h]

    constraints
        R1[d] C= R2[d]
        R1[d1,d1] C= R2[d1,d2]
        R[X] u R[z] = {}
        R[X] n R[z] = Persons[X]

See `relational algebra`_ section for more details about the notation.

Functional dependencies
-----------------------

`Functional dependencies`_ and the associated concepts can be defined as
following:

::

    relation R(a,b,c,d)
        constraints
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

    relation R(a,b,c,d)
        constraints
            3NF

Transformations
---------------

::

    import quality model Database from `../qa/database.qas`

    relation R(a,b,c,d)
        transformation
            from C1
            from C2
            rules R1
            | Columns C1.c and Columns C2.c
            | have been "merged" as following ...


Queries
-------

::

    query Q1(boss)
        | The department leaders
        (Employe:(firstname='John')[department] * Leaders)[boss]

Queries are based on the `relational algebra section`_.

..  _`relational algebra section`:

Relational algebra
------------------

In RelationScript all classical operators of the relational algebra
(`wikipedia <https://en.wikipedia.org/wiki/Relational_algebra>`_)
have their counterparts in ascii syntax.

==================  ====================================================
Operator            Example
==================  ====================================================
Projection          Employee[salary]
Selection           Employee :( address='Randwick' )
Renaming            L(employee, address) := Employee[firstname, address]
Cartesian product   Employee x Leaders
θ join              Employee * ( Employee.dept=Leaders.dept ) Leaders
Natural join        Employee * Leaders
Union               Employee[firstname] u Leaders[firstname]
Intersection        Employee[firstname] n Leaders[firstname]
Difference          Employee[firstname] - Leaders[firstname]
Empty set           {}
Set inclusion       Employee C= Person
Set inclusion       Employee C Person
Set equality        Employee = Person
Intersection        Employee n Person
Union               Employee u Person
Tuple               (10, 3, 'Hello)
==================  ====================================================


Dependencies
------------

The graph below show all language dependencies:

..  image:: media/language-graph-res.png
    :align: center


..  _schemas:
    https://en.wikipedia.org/wiki/Database_schema

..  _`relational data model`:
    https://en.wikipedia.org/wiki/Relational_model

..  _`relational algebra wikipedia`:
    https://en.wikipedia.org/wiki/Relational_algebra

..  _`Referential integrity constraints`:
    https://en.wikipedia.org/wiki/Referential_integrity

..  _`Functional dependencies`:
    https://en.wikipedia.org/wiki/Functional_dependency