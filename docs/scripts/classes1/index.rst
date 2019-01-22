.. .. coding=utf-8

.. highlight:: ClassScript1

.. index:: ! .cl1, ! ClassScript1
   single: Script ; ClassScript1

.. _ClassScript1:

ClassScript1
============

Examples
--------

..  note::
    The following example is absolutely meaningless.
    It is provided here just to give a flavor of the ClassScript1 syntax.

..  code-block:: ClassScript1

    --@ class model Jungle
    --@ import glossary model from "../glossaries/glossaries.gls"

    model Jungle

    enum Season {
        spring,
        summer
    }

    class Yellow
    end

    class Banana < Yellow
        --| A Banana is a nice Fruit that growths
        --| in the forest.
        attributes
            _name_ : String --@ {id} {derived} {optional}
            length : Integer
                --| the length of the banana expressed in milimeters.
            size : Real
            frozen : Boolean
            expirationDate: String --@ {Date}
            growthTime : Season
    end

    association Owns
        --| A person owns some cars if he or she
        --| bought it and didn't sell it.
        between
            Person [1] role owner
            Car[*] role properties
                --| A person can have several
                --| properties if he or she's lucky
    end

    associationclass Hate
        between
            Monkey [*] role monkeys
            Snake [*] role snakes
        attributes
            reason : String
            intensity : Integer
    end

    --@ constraint SmallBananas
    --@     scope
    --@         Banana.size
    --@         Banana.length
    --@     | Bananas are longer than their length.

    context self : Banana
    inv SmallBananas : self.size > self.length

    --@ constraint MomentConcerne
    --@     scope
    --@         Atelier.dateDeDebut
    --@         Atelier.dateDeFin
    --@         Concerne
    --@         Emprunt.dateDeSortie
    --@     | Si un emprunt concerne un atelier alors cet
    --@     | emprunt a eu lieu dans la période correspondant à l'atelier.

ClassScript1
------------

*ClassScript* is a textual notation for UML `class diagrams`_.
In the current version of ModelScript, the``ClassScript1`` language is
actually a "augmented subset" of the `USE OCL`_ language.
ClassScript1 differs only very slightly from `USE OCL`_:

*   annotations. Two kinds of annotations are added as comments:

    *   ``--|`` stands for a ModelScript documentation.
    *   ``--@`` are for other ModelScript code.

*   restrictions: ClassScript1 does not support qualified associations,
    and other features such as post-conditions or pre-conditions.

While in the context of `USE OCL`_ the ``.use`` extension is used,
``.cl1`` is the extension of ClassScripts1 scripts.

Tooling
-------

Analyzing models
''''''''''''''''

ClassScript1 models can be analyzed with the `USE OCL`_ tool.
When using the :ref:`ModelScript Method<ModelScriptMethod>`
the following command line should be entered in a terminal
(assuming that the current
directory is the root directory of the modeling project):

..  code-block:: none

       use -c classes/classes.cl1

The interpreter check that there is no errors such as
syntax errors and type errors.
If no errors are displayed, then the class model is correct.

Generating diagrams
'''''''''''''''''''

Creating UML class diagrams is possible using the `USE OCL`_ tool:

..  code-block:: none

    use -nr classes/classes.cl1

Refer to the page "`creating UML class diagrams`_" for more
information.

When using the :ref:`ModelScript Method<ModelScriptMethod>` the
layout of the class diagram have to be saved in the file
``classes/diagrams/classes.cld.clt``. The diagram has to be
saved in the file ``classes/diagrams/classes.cld.png``.

Concepts
--------

A class model is based on the following concepts:

* enumerations,
* classes,
* attributes,
* associations,
* association classes,
* constraints.

Enumerations
------------

..  code-block:: ClassScript1

    enum Season {
        --| Documentation of the enumeration
        --| Explains what is a season.
        winter,
            --| Documentation of the
            --| winter value
        autumn,
            --| Documentation of the autumn value
        spring,
        summer
    }


Classes
-------

UML class diagram:

..  image:: media/USEOCLClasses.png
    :align: center


ClassScript1 (based on USE OCL):

..  code-block:: ClassScript1

    class Yellow
        --| Documentation of the
        --| yellow class
    end

    abstract class Something
        --| Something is an abstract class
    end

    abstract class Fruit < Something
        --| Fruits are particular cases of Something
    end

    class Banana < Fruit, Yellow
        --| Bananas are both fruits and
        --| yellow things.
    end


Attributes
----------

ClassScript (USE OCL):

..  code-block:: ClassScript1

    class Banana
        --| A Banana is a nice Fruit that growths
        --| in the forest.
        attributes
            _name_ : String --@ {id} {derived} {optional}
                --| A banana always have nice names.
            length : Integer
                --| The length of the banana
                --| is between 5 and 40
            size : Real
            frozen : Boolean
            expirationDate: String --@ {Date}
            growthTime : Season
            remainingDays : Integer
    end

:Attribute types:

    Attributes can have only one of those type:
    *   an enumerations,
    *   ``Boolean``,
    *   ``Integer``,
    *   ``Real``,
    *   ``String``,
    *   ``Date``,
    *   ``DateTme``,
    *   ``Time``.

:Dates:

    Natively there is no ``Date``, ``DateTime`` or ``Time`` data types in
    `USE OCL`_.
    Attributes have to be defined as ``String`` and an
    ``{Date}``, ``{DateTime}`` or ``{Time}`` annotation has to be added
    as shown in the example above.
    Attribute values (in object models for instance) have then to be
    represented in the following format:
    ``2020/12/23`` for Date, ``2020/12/23-23:50:59`` for DateTime,
    and ``23:00`` for Time. This format allows date comparisons although
    no other computation is available.

Associations
------------

UML class diagram:

..  image:: media/USEOCLAssociationUSE.png
    :align: center

ClassScript (USE OCL):

..  code-block:: ClassScript1

    association Owns
        --| A person owns some cars if he or she *
        --| bought it and didn't sell it.
        between
            Person [1] role owner
            Car[*] role properties
                --| A person can have several
                --| properties if he or she's lucky
    end

Note that the roles order is important. In the example above the
association reads "(an) owner Owns (some) ownedCars": the first
role is the subject of the verb, the second role is the complement.
The role order is also when creating links in object diagrams.

Association Classes
-------------------

UML Diagram:

..  image:: media/USEOCLAssociationClassUSE.png
    :align: center

Class Script (USE OCL):


..  code-block:: ClassScript1

    associationclass Hate
        --| Some monkeys hate some snakes.
        --| That's life. Life in the jungle.
        between
            Monkey [*] role monkeys
            Snake [*] role snakes
        attributes
            reason : String
            intensity : Integer
    end

Constraints
-----------

`USE OCL`_ supports 3 kinds of constraints : invariant, pre-conditions and
post-conditions. ClassScript1 is based only on invariants.

Using ClassScript1, constraints can be defined in natural language, using
a particular format, and then using OCL.

Natural Language Constraints
''''''''''''''''''''''''''''

Ecrire les contraintes en Langue Naturelle est une étape indispensable
avant de formaliser ces contraintes en OCL. C'est en effet le client
qui exprime ces contraintes ou sinon qui les valide.

Structure
.........

Chaque contrainte doit comporter les éléments suivants :

*   un **identificateur** (p.e. ``FormatMotDePasse``),

*   une **portée** d'application, c'est à dire la partie du diagramme
    de classes qui permet d'expliquer "où se trouve" la contrainte.
    La zone est représentée par une liste de noms de :

    * **classes** (p.e. ``Personne``),
    * **associations** (p.e. ``Concerne``),
    * **attributs** (p.e. ``Personne.nom``),
    * **roles** (p.e. ``Personne.parents``).

*   une **description** en langue naturelle. Idéalement la description
    doit pouvoir être lue par le "client' aussi bien que par les
    développeurs. La description doit à la fois faire référence au
    glossaire, mais également autant
    que possible aux identificateurs se trouvant dans le diagramme. La
    correspondance entre les éléments décrivant la portée du modèle doit
    être claire et non ambigüe.

Example
.......

Dans cet exemple la contrainte est un invariant. Ce code est à ajouter
en fin du modèles de classes, à la fin du fichier ``classes.class``.

..  code-block:: ClassScript1

    --@ invariant MomentConcerne
    --@     scope
    --@         Atelier.dateDeDebut
    --@         Atelier.dateDeFin
    --@         Concerne
    --@         Emprunt.dateDeSortie
    --@     | Si un emprunt concerne un atelier alors cet
    --@     | emprunt a eu lieu dans la période correspondant à l'atelier.

Dans l'exemple ci-dessus la notion de période n'est pas nécessairement
claire et la locution "a eu lieu" non plus. Il est possible de préciser
la phrase ainsi :

..  code-block:: ClassScript1

    --@     | Si un emprunt concerne un atelier alors cet
    --@     | la date de sortie de l'emprunt a eu lieu entre la date de début
    --@     | de l'atelier et sa date de fin.

Method
......

L'une des façons de trouver les contraintes et de passer un à un les
différents éléments d'un modèle de classes. Il s'agit de lister les
contraintes portant sur :

* **un attribut**, typiquement les contraintes de domaine (e.g. *age>0*)
* **plusieurs attributs** d'une classe (e.g. ``min<=max``)
* **une association** (e.g. *le père d'une personne est plus agé*)
* **plusieurs associations** (e.g. *le salaire d'une personne employée dans une
  entreprise ne peut pas être supérieur à 5% du buget du projet sur lequel
  elle travaille, sauf si elle est classée A*).

Lorsque plusieurs associations forment un cycle il assez probable qu'une
ou des contraintes s'appliquent au sein de ce périmètre.


OCL Constraints
'''''''''''''''

The constraints expressed in natural language (see above) can then
be traduced in OCL (using `USE OCL`_)

Dependencies
------------

The graph below show all language dependencies.

..  image:: media/language-graph-cls.png
    :align: center


..  _`USE OCL`: https://scribestools.readthedocs.io/en/latest/useocl/index.html

.. _`class diagrams`: https://www.uml-diagrams.org/class-diagrams-overview.html

.. _`creating UML class diagrams`: http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams
