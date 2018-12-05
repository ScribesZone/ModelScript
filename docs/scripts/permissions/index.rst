.. .. coding=utf-8

.. highlight:: PermissionScript

.. index::  ! .pes, ! PermissionScript
    pair: Script ; PermissionScript

.. _PermissionScript:


PermissionScript
================

Concepts
--------

Dependencies
------------

The graph below show all language depdencies.

..  image:: media/language-graph-pes.png
    :align: center


Subject
-------

Action
------

Permission
----------

Resource
--------

Examples
--------

..  note::
    The example below is based on a legacy syntax.

::

    permission model A2
    import usecase model from 'a.uss'
    import class model from 'a.cls'
    import class model from 'a1.cls'

    M,N  can create, delete  C,R
    M   can create   D
    M   can read, update  C.cs
    M   can RU  C.ci
    N   can read   R.r1
    N   can create, delete  R
    U1  can create, delete  S
    U1  can R   S.sa



