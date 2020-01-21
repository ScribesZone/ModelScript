..  _`tâche bd.sql.schema`:

tâche bd.sql.schema
===================

:résumé: L'objectif de cette tâche est d'implémenter le schéma
    SQL de la base de données.

:langage: SQL
:artefacts:
    * ``bd/sql/schema/schema.sql``

Introduction
------------

Il s'agit d'implémenter en SQL le schéma de la base de données. Si un
modèle de relations existe alors on cherchera a réaliser une traduction
aussi fidèle et homogène que faire se peut.

Le fichier ``bd/sql/schema/schema.sql`` fourni contient un exemple
de schéma écrit en SQL (un jeu de données est également fourni).
Dans un premier temps, ces ressources peuvent servir à comprendre/tester
la création de la base de données, réaliser éventuellement des premières
requêtes, etc. Bien évidemment **le contenu des fichiers fournis devra
ensuite être remplacé** par le code à produire dans cette tâche. Il est
conseillé de lire les tâches SQL avant de commencer.

(A) Schéma
----------

Implémenter le schéma relationnel en SQL revient concrètement
à exécuter différentes instructions ``CREATE TABLE``. Ces instructions
doivent être écrites dans le fichier ``schema.sql``.
Se référer à la documentation du SQBD utilisé pour connaître le détail de
la syntaxe SQL, les types de données disponibles, la manière d'écrire
les contraintes, etc.

Tester le schéma en executant le code avec une base de données vide.

(B) Automatisation
------------------

Un script de création ``bd/sql/cree-la-bd.sh`` a pour rôle d'automatiser
la création de la base de données à partir du schéma. Le contenu de
ce script est fourni pour le SGBD ``sqlite``. Il pourra dans ce cas être
utilisé tel quel. Si un autre SGBD est utilisé, ce script peut être
réécrit/adapté afin d'avoir une seule et unique commande pour créer
la base de données.

Avec sqlite entrer la commande suivante à partir du répertoire
``bd/sql/``: ::

    cree-la-bd.sh

Ce script crée une base de données vide ``sql/database.sqlite3`` et charge
le schéma ``bd/sql/schema/schema.sql``. L'exécution du script devrait
ressembler à cela : ::

    Clearing database ... done.
    Creating database schema ... done.
    Empty database created.

Si nécessaire se référer au contenu du script pour plus d'information ;
pour changer par exemple la localisation de la base de données. Si un autre
SQBD est utilisé le contenu de ce script devra être adapté.

Une fois la base de données créée utiliser le SGBD selectionné (ici
sqlite3) pour consulter le schéma et le contenu de la base de données.
Avec sqlite3 et la base de données fournie par défaut la session
suivante montre la liste des tables de la BD ainsi que le contenu de
l'une de ces tables. ::

    $ sqlite3 bd.sqlite3
    SQLite version 3.22.0
    Enter ".help" for usage hints.
    sqlite> .tables
    Cinemas     Frequents   IsOn        Movies      Opinions    Spectators
    sqlite> SELECT * FROM Cinemas ;
    sqlite>

Comme on peut le voir avec la dernière requête le contenu de la base
de données par défaut est vide. La :ref:`tâche bd.sql.jdd` montre comment
remplir la base avec un jeux de données (jdd).

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.