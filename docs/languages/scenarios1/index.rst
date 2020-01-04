.. .. coding=utf-8

.. highlight:: ScenarioScript1

.. index::  ! .sc1, ! ScenarioScript1
    pair: Script ; ScenarioScript1

.. _ScenarioScript1:


ScenarioScript1
===============


Exemples
--------

Le développement de scénarios peut se faire en 3 étapes :

*   (1) développement des **scénarios textuels**
    (phrases),

*   (2) développement des **scénarios états**
    (phrase+instructions),

*   (3) développement des **scénarios cas d'utilisation**
    (phrase+instructions+blocs).

Scénarios textuels
''''''''''''''''''

Les scénarios textuels sont des suites de **(phrases)**.

..  code-block:: ScenarioScript1


    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"

    --| phrase1
    --| phrase2
    --| phrase3
    --| phrase4
    --| phrase5
    --| phrase6
    --| phrase7
    --| phrase8

Scénarios états
'''''''''''''''

Les scénarios états sont caractérisés par l'état qu'ils font évoluer.
Concrètemment les scénarios états sont constitués de phrases annotées
par des instructions. Ces instructions correspondent à la l'évolution
au cours du temps d'un modèle d'objets. Les scénarios états
permettent de répondre à la question "comment l'état du système évolue ?".

..  code-block:: ScenarioScript1

    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"
    --@ import class model from "../../classes/classes.cls"

    --| phrase1
    --| phrase2
        ! instruction1
        ! instruction2
    --| phrase3
        ! instruction3
        ! instruction4
    --| phrase4
    --| phrase5
    --| phrase6
        ! instruction5
        ! instruction6
        ! instruction7
    --| phrase7
        ! instruction8
    --| phrase8

Comme le montre l'exemple ci-dessus certaines phrases peuvent ne
correspondre à aucun changement d'état.

Scénarios cas d'utilisation
'''''''''''''''''''''''''''

Les scénarios cas d'utilisation définissent "l'empreinte" des cas
d'utilisation sur les scénarios états. Chaque phrase/instruction
est positionnée par rapport au cas d'utilisation en cours.
Alors que les scénarios états permettent de répondre à la
question "comment le système évolue" les scénarios cas d'utilisation
permettent de répondre à la question "qui fait quoi et pourquoi ?".

..  code-block:: ScenarioScript1

    --@ scenario model S1
    --@ import glossary model from "../../glossaries/glossary.gls"
    --@ import class model from "../../classes/classes.cls"
    --@ import participant model from "../../participants.pas"
    --@ import usecase model from "../../usecases/usecases.uss"

    --@ context
        --| phrase3 (modifiée)
            ! instruction3
            ! instruction4

    --@ personnage1 va usecase1
        --| phrase1
        --| phrase2
            ! instruction1
            ! instruction2

    --| phrase4 (modifiée)
    --| phrase5

    --@ personage2 va usecase2
        --| phrase6
            ! instruction5
            ! instruction6
            ! instruction7
        --| phrase7
            ! instruction8

    --| phrase8

Les blocs ``context`` correspondent au contexte du scénarios, c'est à
dire à la construction de l'état initial. Ils s'agit de la modèlisation
de l'ensemble des informations existant avant que le scénario démarre.

Considérons un exemple où la phrase ``tim a 15 ans`` est suivie
de l'instruction ``tim.age := 15``. Première possibilité, la plus
probable, ces deux instructions font a priori partie du contexte.
Autre solution,
ces informations font partie d'un bloc cas d'utilisation si ``tim`` change d'age
durant le scénario (peu probable, mais cela dépend du scénario).

Bien évidemment dans les deux cas on suppose que
l'age de tim doit être modélisé pour le bon déroulement du scénario.
Si ce n'est pas le cas l'instruction ``tim.age := 15`` doit être éliminée
et la phrase ``tim a 15 ans`` doit être en dehors de tout bloc, au
premier niveau. Cette information est peut être importante pour le
scénario, même si elle n'a pas d'impact directe sur l'état du système.


Outils
------

Analyse de modèles
''''''''''''''''''

La conformité des modèles de scénarios par rapport au modèle de classes
peut être verifiée par l'outil `USE OCL`_ avec la même procédure que
pour :ref:`l'analyse des modèles d'objets<AnalyseDesModelesDObjets>`.

..  note::

    ATTENTION, la conformité avec le modèle de cas d'utilisation n'est
    pas vérifiée.

Génération de diagrammes
''''''''''''''''''''''''

Il est possible de générer un diagramme d'objets correspondant à l'état
final du scénario. Utiliser pour cela la même procédure que pour
:ref:`génerer un diagramme d'objet standard<GenerationDeDiagrammesDObjets>`.


Concepts
--------

Le langage ScenarioScript1 est basé sur les concepts suivants :

* les phrases
* les instructions
* les blocs de contexte
* les blocs de cas d'utilisation
* les scénarios textuels,
* les scénarios états,
* les scénarios cas d'utilisation

Dépendances
-----------

Le graphe ci-dessous décrit les dépendances entre langages.

..  image:: media/language-graph-scs.png
    :align: center

..  _`USE OCL`: http://sourceforge.net/projects/useocl/
