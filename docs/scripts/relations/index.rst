.. .. coding=utf-8

..  .. highlight:: RelationScript

.. index::  ! .res, ! RelationScript
    pair: Script ; RelationScript

.. _RelationScript:



RelationScript
==============

Relations
---------

::

    R3(_a,_b,c,d)




Constraints on domain
---------------------

::

    R(a,b,c,d)
        dom(a) = String
        dom(b) = dom(c) = Date
        dom(d) = Real ?

Referential integrity constraints
---------------------------------

::

    R1[d] <= R2[d1]
    R1[d1,d1] <= R2[d1,d2]
    R[X] u R[z] = {}
    R[X] n R[z] = Persons[X]
    R[b,m] not null

Functional dependencies
-----------------------

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

    R(a,b,c,d)


Exemples
--------

Short form

Long form