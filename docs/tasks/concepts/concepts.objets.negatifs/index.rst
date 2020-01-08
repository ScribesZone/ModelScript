(.. _`tâche concepts.objets.negatifs`:

tâche concepts.objets.negatifs
==============================

:résumé: L'objectif de cette tâche est (1) de créer des modèles négatifs
    d'objets et (2) de vérifier que ces modèles génèrent les erreurs 
    escomptées.

:langage:  :ref:`ObjectScript1`
:artefacts:
    * ``objets/no<N>/no<N>.ob1``
    * ``objets/status.md``

Introduction
------------

Tester une application requière la production de tests dits "positifs"
et de tests dits "négatifs".

*   Les tests positifs testent l'application dans les cas de fontionnement 
    normaux. Aucune erreur ne doit être générée. Ce sont les tests
    "normaux".

*   Les tests négatifs testent l'application dans les cas aux limites.
    Il s'agit de vérifier en situation d'erreurs que l'application
    détecte bien les erreurs escomptées.

Les modèles positifs d'objets (ou modèles d'objets positifs) peuvent
être vus comme des tests positifs du modèle de classes. Ils montrent que
le modèle d'objets est conforme au modèle de classes. Souvent
le terme "positif" est omis et on parle de "modèles d'objets"
par simplification, à la place de "modèles positifs d'objets".

Quant à eux les modèles négatifs d'objets (ou modèles d'objets
négatifs) testent le modèle de classes aux limites. Ils ne sont pas
conformes au modèle de classes. Des erreurs (violations) doivent être
détectées.

..  attention::

    Seules certains types de violations sont détectables automatiquement.
    Voir ci-dessous pour plus de détails.

(A) Création
------------

Les modèles négatifs d'objets donnent lieu soit à des violations de
cardinalités, soit à des violations de contraintes. Il s'agit dans
cette tâche d'écrire un ou plusieurs modèles d'objets négatifs.
Chaque violation attendue doit être déclarée dans le modèle.
Se référer à la documentation concernant les :ref:`violations` pour plus
de détails.

En pratique il s'agit de créer des modèles d'objets négatifs ou de
compléter ceux existants (le cas échéant). Ces modèles doivent être
rangés dans des répertoires ``on<N>`` (où ``<N>`` est un numéro). La
structure de ce répertoire doit être analogue à la structure des modèles
d'objets.

Pour définir le contenu de ces modèles, choisir d'abord une liste
de violations intéressantes à détecter. Définir ensuite le contenu du
modèle d'objets pour que ces erreurs soient produites.

Il est possible de créer de multiples modèles d'objets, un modèle par
violation, ou au contraire de rassembler en quelques modèles d'objets
toutes les violations. Indiquer dans le fichier
``concepts/objets/status.md`` les choix retenus pour structurer
les modèles d'objets.

(B) Vérification
----------------

Une fois les violations déclarées dans les modèles d'objets négatifs
il s'agit de vérifier, pour chaque modèle, que les violations ont
bien lieu. Utiliser pour cela l'outil USE. Les violations de cardinalités
sont indiquées dans la section ``Checking structure...``. Les
violations de contraintes sont indiquées dans la section
``Checking invariants...``. Si une violation n'est pas détectée, soit la
contrainte (ou la cardinalité) est erronée (ou non implémentée en OCL),
soit le modèle d'objets est incorrect.

..  attention::

    Les violations de contraintes ne sont détectées que pour les
    contraintes exprimées en OCL. Les contraintes exprimées uniquement
    sous forme textuelle sont ignorées par l'outil USE.


En pratique il s'agit d'observer les messages d'erreurs produits par
l'outil USE et de  comparer ces erreurs aux instructions ``violates``
introduites dans les modèles négatifs d'objets. Consigner le résultat
dans le fichier ``status.md``.


(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.)