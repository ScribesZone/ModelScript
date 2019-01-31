.. .. coding=utf-8

.. highlight:: ScenarioScript1

.. index::  ! .sc1, ! ScenarioScript1
    pair: Script ; ScenarioScript1

.. _ScenarioScript1:


ScenarioScript1
===============


Examples
--------

Scenario development can be done in three stages:

* **textual scenarios** (sentences),
* **flat scenarios** (sentences+statements)
* **usecase scenarios** (sentences+statements+blocks)

Textual Scenarios
'''''''''''''''''

sentences

..  code-block:: ScenarioScript1


    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"

    --| sentence1
    --| sentence2
    --| sentence3
    --| sentence4
    --| sentence5
    --| sentence6
    --| sentence7
    --| sentence8

Flat scenarios
''''''''''''''

sentences+statements

..  code-block:: ScenarioScript1

    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"
    --@ import class model from "../../classes/classes.cls"

    --| sentence1
    --| sentence2
        ! statement1
        ! statement2
    --| sentence3
        ! statement3
        ! statement4
    --| sentence4
    --| sentence5
    --| sentence6
        ! statement5
        ! statement6
        ! statement7
    --| sentence7
        ! statement8
    --| sentence8

Usecase scenarios
'''''''''''''''''
sentences+statements+blocks

..  code-block:: ScenarioScript1

    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"
    --@ import class model from "../../classes/classes.cls"
    --@ import participant model from "../../participants.pas"
    --@ import usecase model from "../../usecases/usecases.uss"

    --@ context
        --| sentence3 (changed)
            ! statement3
            ! statement4

    --@ persona1 usecase1
        --| sentence1
        --| sentence2
            ! statement1
            ! statement2

    --| sentence4 (changed)
    --| sentence5

    --@ persona2 usecase2
        --| sentence6
            ! statement5
            ! statement6
            ! statement7
        --| sentence7
            ! statement8

    --| sentence8

Tooling
-------

Analyzing models
''''''''''''''''

The conformity of scenario models with class models can be checked with
the `USE OCL`_ tool. Analyzing scenario models is just like
:ref:`analyzing object models<AnalyzingObjectModels>`.

Generating models
'''''''''''''''''

It is possible to generate an object diagram representing the state at
the end of a scenario. Creating such object diagrams is possible.
Check how to :ref:`generate object diagram<GeneratingObjectDiagrams>`.


Concepts
--------

ScenarioScript1 models are based on the following concepts:




Dependencies
------------

The graph below show all language depdencies.

..  image:: media/language-graph-scs.png
    :align: center

..  _`USE OCL`: http://sourceforge.net/projects/useocl/
