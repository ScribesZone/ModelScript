..  _`tâche cu.participants`:

tâche cu.participants
=====================

:résumé: L'objectif de cette tâche est de définir les acteurs
    et les personnages.

:langage:  :ref:`ParticipantScript`
:artefacts:
    * ``participants/participants.pas``


(A) Acteurs
-----------

Définir tout d'abord les "acteurs" qui interviendront par la suite
dans le modèle de cas d'utilisation. Donner pour chaque acteur un
nom (p.e. ``ResponsableDesAchats``) ainsi qu'une courte définition faisant
référence aux éléments du glossaire. Par définition un acteur intéragit
directement avec le système (via une interface), sinon il ne s'agit
pas d'un acteur.

(B) Personnages
---------------

Les "personnsages" sont des instances particulières d'acteurs. Ceux-ci
interviennent dans les modèles de scénarios. Repérer "qui", dans chaque
scénario, existant ou à définir, joue le rôle d'un acteur. Définir chaque
personnage en donnant a minima son nom et son type. Par exemple
``mario : ResponsableDesAchats``.

(C) Alignement
--------------

Les participants et les personnages pourront être définis "à la demande"
lors de la :ref:`tâche cu.preliminaire` ou de la
:ref:`tâche cu.scenarios`. Par la suite  il
s'agira  aussi d'aligner les participants au modèle de
permissions.

*In fine* le modèle de particiants doit être aligné avec les modèles
suivants:

* le modèle de cas d'utilisation
* les différents modèles de scénarios.
* le modèle de permission.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.