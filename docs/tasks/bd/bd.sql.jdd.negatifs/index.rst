..  _`tâche bd.sql.jdd.negatifs`:

tâche bd.sql.jdd.negatifs
=========================

:résumé: L'objectif de cette tâche est de définir des jeux
     de données (jdd) négatifs pour la base de données SQL.

:langage: SQL
:artefacts:
    * ``sql/datasets/*.sql``

(A) JDD négatifs
----------------

Cette tâche fait suite à la :ref:`tâche bd.sql.jdd`.

Contrairement aux jeux de données positifs qui ne doivent produire
aucune erreur, les jeux de données négatifs doivent générer des erreurs
partout où les contraintes associées au schéma ne sont pas respectées.
Un jeu de données négatif pourrait produire un résultat comme suit : ::

    Clearing database ... done.
    Creating database schema ... done.
    Loading dataset nds1 ...Error: near line 13: UNIQUE constraint failed: Movies.title
    Error: near line 39: UNIQUE constraint failed: Cinemas.name
    Error: near line 53: UNIQUE constraint failed: Spectators.name
    Error: near line 68: UNIQUE constraint failed: IsOn.movie, IsOn.cinema
    Error: near line 70: FOREIGN KEY constraint failed

Chacune des erreurs doit être répertoriée sous forme de commentaires
dans le fichier ``.sql``. Pour chaque erreur, indiquer la contrainte
violée. Utiliser pour cela le mot clé ``violates``. Un jeu de données
négatif pourrait ressembler à cela : ::

    INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts CBD');
    --@ violates Spectators.PK
    INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts CBD');
    --@ violates Spectators.FK_movie
    INSERT INTO IsOn VALUES ('==> VIOLATION <==','Hoyts CBD');
    --@ violates Spectators.FK_cinema
    INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','==> VIOLATION <==');
    INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema Myer');
    INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema');

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.