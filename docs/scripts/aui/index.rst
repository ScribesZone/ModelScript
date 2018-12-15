.. .. coding=utf-8

.. highlight:: AUIScript

.. index:: ! .aus, ! AUIScript
   single: Script ; AUIScript

.. _AUIScript:

AUIScript
=========

..  warning::
    At the time being abstract user interfaces (AUI) are currently
    to be described only informally using a "paper and pencil" method.
    This page present a candidate language to represent AUI more formally.
    It is **not** to be used in current projects. It is shown here just
    to shown how abstract user interface modeling could be integrated
    in ModelScript.

Examples
--------

..  code-block:: AUIScript

    aui model Demo

    space EntrerLesInformations
        | Some documentation
        concepts
            email
            numerotel
        links
            ChoisirTypeReservation
            EntrerLesInformations


    space EntrerLesInformations "Réservation"
        concepts
            email "email"
            numerotel "numéro de téléphone"
        links
            ChoisirTypeReservation "type"
            EntrerLesInformations "détail"
            back to EntrerLesInformations "précédent"
        transformation
            from
                Informer
            rule R1
            rule R2
            | Some explainations

    space ChoisirTypeReservation
        links
            ReservationSansPayer
            Reserver
            back to EntrerLesInformations

    space ReservationSansPayer
        links
            back to ChoisirTypeReservation
            PreciserCriteresDeRecherche

    space PreciserCriteresDeRecherche
        links
            EntrerLesInformations

    space Reserver
        links
            back to ChoisirTypeReservation
            Payer

    space Payer
        concepts
            modeDePaimement
            numeroDeCarte
        links
            ChoisirTypeDeBillet
            Payer

    space ChoisirTypeDeBillet
        concepts
            pdf
            mobile
        links
            back to PreciserCriteresDeRecherche


    space PreciserCriteresDeRecherche
        links
            EntrerLesInformations

.. index:: ! AbstractSpace, ! Space
   pair: AUIScript ; Space

Concepts
--------

* spaces
* links
* transformations

Dependencies
------------

The graph below show all language depdencies.

..  image:: media/language-graph-aui.png
    :align: center


Spaces
------

Links
-----

Transformation
--------------
