..  _`tâche cu.scenarios`:

tâche cu.scenarios
==================

:résumé: L'objectif de cette tâche est d'aligner les scénariosn définis
     jusque là avec les cas d'utilisation.

:langage: :ref:`ScenarioScript1`, :ref:`ParticipantScript`
:artefacts:
    * ``participants/participants.pas``
    * ``scenarios/n/scenario.scs``

Introduction
------------

Les scénarios réalisés jusque là étaient caractérisés par le modèle
d'objets qu'ils généraient à la fin de leur exécution.
Il s'agissait d'une liste "à plat" de créations d'objets et de liens.
Dans cette tâche les scénarios sont considérés comme un emboîtement
d'instances de cas d'utilisation.

Les modèles de scénarios à raffiner/compléter se trouvent dans les fichiers
``scenarios/s<N>/s<N>.sc1`` (où ``<N>`` est un entier). Se reporter à la
documentation de :ref:`ScenarioScript1` lorsque nécessaire.

(A) Personnages
---------------

Dans un premier temps il s'agit de repérer dans les scénarios quels
"personnages" interagissent **directement** avec le système. Ces
personnages sont, par définition, des instances d'acteurs (ajouter
les acteurs si nécessaire).

A chaque fois qu'un personnage est identifié celui-ci doit être ajouté au
modèle de participants (fichier ``participants/participants.pas``).

Par exemple le personnage ``marie`` peut jouer le rôle de
``Bibliothecaire`` dans un scénario : ::


    persona marie : Bibliothecaire

Les personnages comme "marie" peuvent être caractérisés par de nombreuses
propriétés (voir l'exemple dans la documentation de
:ref:`ParticipantScript`).
Ces propriétés seront nécessaires par exemple lors de la conception
d'Interface Homme Machine (IHM). Ici on se contentera d'une brève
description pour chaque acteur.

(B) Décomposition
-----------------

Chaque scénario "à plat" doit ensuite être décomposé sous forme d'une
série d'instances de cas d'utilisation. Autrement dit il s'agit de
repérer dans le texte des scénarios quels cas d'utilisation
sont mis en oeuvre.


Soit le fragment ci-dessous : ::

    ...

    --@ marie va RentrerUneOeuvre
        --| Stéphanie rend le disque "High way to hell" [A24].
        --| Marie scanne le disque qui devient à nouveau disponible [A26].
            ! insert (b4885, bib14) into EstDisponibleA
            ! delete (steph, emp1) from AEmprunte

    ...

Dans cet exemple le personnage ``marie`` intéragit (mot-clé ``va``)
avec le cas d'utilisation ``RentrerUneOeuvre``. Cette interaction
modifie l'état du système via les instructions ``! insert ...`` et
``! delete ...``. L'indentation montre que les phrases/instructions
avant et après ne font pas partie de cette instance de cas d'utilisation.

Les règles suivantes doivent être respectées :

*   le cas d'utilisation ``RentrerUneOeuvre`` doit être défini dans
    le modèle de cas d'utilisation,

*   ``marie`` doit être un personnage existant dans le modèle
    de participant et

*   ``marie``doit correspondre à un acteur (``Bibliothecaire`` ici)
    pouvant exécuter le cas d'utilisation (une ``Bibliothecaire`` peut
    effectivement ``RentrerUneOeuvre``).


(C) Contexte
------------

Dans cette sous-tâche il s'agit d'isoler les instructions qui font
partie du "contexte" plutôt que du flôt normal du scénario. Considéront
par exemple le cas d'une réservation de salle. L'instruction
``create s203 : Salle`` ne fait pas partie du cas
d'utilisation ``ReserverUneSalle`` car la salle ``s203`` pré-existe à
l'exécution du cas d'utilisation : la salle n'est pas créée, elle est
juste réservée ! Le fait que la salle 203 existe fait partie du "contexte".
Une telle information (la phrase et les instructions correspondantes)
doivent être inclues dans un block ``context``. L'exemple ci-dessous
montre la séparation entre un block contextuel et un block de
cas d'utilisation. ::

    --@ context
        --| La salle 203 peut accueillir 30 personnes [A6].
            ! create s203 : Salle
            ! s203.capacite := 30
        --| Elle se trouve dans le batiment C [A7]
            ! create batC : Batiment
            ! insert (s203, batC) into EstDansBatiment

    ...

    --@ toufik va ReserverUneSalle
        --| Toufik décide de réserver la salle 203 [A21][A22].
            ! insert (toufif, s203) AReservee
            ! s203.reservations := s203.reservations + 1
        --| Il indique que l'évenement qu'il prépare est payant [A23].
            ...

    ...


Il s'agit de :

*   déplacer ces blocks en début de scénario et

*   vérifier que cela ne provoque aucune erreur dans la "compilation"
    du scénario.

(D) Texte
---------

Le texte fourni initialement et qui a donné lieu au scénario états doit,
dans certains cas, être remanié. Par exemple de déplacement de blocks
contextuels en début de scénario peut impliquer un remaniement de certaines
phrases. Il en est de même lorsque les limites des scénarios sont établies.

Quelque en soit la raison, certaines phrases peuvent être déplacées,
découpées, ou même supprimées.

Il n'y a pas de règle pour le remaniement du texte. L'équipe de
développement, mais aussi le client, doivent cepandant pouvoir "lire" et
utiliser le scénario tout au long du son cycle de vie. Une attention
particulière devra être portée aux élements de traçabilité
(e.g. ``[A12][A14-A19]``).

(E) Transformation
------------------

L'exemple ci-dessous résume le processus global :
* (1) définition des personnages (``persona x : A``),
* (2) identification des instances de cas d'utilisation (``x va y``),
* (3) extraction des instructions du contexte (``context``),
* (4) remaniement du texte.

::

    =========================== =========================================
      AVANT: Scénario (états)        APRES: Scénario (cas d'utilisation)
    =========================== =========================================

                                Modele de participant (participant.pas)
                                -----------------------------------------
                                        participant marie : Bibliotecaire
                                        participant toufik : Manager

                                        ...

                                Modèle de scenario (S<N>.sc1)
                                -----------------------------------------

    --| phrase1                 --@ context
    --| phrase2                     --| phrase3 modifiée
        ! instruction1                  ! instruction3
        ! instruction2                  ! instruction4
    --| phrase3
        ! instruction3          --@ toufik va ReserverUneSalle
        ! instruction4              --| phrase1
    --| phrase4                     --| phrase2
    --| phrase5                         ! instruction1
    --| phrase6                         ! instruction2
        ! instruction5
        ! instruction6          --| phrase4 modifiée
        ! instruction7          --| phrase5
    --| phrase7
        ! instruction8          --@ marie va RentrerUneOeuvre
    --| phrase8                     --| phrase6
                                        ! instruction5
                                        ! instruction6
                                        ! instruction7
                                    --| phrase7
                                        ! instruction8

                                --| phrase8

    =========================== =========================================

(F) Cas d'utilisation
---------------------

Vérifier (manuellement) que le modèle de scénarios est bien aligné
avec le modèle de cas d'utilisation.
Par exemple ``toufik va ReserverUneSalle`` implique qu'un
ChefBibliothequaire peut réserver une salle.


(G) Classes
-----------

Vérifier que le scénario est encore aligné avec le modèle de classes. ::

    use -qv Classes/classes.cls Scenarios/n/scenario.scn

Cette vérification a été faite précédemment avec le scénario états
mais il s'agit là de vérifier que la transformation ci-dessus n'a pas
généré de problèmes supplémentaires. Ce peut être le cas si le
réordonnancement des instructions n'est pas correct.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.