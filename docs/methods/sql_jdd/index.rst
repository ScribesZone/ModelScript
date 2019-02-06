tache:sql_jdd
=============

:résumé: L'objectif de cette tâche est de définir des jeux
     de données (jdd) (positif) pour la base de données SQL.

:langage: SQL
:résultat:
    * ``sql/datasets/*.sql``

(A) Exemple
-----------

Des jeux de données (positifs) doivent être implémentés en SQL.
A titre d'illustration le repertoire ``sql/datasets/`` contient des exemples.
Cet exemple permet d'illustrer l'approche et de tester des
requêtes sur des données existantes. Le contenu de ces fichiers devra être
évidemment remplacé par des jeux de données appropriés.

(B) Implémentation des jeux de données
--------------------------------------

Les jeux de données doivent être implémentés via des instructions SQL
``INSERT``. Ces instructions doivent être écrites dans les fichiers
``sql/datasets/<N>.sql`` ou ``<N>`` est le nom du jeu de données.

Si des modèles d'objets ou des jeux de données relationnels ont été
définis auparavant ces derniers doivent être réutilisés autant que possible.

(C) Chargement des jeux de données
----------------------------------

Le script de création de base de données peut être utilisé pour charger
un jeu de données. Par exemple pour un jeu de données ``ds1`` la création
de la base de données se fait avec la commande suivante
(dans l'exemple ci-dessous on suppose que le fichier ``datasets/ds1.sql``
existe) : ::

    create-database.sh ds1

Dans le cadre de cette tâche on s'intéresse aux jeux de données positifs.
Ces derniers doivent être conformes au schéma de données. Aucune erreur ne
devra donc être détectée lors du chargement.

L'exécution du script ``create-database.sh`` avec le jeu de données
positif ``ds1`` devrait ressembler à cela : ::

    Clearing database ... done.
    Creating database schema ... done.
    Loading dataset ds1 ... done.
    Dataset ds1 loaded in database.

(Z) Suivi et status
-------------------

**Suivi**: Si des questions ou des hypothèses surgissent lors de ce travail
appliquer les :ref:`règles relatives au suivi <Tracks_Rules>`.

**Status**: Avant de terminer cette tâche écrire le status en appliquant
les :ref:`règles relatives au status <Status>`.