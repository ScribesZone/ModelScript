tâche concepts.classes
======================

:résumé: L'objectif de cette tâche est (1) de compléter le modèle
    de classes, (2) de le compiler, (3) de créer un diagramme de classes,
    (4) de vérifier l'alignement du modèle de classes avec les autres
    modèles.
:langage:  :ref:`ObjectScript1`
:résultat:
    * ``classes/classes.cl1``
    * ``classes/diagrams/classes.cld.clt``
    * ``classes/diagrams/classes.cld.png``

(A) Définition du modèle de classes
-----------------------------------

Compléter le modèle de classes en fonction :

* des besoins exprimés par le client (dossier ``requirements/`` )
* des modèles d'objets (dossier ``objects/`` )
* des scénarios (dossier ``scenarios/`` )
* de vos connaissances du domaine.

Certains de ces répertoires peuvent être absents.

(B) Compilation
---------------

Le modèle de classes doit **IMPERATIVEMENT** pouvoir
être "compilé" sans erreur en utilisant la commande suivante
(à partir du répertoire racine du dépot)::

       use -c classes/classes.cl1

S'il y a des erreurs elles seront affichées. Aucun affichage
signifie que le modèle est conforme à UML.

(C) Diagramme de classes global
-------------------------------

`Créer ensuite un diagramme de classes`_ avec l'outil USE OCL.
Sauvegarder impérativement le diagramme dans le fichier
``classes/diagrams/classes.cld.clt`` (remplacer le fichier
existant). Si une ébauche est founrie le diagramme dessiné devra en
respecter la disposition . Faire une copie d'écran du diagramme
et remplacer le fichier ``classes/diagrams/classes.cld.png`` fourni.
Respecter **impérativement** les noms de fichiers, entre autre l'extension
``.png``.

(D) Alignement avec les objets et les scénarios
-----------------------------------------------

Dans la suite, il sera demandé de valider le modèle de classes proposé
avec les modèles d'objets et des scénarios. Voir les tâches
correspondantes. Répéter ces operations jusqu'à ce que le modèle soit
satisfaisant.

(E) Alignement avec le glossaire
--------------------------------

Vérifier que les termes importants apparaissant dans les noms de classes,
d'associations, d'attributs ou de rôles sont bien dans le glossaire.
Par exemple il peut être important de définir ce qu'est la "DateDeRetour"
dans le contexte d'un bibliothèque. Ce terme fait partie du domaine.
Il est sans doute nécessaire de l'expliquer s'il ne correspond pas à
une définition de sens commun. D'ailleurs le terme à définir est peut
être "Retour".

Lire et appliquer les :ref:`règles associées à la réécriture d'identificateurs <GlossaryScript_RewritingIdentifiers>`.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.


..  _`Créer ensuite un diagramme de classes`:
    http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams

.. _`règles associées à la réécriture d'identificateurs`:
    https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rewriting-identifiers