..  _`tâche projet.participants`:

tâche projet.participants
=========================

:résumé: L'objectif de cette tâche est de définir les
    membres de l'équipe ainsi que leurs rôles.

:langage: :ref:`ParticipantScript`
:résultat:
    * ``participants/participants.pas``

Introduction
------------

Les membres de l'équipe et leurs rôles font partie de la définition des
"participants" du projet. Il s'agit de définir leurs caractéristiques
principales dans le fichier ``participants/participants.pas``. Se reporter
à la documentation de :ref:`ParticipantScript` pour plus d'information.

(A) Rôles
---------

Définir les roles que peuvent jouer les membres de l'équipe en utilisant
les mots clés ``team role``. Un projet peut par exemple définir un
rôle ``IntegrationManager``. Indiquer brièvement quelles sont les
fonctions associées à chaque rôle. Des rôles externes à l'équipe
strictement parlant peuvent être définis, par exemple ``ConsultantBD``
pour un expert en base de données donnant des conseils sur les base de
données et/ou réalisant des audits sur ce thème.

Il est à noter qu'un rôle peut être joué par plusieurs membres et
inversemment qu'un membre peut jouer plusieurs rôles. De même une
personne peut jouer un rôle à un moment donné puis changer de rôle
par la suite. Tous ces rôles seront associés à la personne en
mentionnant si nécessaire ces changements la description de la personne.
Par exemple "| Integration Manager du 12/03/2020 au 17/03/2020".

Dans le cadre d'un projet "exploratoire", du point de vue de la
méthodologie, les rôles peuvent être définis au fur et à mesure du projet,

(B) Personnes
-------------

Les membres de l'équipe doivent être brièvement décrit : nom et trigramme.
Utiliser le mot clé ``person``. Indiquer le ou les rôles que chaque
personne a ou va jouer. Définir également les éventuels consultants
extérieurs ou toute autre personne impliquée dans le projet.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.