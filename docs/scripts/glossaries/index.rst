.. .. coding=utf-8

.. highlight:: GlossaryScript

.. index::  ! .gls, ! GlossaryScript
    pair: Script ; GlossaryScript

.. _GlossaryScript:

GlossaryScript
==============

Examples
--------

A complete, yet meaningless, example of glossary is given below. Note
that many terms should be defined as they are referenced in definitions.

..  code-block:: GlossaryScript

    glossary model Medium
        | `Description` de `un` élément
        | dans `un` contexte `uno` et `deux`
        | `un` `test`


    //------------------------------------------------------------
    //   Glossaire du domaine
    //------------------------------------------------------------

    package GlossaireDuDomaine

    FilDeDiscussion
        | Suite ordonnée de `Messages`
        synonyms: Uno One
        inflections: unite uns
        texts:
            fr: "Fil de discussion"
            en: "Thread"

    Reference
        | Mot ou suite de mots faisant référence à
        | un `Concept` déjà défini. Attention à l'`Indentation`
        | qui doit être toujours de `huit` espaces.
        synonyms : a b c

    //------------------------------------------------------------
    //   Glossaire technique
    //------------------------------------------------------------

    package GlossaireTechnique

    MVC
        | Patron de conception utilisé lors de la définition
        | d'interface homme machine.
        | Voir https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller
        | In the context of this project ...

GlossaryScript
--------------

The ``GlossaryScript`` language, as defined below, allows to express
*glossaries*. Various glossaries can be defined (for instance
a domain glossary and a technical glossary) but all glossaries
are defined in the same file. Packages can be used to split this file.
Glossary scripts are to be save with the ``.gls`` extension.

.. index:: ! Glossary


Concepts
--------

A **glossary** is a collection of **entries** optionally organized into
**packages**. The goal of a **glossary** is to define all **terms**
used in the context of a given project.

In essence a **glossary** is:

*   a set of **entries** composed by a **main term** and
    **alternative terms** (**synonyms**, **abbreviations**, etc.)

*   the definition of relationships between all these **terms**,

.. index:: ! Entry
    single: Term
    single: Term; Main term (term)

Entries
-------

An **entry** is basically:

* a selected **main term** (e.g. ``Fil`` in the example below)
* a set of **alternative terms** (**synonyms**, **abbreviations**, etc.),
* a **definition** that fits for all the **terms**,
* some optional textual représentation **translations**.

..  code-block:: GlossaryScript

    Fil
        | Séquence de `Messages` en réponse à un `Initial`. Un fil
        | peut être `Bloque` ou `Ouvert` et est identifié par
        | un `Theme` et un ensemble de `Cles`.
        synonyms: Discussion, FilDeDiscussion
        inflections; Fils
        translations
            fr: "fil de discussion"
            en: "thread"
            es: "conversacion"
    ...

The **main term** (``Fil`` here) is the one that is expected to be
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
        ...
    Fil
        ...
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


.. _GlossaryScript_Rules:

Rules
-----

Les règles suivantes doivent être appliquées dans l'élaboration
des glossaires.

*   Dans les définitions, les références à d'autres termes du
    glossaire doivent être entre backquotes (p.e. `Backquote`).
    Ces termes doivent être définis.

*   Les définitions doivent commencer par une forme nominale ;
    tout comme dans un dictionnaire. La définition
    *"Singe : Animal ..."* est adaptée. Le premier terme ("Animal" ici)
    peut faire partie du glossaire entre backquotes ou être un terme
    d'usage courant (sans backquotes).

*   Toutes les définitions doivent correspondre au contexte
    particulier du projet. Omettre les définitions générales.
    Par exemple "Personne : Etre humain" n'apporte rien si le terme
    "Personne" n'a pas de signification différente de "personne" d'usage
    courant. Mettre "Personne" dans le glossaire s'il s'agit d'un
    terme spécifique au projet.

.. _GlossaryScript_RewritingTexts:

Rewriting texts
---------------

Au fur et à mesure qu'un glossaire est défini, il faut réécrire les
texte utilisant "informellement" le glossaire. En pratique pour chaque
terme appraissant dans un texte il faut déterminer s'il s'agit :

*   d'un terme d'usage général : aucune action n'est nécessaire.

*   d'un terme du domaine mais non défini : l'ajouter au glossaire.

*   d'un terme déjà défini comme terme principal dans le glossaire.
    il faut alors créer une référence (entre backquotes) vers ce terme.

*   d'un synonyme déjà défini : il faut le remplacer par le terme
    principal.

Ce travail de réécriture / définition du glossaire est bien évidemment
itératif. L'objectif final est d'obtenir des textes les moins ambigüs
et plus cohérents possible avec le glossaire.


.. _GlossaryScript_RewritingIdentifiers:

Rewriting identifiers
---------------------

La plupart des identificateurs (UML, Class, Java, SQL, etc.) devraient
faire référence à un ou plusieurs terme d'un glossaire du domaine
et/ou technique. C'est le cas par exemple pour l'identificateur suivant:

    getCartLayout

Le term ``Cart`` provient sans doute du glossaire du domaine alors que
``Layout`` peut provenir d'un domaine technique correpondant à un
framework utilisé.

Dans certains cas des abbréviations sont utilisés pour obtenir des
identificateurs plus cours. Celles-ci doivent être ajoutées dans le
glossaire technique (e.g. ``DAO``) ou dans le glossaire de domaine
(``num`` pour ``numero``). Le glossaire doit assurer l'usage des termes
de manière homogéne est consistante dans tous les modèles et dans tous
le code.

Un identificateurs qui ne fait référence ni au domaine ni aux
aspects techniques, est sujet a suspiscion.

Dans tous les cas il est fondamental lorsque les glossaires chanqent
ou lorsque de nouveaux indentificateurs sont définis, de s'assurer de
l'alignement entre glossaire et autre artefacts.

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
