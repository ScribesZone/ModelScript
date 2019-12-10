tâche cu.permissions
====================

:résumé: L'objectif de cette tâche est de définir le modèle
    de permission en mettant en relation les acteurs/cas d'utilisation
    avec les éléments du modèles de classes utilisés.

:langage: :ref:`PermissionScript`

:artefacts:
    * ``permissions/permissions.pes``


Introduction
------------

Après avoir défini un modèle de classes (:ref:`tâche concepts.classes`)
et un modèle de cas d'utilisation (:ref:`tâche cu.preliminaire`),
il est possible de définir le modèle de permissions. Cette tâche a
*in fine* pour objectif d'aligner :

* le modèle de permissions,
* le modèle de classes,
* le modèle de participants,
* le modèle de cas d'utilisation,
* les modèles de scénarios.

Il existe :ref:`plusieurs manières <PermissionScript_Methode>` de remplir
le modèle de permission. L'objectif de cette tâche est de mettre en
pratique deux de ces techniques.


(A) Technique 1
---------------

Commencer par la méthode
:ref:`"classes en premier" <PermissionScript_ClassesEnPremier>`.
Lorsque des classes/attributs/associations ne sont créés/utilisés/modifiés
par aucun cas d'utilisation, indiquer pourquoi sous forme de commentaires
dans le modèle de permissions.  Ajuster le modèle de cas d'utilisation
si nécessaire.

(B) Technique 2
---------------

Dans un deuxième temps utiliser la méthode
:ref:`"Cas d'utilisation en premier" <PermissionScript_CasDUtilisationEnPremier>`
pour remplir
la suite du modèle. Ajuster le modèle de classes si nécessaire.

(C) Scénarios
-------------

Une fois le modèle de permission créé, vérifier que les accès réalisés
dans les scénarios ne violent pas les permissions données.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.