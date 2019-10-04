..  _`tâche bd.relations.classes`:

tâche bd.relations.classes
==========================

:résumé: L'objectif de cette tâche est d'annoter le modèle de
    classes conceptuel en un modèle de données pour base de données.

:langage: :ref:`ClassScript1`
:résultat:
    * ``classes/classes.cl1``


Introduction
------------

Le modèle de classes élaboré jusqu'à présent était un modèle
conceptuel, c'est à dire décrivant des concepts du domaine de
manière abstraite ; et ce indépendamment de toute considération
technique.

Il s'agit maintenant de transformer ce modèle abstrait en un modèle
de de classe pour base de données ; plus particulièrement de
préparer le modèle classes avant de le transformer en modèle
de relations.

(A) Identifiants
----------------

Pour chaque classe, il s'agit de définir quel(s) attribut(s)
peuvent appatenir à une clé. Chacun de ces attributs doit être
entouré par des caractères soulignés ('_'). Par exemple l'attribut
``login`` devient ``_login_`` s'il s'agit d'un identifiant. Cette
convention n'est pas parfaite, car dans
certains cas une "clé" peut être composée, dans d'autres cas plusieurs
"clés" peuvent exister. Quoi qu'il en soit, cette convention sera
utilisée à ce niveau, sachant que les définitions des identifiants seront
raffinées et précisées lors de la transformation en modèle de relations.

(B) Composition
---------------

Dans certains cas les objets d'une classe doivent être identifiés
non pas de manière directe, avec son/ses identifiants, mais par
rapport aux objets composites les contenant.

Par exemple une salle peut être identifiée en partie par son numéro,
par exemple 13, mais aussi le numéro de l'étage à laquelle elle se trouve,
par exemple 6. Dans cet exmple l'identifiant de la salle est le couple
( 6 , 13 ).

Dans le cas du modèle de base de données, l' "importation" de
l'identifiant du composite se fait dans le cadre d'association de
composition. Il est alors nécessaire, parfois, de changer une
association "standard" en une composition.

Par exemple : ::

    association ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances
    end

peut être changé en : ::

    composition ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances
    end

Même si cette composition pourrait sembler contestable dans le cas d'un
modèle conceptuel, cette modification peut être valide dans un modèle
technique, ici dans le cadre de la conception de bases de données.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.
