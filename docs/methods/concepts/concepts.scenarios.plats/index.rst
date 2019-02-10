tâche concepts.scenarios.plats
==============================

:résumé: L'objectif de cette tâche est de traduire les scénarios textuels
     en scénarios (orienté données) plats.

:langage: :ref:`ScenarioScript1`
:résultat:
    * ``scenarios/s<N>/s<N>.sc1``
    * ``scenarios/s<N>/diagrams/S<N>.scd.olt``
    * ``scenarios/s<N>/diagrams/S<N>.scd.png``

(A) Introduction
----------------

L'objectif de cette tâche est de traduire dans un premier temps
les textes en scénarios "plats", c'est à dire une simple suite
d'instructions ``!``. On ne s'intéresse qu'au changement d'états
du système en adoptant une perspective "données".

Les fichiers de scénarios obtenus dans cette tâche seront modifiés
par la suite pour leur ajouter une structure.

Les tâches ci-dessous doivent être répétées pour chaque scénario.


(B) Traduction
--------------

En pratique, comme dans les modèles d'objets, il s'agit dans
cette tâche simplement de traduire le texte des scénarios
en une suite d'instructions ``!`` *à plat*. Voir la tâche
concernant les modèles d'objets pour plus de détail.

NOTE: Si le fichier ``s<N>.sc1``  n'est pas vide ignorer
les éventuelles instructions comme ci-dessous : ::

    --@ context
        ...
    --@ end
    --@ ... va ...
        ...
    --@ end

Ignorer également les emboîtements correspondants, s'ils sont présents.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.