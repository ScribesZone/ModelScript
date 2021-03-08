..  _`tâche bd.sql.requetes`:


tâche bd.sql.requetes
=====================

:résumé: L'objectif de cette tâche est de spécifier, d'écrire
    et de tester des requêtes SQL.

:langage: SQL
:artefacts:
    * ``bd/sql/requetes/``

Introduction
------------

Cette tâche permet de spécifier un ensemble de requêtes à réaliser
en SQL, de définir le résultat attendu et de tester que la requête
fourni bien le bon résultats.

La structure de repertoire ```requetes/``` est le suivant :

*   Les fichiers ```QNNN_Identifiant.sql``` contiennent les requêtes
    écrites en SQL.

*   Le repertoire ```attendu``` contient pour chaque requête le résultat
    attendu sous forme de fichier csv.

Pour évaluer une requête ```QNNN``` utiliser le script suivant :

    eval.sh QNNN

Pour évaluer toutes les requêtes utiliser la commande suivante :

    eval.sh all

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.