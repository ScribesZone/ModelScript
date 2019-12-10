..  _`tâche concepts.classes`:

tâche concepts.classes
======================

:résumé: L'objectif de cette tâche est (1) de définir/compléter le modèle
    de classes, (2) de le compiler, (3) de vérifier l'alignement
    du modèle de classes avec le glossaire si celui-ci existe.
:langage:  :ref:`ClassScript1`
:artefacts:
    * ``concepts/classes/classes.cl1``
    * ``concepts/classes/status.md``

(A) Classes
-----------------------------------

Créer le modèle de classes dans le fichier ``concepts/classes/classes.cl1``.
Pour écrire le modèle utiliser la documentation du langage
:ref:`ClassScript1` (USE OCL).

Eventuellement un modèle est peut être fourni, soit
sous forme textuelle dans le fichier ``concepts/classes/classes.cl1``,
soit sous forme de diagramme dans le répertoire
``concepts/classes/diagrammes``. Dans les deux cas il s'agit de completer
et/ou de corriger le modèle à partir des éléments fournis.

Le modèle de classes doit in fine être développé en fonction :

* des besoins exprimés par le client (dossier ``concepts/besoins/`` )
* des modèles d'objets (dossier ``concepts/objets/`` )
* des scénarios (dossier ``cu/scenarios/`` )
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


(C) Glossaire
-------------

Si un glossaire existe, vérifier que les termes importants apparaissant
dans les noms de classes, d'associations, d'attributs ou de rôles
sont bien dans le glossaire.
Par exemple il peut être important de définir ce qu'est la "DateDeRetour"
dans le contexte d'un bibliothèque. Ce terme fait partie du domaine.
Il est sans doute nécessaire de le définir s'il ne correspond pas à
une définition de sens commun. D'ailleurs le terme à définir est peut
être "Retour".

.. A AJOUTER QUAND LES FAUTES SERONT CORRIGEES
    -------------------------------------------------------------------
    -------------------------------------------------------------------
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