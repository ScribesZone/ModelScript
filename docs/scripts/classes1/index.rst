.. .. coding=utf-8

.. highlight:: ClassScript

.. index:: ! .cl1, ! ClassScript1
   single: Script ; ClassScript1

.. _ClassScript1:

ClassScript1
============

Class models, as implemented here, are subsets of UML class models. A class
model is defined through a series of *classes*, *associations* and
*enumerations*.


Dependencies
------------

The graph below show all language dependencies.

..  image:: media/language-graph-cls.png
    :align: center


ClassScript1
------------

CLassScript is a textual notation for UML `class diagrams`_.
In the current version of ModelScript, called ModelScript1, the
``ClassScript1`` language is a subset of the `USE OCL`_ language.
ClassScript1 different very slightly:
* some annotations are added inside USE OCL comments (,
* only
Class script is a (very slightly) augmented version of the
class language. While in the context of USE the
``.use`` extension is used, ``.cls`` is the extension of class scripts.

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
            _name : String --@ {id} {derived} {optional}
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




..  _`USE OCL`: http://sourceforge.net/projects/useocl/

.. _`class diagrams`: https://www.uml-diagrams.org/class-diagrams-overview.html