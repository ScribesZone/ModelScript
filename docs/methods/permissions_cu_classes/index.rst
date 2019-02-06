tache:permissions_cu_classes
============================


:résumé: L'objectif de cette tâche est de définir le modèle
    de permission en mettant en relation les acteurs/cas d'utilisation
    avec les éléments du modèles de classes utilisés.

:langage: :ref:`PermissionScript`

:résultat:
    * ``permissions/permissions.pes``


(A) Introduction
----------------

Après avoir défini un modèle de classes et un modèle de cas d'utilisation
il est possible de définir le modèle de permissions. Cette tâche a
*in fine* pour objectif d'aligner :

* le modèle de permissions,
* le modèle de classes,
* le modèle de particpants,
* le modèle de cas d'utilisation,
* les modèles de scénarios.

Il existe :ref:`plusieurs manières <PermissionScript_Methode>` de remplir
le modèle de permission. L'objectif de cette tâche est de mettre en
pratique deux de ces techniques.


(B) Technique 1: classes en premier
-----------------------------------

Commencer par la méthode
:ref:`"classes en premier" <PermissionScript_ClassesEnPremier>`.
Lorsque des classes/attributs/associations ne sont créé/utilisés/modifiés
par aucun cas d'utilisation, indiquer pourquoi sous forme de commentaires
dans le modèle de permissions.  Ajuster le modèle de cas d'utilisation
si nécessaire.

(C) Technique 2: cas d'utilisation en premier
---------------------------------------------

Dans un deuxième temps utiliser la méthode
:ref:`"Cas d'utilisation en premier" <PermissionScript_CasDUtilisationEnPremier>`
pour remplir
la suite du modèle. Ajuster le modèle de classes  si nécessaire.

(D) Alignement avec les modèles de scénarios
--------------------------------------------

Une fois le modèle de permission créé, vérifier que les accès réalisés
dans les scénarios ne violent pas les permissions données.


(Z) Suivi et status
-------------------

**Suivi**: Si des questions ou des hypothèses surgissent lors de ce travail
appliquer les :ref:`règles relatives au suivi <Tracks_Rules>`.

**Status**: Avant de terminer cette tâche écrire le status en appliquant
les :ref:`règles relatives au status <Status>`.