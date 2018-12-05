.. .. coding=utf-8

.. highlight:: ObjectScript1

.. index::  ! .obs, ! ObjectScript1
    pair: Script ; ObjectScript1

.. _ObjectScript1:


ObjectScript1
=============

OB Script (OBS) is a textual notation for UML `object diagrams`_.
Object script is a restricted version of the `USE OCL`_
SOIL language. While in the context of USE the
``.soil`` extension is used, ``.obs`` is the extension of
object scripts.


Dependencies
------------

The graph below show all language depdencies.

..  image:: media/language-graph-obs.png
    :align: center

Concepts
--------


Enumerations
------------

..  code-block:: ObjectScript1

    Season::winter

Objects
-------

ObjectScript (USE OCL):

..  code-block:: ObjectScript1

    ! create bob : Person
    ! bob.nom := 'bob'
    ! bob.dateDeNaissance := '21/10/1994'

Links
-----

ObjectScript (USE OCL):

..  code-block:: ObjectScript1


    ! insert(tian,c232) into Owns


UML object diagram:

..  image:: media/USEOCLAssociationSOIL.png
    :align: center

Link objects
------------

Object Script (USE OCL):

..  code-block:: ObjectScript1

    ! c := new Hate between (chita,kaa)
    ! c.reason := "kaa is really mean"
    ! c.intensity = 1000

Annotated object models
-----------------------

..  code-block:: ObjectScript1

    --| Bob was born  ow
        ! create bob : Personne
        ! bob.nom := 'bob'
        ! insert(tian,c232) into Owns
    --| (1) Nourry Blanc est professeur de musique.
        ! create nourry : Enseignant
        ! nourry.nom := 'Nourry Blanc'
        ! nourry.matiere := 'musique'
        ! nourry.login := Undefined
        ! nourry.motDePasse := Undefined
    --| (2) Nourry Blanc intervient en terminale S876.
    --| (3) Il a vraiment de la chance.
    --| (4) La terminale S876 est plaisante.
        ! create s876 : Classe
        ! s876.code := 'S876'
        ! insert (nourry, s876) into IntervientDans
    --| (3) Alicia Ganto est professeur de math.



..  _`USE OCL`: http://sourceforge.net/projects/useocl/

..  _`object diagrams`: https://www.uml-diagrams.org/class-diagrams-overview.html#object-diagram