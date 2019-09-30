..  _`tâche concepts.classes`:

tâche concepts.classes
======================

:résumé: L'objectif de cette tâche est (1) de définir/compléter le modèle
    de classes, (2) de le compiler, (3) de créer un diagramme de classes,
    (4) de vérifier l'alignement du modèle de classes avec les autres
    modèles.
:langage:  :ref:`ClassScript1`
:résultat:
    * ``concepts/classes/classes.cl1``
    * ``concepts/classes/diagrammes/classes.cld.clt``
    * ``concepts/classes/diagrammes/classes.cld.png``

(A) Classes
-----------------------------------

Créer ou compléter le modèle de classes dans
``concepts/classes/classes.cl1`` en fonction :

* des besoins exprimés par le client (dossier ``concepts/besoins/`` )
* des modèles d'objets (dossier ``concepts/objets/`` )
* des scénarios (dossier ``dynamique/scenarios/`` )
* de vos connaissances du domaine.

Certains éléments peuvent ne pas s'appliquer.

(B) Compilation
---------------

Le modèle de classes doit **IMPERATIVEMENT** pouvoir
être "compilé" sans erreur en utilisant la commande suivante
(à partir du répertoire racine)::

       use -c concepts/classes/classes.cl1

S'il y a des erreurs elles seront affichées. Aucun affichage
signifie que le modèle est conforme au langage
:ref:`ClassScript1` (USE OCL).

(C) Diagramme global
--------------------

`Créer ensuite un diagramme de classes`_ avec l'outil USE OCL.
Sauvegarder impérativement le diagramme dans le fichier
``concepts/classes/diagrammes/classes.cld.clt`` (remplacer le fichier
existant). Si une ébauche est fournie le diagramme dessiné devra en
respecter la disposition. Faire une copie d'écran du diagramme
et remplacer le fichier ``concepts/classes/diagrammes/classes.cld.png``
fourni.
Respecter **impérativement** les noms de fichiers, entre autre l'extension
``.png``. Le diagramme global doit impérativement montrer les
cardinalités ; afficher si possible les noms de rôles ou d'associations si
le diagramme reste visible.

(D) Vues
--------

Il peut être demandé de réaliser plusieurs diagrammes pour différentes
vues. Créer dans ce cas des fichiers ``concepts/classes/diagrammes/<NOM>.cld.*``
où ``<NOM>`` fait référence au nom de la vue. Les classes à masquer
peuvent être définies avec le menu contextuel de l'outil `use ocl`_
(click droit).

Si les vues proposées couvrent l'ensemble du diagramme il est intéressant
de montrer moins de détails dans la vision globale (par exemple en
cachant les attributs) et plus de détails dans les vues (par exemple
en montrant les attributs).
Dans chaque vue respecter autant que possible la disposition du
diagramme global.

(E) Objets et scénarios
-----------------------

Dans la suite, il sera demandé de valider le modèle de classes proposé
avec les modèles d'objets et les scénarios. Voir les éventuelles tâches
correspondantes.

(F) Glossaire
-------------

Si un glossaire existe, vérifier que les termes importants apparaissant
dans les noms de classes, d'associations, d'attributs ou de rôles
sont bien dans le glossaire.
Par exemple il peut être important de définir ce qu'est la "DateDeRetour"
dans le contexte d'un bibliothèque. Ce terme fait partie du domaine.
Il est sans doute nécessaire de le définir s'il ne correspond pas à
une définition de sens commun. D'ailleurs le terme à définir est peut
être "Retour".

Lire et appliquer les
:ref:`règles associées à la réécriture d'identificateurs <GlossaryScript_RewritingIdentifiers>`.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.


..  _`use ocl`:
    http://scribetools.readthedocs.io/en/latest/useocl/index.html

..  _`Créer ensuite un diagramme de classes`:
    http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams

.. _`règles associées à la réécriture d'identificateurs`:
    https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rewriting-identifiers