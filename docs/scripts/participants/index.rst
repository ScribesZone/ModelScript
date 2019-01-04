.. .. coding=utf-8

.. highlight:: ParticipantScript

.. index::  ! .pas, ! ParticipantScript
    pair: Script ; ParticipantScript

.. _ParticipantScript:

ParticipantScript
=================

Examples
--------

::

    participant model Demo

    import glossary model from '../glossaries/glossaries.gls'

    //=========================================================================
    // "Class" level participants
    //-------------------------------------------------------------------------
    // "Actors" are defined by UML usecase model ; they represent (classes of) users.
    // "Stakeholders" have some interest in the system and/or its development.
    // "Team roles" collaborate to design and develop the system/
    //=========================================================================


    //--- actors --------------------------------------------------------------

    actor Cashier
        | Cashiers are employee of `Cinemas`. The role of `Cashiers`
        | is to sell `Ticket` to `Spectators`. They also manage
        | `Subscriptions`. To perform these tasks `Cashiers` should have a
        | desktop application at their disposal.

    actor HighCashier < Cashier
        | HighCashiers can cancel `Transactions` and launch
        | `MoneyBack` operations.

    actor Client
        | Clients are people that interact with the web interface
        | of the system or that take their `Ticket` at a
        | `VendingMaching`. Most of them do not know the system,
        | or experienced have less than




    //--- stakeholders ----------------------------------------------------

    stakeholder role Treasurer
        | The role of treasurers is to check that all `FinancialTransactionq`
        | processed by the system are accurate.

    stakeholder role SecurityManager
        | The role of the SecurityManager is to ensure the security in all
        | `Cinemas` and in particular in all `Rooms`. It should be possible
        | for example to inform SecurityManagers when an accident occur
        | in some `Room` or when a `Cinema` is overcrowded.




    //--- team roles ------------------------------------------------------

    team role Developer
        | A developer is responsible to design, develop, test and
        | maintain models and pieces of code.

    team role QualityManager
        | The QualityManager is responsible to define, with other
        | members of the development team, `QA` standard.
        | She also monitors `QC` process although she can to delegate
        | actual controls to other team members.
        |
    team role QualityMaster < QualityManager
        | A `QualityMaster` has all duties and privileges of
        |`QualityManager` but she also has the power to change
        | the content of `QA` and `QC` standard.

    team role ScrumMaster
        | The `ScrumMaster` is the team role responsible for
        | ensuring the team lives agile values and principles and
        | follows the processes and practices that the team
        | agreed they would use.
        | The responsibilities of this role include:
        | * clearing obstacles,
        | * Establishing an environment where the team can be effective
        | * Addressing team dynamics
        | * Ensuring a good relationship between the team and
        |   product owner as well as others outside the team
        | Protecting the team from outside interruptions and distractions.

    team role ProductOwner
        | The `ProductOwner` responsibility is to have a vision of
        | what she wishes to build, and convey that vision to the
        | `ScrumTeam`.


    //=========================================================================
    //   "Instance" level participants
    //-------------------------------------------------------------------------
    // Both personae and persons are at the instance level: they belong to
    // one of many participant class (actor, stakeholder or team role)
    // Personae are fictional characters that serve as instance of actors.
    // Persons are real-life people.
    //=========================================================================


    person marieDupont : Developer, QualityManager
        name : "Marie Dupont Laurent"
        trigram : MDL
        portrait : './mdupont.png'


    persona marco : Cashier, Client
        name : "Marco Gonzales"
        trigram : MGS
        portrait : './mdupont.png'
        | Marco is 45 years old.
        | He is used to computers and phones.
        | Some more description about marco
        attitudes
            | marco likes playing football.
            | He also loves eating pizza and playing with this
            | damned computer system.
        aptitudes
            education
                | master software engineering (1992)
                | PhD in medio chemicals (1999)
            languages
                | english (fluent)
                | spanish (novice)
            age : 45
            disabilities : "blind"
            learning ability : low
            | Marco is kind to learn but he also knows already
            | very much.
        motivations
            why
                | Marco is really reluctant to use the system.
                | Her boss, anna, told him that he will be fired
                | if he do not get good results.
            level : low
            kind : obliged
            | Some additional remark or documentation
        skills
            | Marco is an expert in playing with the mouse.
            level : novice
            culture
                | occidental
            modalities
                "labtop" : expert
                "smartphone" : novice
                "iPhone 10.3" : expert
            environments
                "Ubuntu" : expert
                "Windows" : intermediate
                "Android 18.5" : novice


    adhoc persona jean : Cashier, Client
        | Jean is 50 years old.


ParticipantScript
-----------------

The participant model aims to define all kinds of participants involved
somehow in the software project. This could be either because they
will *use* the system or because they are implicated in its design.

Concepts
--------

* actors
* stakeholders
* team role
* person
* persona

Dependencies
------------

The graph below show all language depdencies.

..  image:: media/language-graph-pas.png
    :align: center


..  _`usecase diagrams`: https://www.uml-diagrams.org/use-case-diagrams.html