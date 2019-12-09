.. _`tâche concepts.objets.diag`:

tâche concepts.objets.diag
==========================

:résumé: L'objectif de cette tâche est de créer des diagrammes
    d'objets.

:langage:  :ref:`ObjectScript1`
:artéfacts:
    * ``concepts/objets/o<N>/o<N>.ob1``
    * ``concepts/objets/o<N>/diagrammes/o<N>.obd.olt``
    * ``concepts/objets/o<N>/diagrammes/o<N>.obd.png``

(A) Diagrammes
--------------

Pour produire un diagramme d'objets procéder de manière analogue à la
production de diagrammes de classes. Lancer l'outil USE avec la
commande suivante (remplacer ``<N>`` par le numéro du modèle d'objets)::

    use concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

Utiliser le menu ``View > Create View > Object Diagram``.

* ``concepts/objets/o<N>/diagrammes/o<N>.obd.olt``
* ``concepts/objets/o<N>/diagrammes/o<N>.obd.png``

NOTE: La disposition des objets doit autant que possible refléter
la disposition du diagramme de classes.

Observer la présence ou non d'objets isolés. Vérifier s'il s'agit d'un
problème dans le scénario lui même ou un problème dans la traduction qui en
a été faite.
