.. .. coding=utf-8

.. highlight:: GlossaryScript

.. index::  ! .gls, ! GlossaryScript
    pair: Script ; GlossaryScript

.. _GlossaryScript:

GlossaryScript
==============

The ``GlossaryScript`` language, as defined below, allows to express
*glossaries*. In practice there is only one glossary for a given project
(although packages can be used to split a glossary in multiple part).
Glossary scripts are to be saved with the ``.gls`` extension.

Dependencies
------------

The graph below show all language depdencies. As it can be seen the
glossary depend on all requirement documents. This is due to the fact
that the glossary is extracted from these documents. On the opposite
direction it is worth noticing that all artefacts depends on the glossary.
This is due to the fact that all scripts/artefacts may contain
documentations based on the glossary terms as well as identifiers.

..  image:: media/language-graph-gls.png
    :align: center


.. index:: ! Glossary


Concepts
--------



A *glossary* is a collection of *entries* optionally organized into
*packages*. The goal of a *glossary* is to define all *terms* used in the
context of a given project.

In essence a *glossary* is:

* a set of *entries* composed by a *main term* and *alternative terms*.
* the definition of relationships between all these terms,


.. index:: ! Entry
    single: Term
    single: Term; Main term (term)

Entries
-------

An entry is basically:

* a selected *main term* (e.g. ``Fil`` in the example below)
* a set of *alternative terms* (*synonyms*, inflections*,...),
* a *definition* that fits for all the terms,
* some optional *translations*.

..  code-block:: GlossaryScript

    Fil
        | Séquence de messages en réponse à un `Initial`. Un fil
        | peut être `Bloque` ou `Ouvert` et est identifié par
        | un `Theme` et un ensemble de `Cles`.
        synonyms: Discussion, FilDeDiscussion
        inflections; Fils
        translations
            fr: "fil de discussion"
            en: "thread"
            es: "conversacion"
    ...

The main term (``Fil`` here) is the one that is expected to be
referenced in technical texts.

.. index::
    single: Synonym
    single: Term; Synonym (term)

synomys
'''''''
Various synonyms can be associated to an entry:

..  code-block:: GlossaryScript

    Fil
        | Définition
        | ...
        synonyms: Discussion, FilDeDiscussion

Synonyms are terms that
that have the same meaning of the main term, but that come in different
forms. For instance the terms ``Discussion`` and ``Fil`` are said to be
synonym in the example above.  But ``Fil`` being the main term,
all occurrences of ``Discussion`` are expected to be substituted by
``Fil``.

.. index:: Inflection
    single: Term ; Inflection (term)


inflections
'''''''''''
*Inflections* are derivatives of the *main term*, such as plural forms,
forms with different genders, verbal vs. nominal form, and so one:

..  code-block:: GlossaryScript

    Fil
        | Définition
        | ...
        inflections: Fils

By contrast with *synonyms* *inflections* are regular variations
of the *main term* and are not expected to be replaced by this very term.

.. index:: Translation
    single: Term ; Translation (term)

translations
''''''''''''
While an *entry* is defined by its *main term*, this *entry* can possess
various *translations*. Each *translation* is defined by:
* the natural language used for the translation (encode using iso-639)
* the translation string.

..  code-block:: GlossaryScript

    Fil
        translations
            fr: "fil de discussion"
            en: "thread"
            es: "conversacion"


.. index:: Package

Packages
--------

A set of *entries* can be separated into different *packages* using the
``package`` keyword followed by the package identifier.

.. index::
    single: Package; Toplevel package
    single: Toplevel package

Toplevel packages
'''''''''''''''''

All *entries* after the ``package`` keyword and until the next one go
to the specified *package*. Moreover the *entries* before go to the
default "unamed" package. Note that to save space *entries* and *packages*
are at the same indent level.

A common usage for *packages* is to define various "sub glossary".
For instance the example below shows how to define a "DomainGlossary"
and a "TechnicalGlossary".

..  code-block:: GlossaryScript

    glossary model CyberForum


    //------------------------------------------------------------
    //   Glossaire du domaine
    //------------------------------------------------------------

    package GlossaireDuDomaine

    Forum
        | Outil de commnication asynchrone basé sur l'utilisation
        | par des `Abonnes` de `Messages` organisés en `Fils`.

    Fil
        | Séquence de messages en réponse à un `Initial`. Un fil
        | peut être `Bloque` ou `Ouvert` et est identifié par
        | un `Theme` et un ensemble de `Cles`.
        translations
            fr: "fil de discussion"
            en: "thread"
            es: "conversacion"
    ...

    //------------------------------------------------------------
    //   Glossaire technique
    //------------------------------------------------------------

    package GlossaireTechnique

    MVC
        | Patron de conception utilisé lors de la définition
        | d'interface homme machine.



    ...

.. index::
    single: Package; Inline package
    single: Inline package

Inline packages
'''''''''''''''

Note that an *entry* can be assigned to a particular *package*
using the ``package`` keyword. In that case the specification
overrides the current package. For instance in the following
example the entry One is in package ``Numbers``:

..  code-block:: GlossaryScript

    ...
    package Letters              // Toplevel package

    Alpha

    One
        package: Numbers         // Inline package

    Beta


Examples
--------

A complete, yet meaningless, example of glossary is given below.

..  code-block:: GlossaryScript

    glossary model Medium
        | ceci `est` la description de `un` élément
        | dans `un` contexte `uno` et `deux`
        | `un` `test`

    Trois
        | a
        package: technical
        synonyms: Uno One
        inflections: unite uns
        label: "un"
        translations
            en: ""
            es: ""


    Reference
        |
        | `une` `reference` est un peu plus que
        | `deux` mot. Attention à l'`indentation`
        | qui doit être toujours de `huit` espaces.
        synonyms : a b c
        package : a


    Deux
        | ceci est la description de `un` élément
        | dans `un` contexte `uno` et `deux`
        | `un` `test`
        | trois
        package: a

    ZIO
        | packaef
        package: b

    ODK
        | Order Designed Kant
        package: a

