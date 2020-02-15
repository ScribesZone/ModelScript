..  _`tâche bd.sql.jdd.negatifs`:

tâche bd.sql.jdd.negatifs
=========================

:résumé: L'objectif de cette tâche est de définir des jeux
     de données négatifs pour la base de données SQL.

:langage: SQL
:artefacts:
    * ``bd/sql/jdd/jddn*.sql``

(A) JDD négatifs
----------------

Cette tâche fait suite à la :ref:`tâche bd.sql.jdd`.

Contrairement aux jeux de données positifs qui ne doivent produire
aucune erreur, les jeux de données négatifs doivent générer des erreurs
lorsque les contraintes associées au schéma ne sont pas respectées.

Les "violations" du schéma de données doivent être documentées
explicitement dans le jeu de données à l'aide d'annotations
``--@ violates``. Voici par exemple un extrait du jeu de données
``jddn1.sql`` :

..  code-block:: sql

    ...
    107   INSERT INTO Opinions VALUES ('Marie','The Inbetweeners 2','0');
    108
    109   --@ violates Opinions.PK
    110   INSERT INTO Opinions VALUES ('Marie', 'The Inbetweeners 2', '3');
    111
    112   --@ violates Opinions.Dom_stars
    113   INSERT INTO Opinions VALUES ('Marie','The Inbetweeners 2','===> VIOLATION <===');
    114
    115   --@ violates Opinions.FK_spectator
    116   INSERT INTO Opinions VALUES ('==> VIOLATION <==','The Inbetweeners 2','0');
    117
    118   --@ violates Opinions.FK_movie
    119   INSERT INTO Opinions VALUES ('Marie','==> VIOLATION <==','0');
    120   INSERT INTO Opinions VALUES ('Adrian','The Inbetweeners 2','0');
    121   INSERT INTO Opinions VALUES ('Phil','The Inbetweeners 2','2');
    ...

Chaque annotation ``--@ violates`` indique quelles erreurs sont censées
être produites lors de l'exécution de la ligne suivante. Comme on
peut le voir dans l'exemple ci-dessus le paramètre de chaque violation
correspond à un nom de contrainte défini dans le schéma.

Dans l'exemple le chargement du jeu de données ``jddn1.sql`` produit le
résultat suivant : ::

    $ cree-la-bd.sh jddn1

    Nettoyage de la base de données ... fait.
    Chargement du schéma ... fait.
    Chargement du jeu de données jddn1 ...Error: near line 23: UNIQUE constraint failed: Movies.title
    ...
    Error: near line 110: UNIQUE constraint failed: Opinions.spectator, Opinions.movie
    Error: near line 113: CHECK constraint failed: Dom_stars
    Error: near line 116: FOREIGN KEY constraint failed
    Error: near line 119: FOREIGN KEY constraint failed
    ...

Le propre des jeux de données négatifs est qu'à chaque violation escomptée
une erreur doit être effectivement produite. Dans l'exemple ci-dessus
on retrouve les numéros de lignes où doivent se trouver les violations
ainsi qu'un message d'erreur propre au SGBD.

La vérification de la
correspondance entre violations escomptées et erreurs produites n'est pas
automatisée. Il convient donc de vérifier "manuellement" l'alignement
entre violations escomptées / erreurs produites.

La qualité d'un schéma
de base de données ne tient pas uniquement en ce que ce schéma autorise
mais aussi en la qualité des erreurs détectées.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.