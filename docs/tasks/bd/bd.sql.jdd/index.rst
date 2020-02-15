..  _`tâche bd.sql.jdd`:


tâche bd.sql.jdd
================

:résumé: L'objectif de cette tâche est de définir des jeux
     de données (jdd) (positifs) pour la base de données SQL.

:langage: SQL
:artefacts:
    * ``bd/sql/jdd/jdd*.sql``

Introduction
------------

Des jeux de données (positifs) doivent être implémentés en SQL.

(A) Implémentation
------------------

Les jeux de données doivent être implémentés via des instructions
``INSERT``. Ces instructions doivent être écrites dans les fichiers
``bd/sql/jdd/jdd<N>.sql`` ou ``<N>`` est le numéro du jeu de données.

Voici a titre d'exemple un extrait d'un jeu de données :

..  code-block:: sql

    ---------------------------------------------------------------------------
    -- Cinemas
    ---------------------------------------------------------------------------

    INSERT INTO Cinemas VALUES ('Hoyts CBD','Sydney');
    INSERT INTO Cinemas VALUES ('Hoyts','Brisbane');
    INSERT INTO Cinemas VALUES ('Event Cinema Myer','Brisbane');
    INSERT INTO Cinemas VALUES ('Event Cinema','Cairns');
    INSERT INTO Cinemas VALUES ('Birch Carroll and Coyles','Brisbane');
    INSERT INTO Cinemas VALUES ('Event Cinema Red Center','Alice Spring');
    ...

..  note::

    Si des modèles d'objets ou des jeux de données relationnels ont été
    définis auparavant ces derniers doivent être réutilisés autant que
    possible.

(B) Chargement
--------------

Le script de création de base de données peut être utilisé pour charger
un jeu de données. Par exemple pour un jeu de données ``jdd1`` la création
de la base de données se fait avec la commande suivante
(dans l'exemple ci-dessous on suppose que le fichier ``jdd/jdd1.sql``
existe) : ::

    cree-la-bd.sh jdd1

Comme on s'intéresse dans cette tâche aux jeux de données positifs,
aucune erreur ne doit être détectée lors du chargement.

L'exécution du script ``cree-la-bd.sh`` avec le jeu de données
positif ``jdd1`` devrait ressembler à cela : ::

    Nettoyage de la base de données ... fait.
    Chargement du schéma ... fait.
    Chargement du jeu de données jdd1 ...fait.
    Jeu de données jdd1 chargé dans la base de données.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.