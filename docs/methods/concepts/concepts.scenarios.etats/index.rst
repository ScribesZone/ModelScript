.. _`tâche concepts.scenarios.etats`:

tâche concepts.scenarios.etats
==============================

:résumé: L'objectif de cette tâche est de traduire les scénarios textuels
     en scénarios états.

:langage: :ref:`ScenarioScript1`
:résultat:
    * ``scenarios/s<N>/s<N>.sc1``
    * ``scenarios/s<N>/diagrams/S<N>.scd.olt``
    * ``scenarios/s<N>/diagrams/S<N>.scd.png``

Introduction
------------

L'objectif de cette tâche est de traduire dans un premier temps
les textes en scénarios "états", c'est en scénarios vu comme une simple
succession de changement d'états effectuée via des
d'instructions ``!``. Le terme "scénarios états" doit être considéré
en regard aux "sénarios cas d'utilisation". Ces derniers
seront produits par la suite.

Dans cette tâche on ne s'intéresse qu'au changement d'états du système
en adoptant une perspective "données".

Les tâches ci-dessous doivent être répétées pour chaque scénario.


(A) Traduction
--------------

En pratique, comme dans les modèles d'objets, il s'agit dans
cette tâche simplement de traduire le texte des scénarios
en une suite d'instructions ``!`` *à plat*. Voir la tâche
concernant les modèles d'objets pour plus de détails.

NOTE: Si le fichier ``s<N>.sc1``  n'est pas vide ignorer
les éventuelles instructions comme ci-dessous : ::

    --@ context
        ...
    --@ end
    --@ ... va ...
        ...
    --@ end

Ignorer également les emboîtements correspondants, s'ils sont présents.

(B) Inclusion
-------------

L'état initial d'un scénario peut être défini sous forme d'un
modèle d'objet. Dans ce cas il est possible d'inclure ce modèle
d'objets au début du scénario. Utiliser pour cela l'instruction
``open -q`` de use : ::

    open -q ../../../objects/o3/o3.ob1

Cette technique d'inclusion peut êgalement être mis en oeuvre pour
inclure un scénario dans un autre.


(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.