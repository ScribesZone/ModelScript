.. .. coding=utf-8

.. highlight:: ClassScript

.. index:: ! .cl1, ! ClassScript1
   single: Script ; ClassScript1

.. _ClassScript1:

ClassScript1
============

*ClassScript* is a textual notation for UML `class diagrams`_.
In the current version of ModelScript, the``ClassScript1`` language is
actually a "augmented subset" of the `USE OCL`_ language.
ClassScript1 differs only very slightly for `USE OCL`_:

* extensions: a few annotations are added inside USE OCL comments (``--``),
* restrictions: ClassScript1 does not support qualified associations.

While in the context of `USE OCL`_ the ``.use`` extension is used,
``.cl1`` is the extension of ClassScripts1 scripts.

Examples
--------

..  note::
    The following example is absolutely meaningless.
    It is provided here just to give a flavor of the ClassScript1 syntax.

..  code-block:: ClassScript1

    --@ glossary model CASESTUDY
    --@ import glossary model from "../glossaries/glossaries.gls"

    model Jungle

    enum Season {
        winter,
        autumn,
            --| Documentation of the autumn value
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
                --| The name is key.
            length : Integer
            size : Real
            frozen : Boolean
            expirationDate: String --@ {date}
            growthTime : Season
            remainingDays : Integer
    end

    association Owns
        --| A person owns some cars if he or she *
        --| bought it and didn't sell it.
        between
            Person [1] role owner
            Car[*] role properties
                --| A person can have several
                --| properties if he or she's lucky
    end

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

    --@ invariant SmallBananas
    --@     scope
    --@         Banana.size
    --@     | Bananas are quite small

    context self : Banana
        inv self.size < 10

    --@ invariant MomentConcerne
    --@     scope
    --@         Atelier.dateDeDebut
    --@         Atelier.dateDeFin
    --@         Concerne
    --@         Emprunt.dateDeSortie
    --@     | Si un emprunt concerne un atelier alors cet
    --@     | emprunt a eu lieu dans la période correspondant à l'atelier.


Concepts
--------

A class model is based on the following concepts:

* enumerations,
* classes,
* attributes,
* associations,
* association classes
* constraints

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


ClassScript (USE OCL):

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
            expirationDate: String --@ {date}
            growthTime : Season
            remainingDays : Integer
    end

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


..  _`USE OCL`: http://sourceforge.net/projects/useocl/

.. _`class diagrams`: https://www.uml-diagrams.org/class-diagrams-overview.html