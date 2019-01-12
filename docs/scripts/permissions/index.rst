.. .. coding=utf-8

.. .. highlight:: PermissionScript

.. index::  ! .pes, ! PermissionScript
    pair: Script ; PermissionScript

.. _PermissionScript:


PermissionScript
================

Examples
--------

::

    permimission model CyberCompagnie
    import usecase model from '../classes/classes.cld'
    import class model from '../usecase/usecase.uss'

    EmbaucherUnEmploye can C Employe, EstEmployeeDans
    EmbaucherUnEmploye can RU Compagnie.budget, Compagnie.quota
    LicencierUnEmploye can delete Employe
    Responsable, Secretaire can R Employee.salary
    Directeur can read, update Employee.salary

..  note::
    * ``can`` peut être remplacé par ``peut``.
    * Les actions peuvent être abbréviées ou pas ("C" ou "create").
    * Les actions peuvent être traduites. Voir la section actions_.

Concepts
--------

Conceptuellement le modèle de permission est basé sur une suite de triplets : ::

    (sujets, actions, ressources)

Ce triplet signifie : " *les <sujets> peuvent effectuer les
<actions> sur les <ressources>.*"

Exemple : ::

    EmbaucherUnEmploye can RU Compagnie.budget, Compagnie.quota

``EmbaucherUnEmploye`` est le sujet_. ``R`` et ``U`` sont les
actions_. ``Compagnie.budget``, ``Compagnie.quota`` sont les ressources_.
Le triplet signifie : *le cas d'utilisation* ``EmbaucherUnEmploye`` *peut lire
(Read) et mettre à jour (Update) les attributs* ``budget`` *et* ``quota`` *de la classe* ``Compagnie``.

..  _sujet:

Sujets
------

Un **sujet** est soit:

*   un **acteur** (provenant du :ref:`modèle de participants<ParticipantScript>`),
    par exemple ``Directeur``,
*   un **cas d'utilisation** (provenant du :ref:`modèle de cas d'utilisation<UsecaseScript>`),
    par exemple ``CreerUnDepartement``.

Si un **acteur** peut réaliser une action sur une ressource_ alors
tous les cas d'utilisation associés à cet acteur peuvent réaliser cette
action.

Exemple : ::

    Directeur can CreerUnDepartement          (modèle de cas d utilisation)
    Directeur can AugmenterUnEmploye          (modèle de cas d utilisation)

    Directeur can U Employe.salaire           (modèle de permission)

Dans cet exemple les deux cas d'utilisation ``CreerUnDepartement``
et ``AugmenterUnEmploye`` peuvent mettre à jour (Update) l'attribut
``salaire`` de la classe ``Employee``.

Actions
-------

Les actions correspondent essentiellement au modèle CRUD (voir wikipedia_).
Les actions peuvent être écrites en entier ou sous forme abbréviées,
en anglais ou en français.

================= =====================
En anglais        En français
================= =====================
C / create        C / creer
R / read          L / lire
U / update        M / modifier
D / delete        D / detruire
X / execute       X / execute
================= =====================

La signification des opérations dépend des ressources. Voir la section
ressources_.

.. _ressource:

Ressources
----------

Pour un modèle de classe une **resource** est soit :

* une **classe**, par exemple ``Employee``,
* un **attribut**, par exemple ``Employee.salaire``,
* une **opération**, par exemple ``Employee.augmenter()``.
* une **association**, par exemple ``EstAffecteA``,
* une **role**, par exemple ``Employe.responsable``.

Le type de ressources définit les actions autorisées :

*   l'opération **create** s'applique à une classe ou à une association.
    Par exemple ``create Employe`` ou ``create EstEmployePar``. Créer un
    attribut, un role ou une opération ne fait pas de sens.
*   l'operation **read** s'applique à un attribut ou à un role. Par
    exemple ``read Employe.salaire`` ou ``read Employe.responsable``.

    *   Lorsque cette action est associé à une classe (par exemple
        ``read Employe`` alors n'importe quel attribut peut être attribut
        de la classe peut être lu (dans l'exemple l'accès est donné
        à tous les attributs de la classe ``Employe``).
    *   Lorsque cette action est associée à une association (par exemple
        ``read EstEmployePar``), alors ,
        celle-ci peut être traversée dans n'importe quel sens.

*   l'opération **update** s'applique à un attribut uniquement.
*   l'opération **delete** s'applique à une classe ou à association
*   l'opératop, **execute** s'applique à une operation uniquement.


============  ======== ========= ========= =========== =====
action/resc.  classe   attribut  operation association role
============  ======== ========= ========= =========== =====
create           X                              X
read            [X]        X                             X
update          [X]        X
delete           X                              X
execute                              X
============  ======== ========= ========= =========== =====

Methode
-------

Les tâches listées par la suite ne peuvent que difficilement être réalisées
en séquentiel. Cependant plusieurs pratiques existent, selon que l'on
part d'un modèle ou d'un autre :

*   **modèle de classes en premier**. Il s'agit de partir d'un modèle de
    classes, de lister les différentes ressources et de répondre à la
    question *"qui change telle ou telle ressource ?"*.

    XXX exemple XXX


*   **modèle de cas participants en premier**. Il s'agit de répondre à
    la question *"que peut faire tel ou tel acteur ?"**

    XXX exemple XXX

*   **modèle de cas d'utilisation en premier**. Il s'agit de répondre à
    la question *"que peut faire tel ou tel cas d'utilisation ?"*

    XXX exemple XXX

*   **matrice de permissions**. Il est également classique de combiner
    les deux méthodes ci-dessus en produisant d'abord une matrice
    listant d'un coté toutes les resources (classes, etc.) et de l'autre
    tous les sujets (acteurs, etc.). Il s'agit ensuite de répondre
    pour chaque élément de la matrice à la question *"quelles actions
    peut être réalisées par ce sujet sur cette ressource"*

    XXX exemple XXX

Quelque soit la méthode retenue, ou certainement combinaison de méthodes,
l'objectif est de construire un modèle de permissions aligné avec
le modèle de classes et avec le modèle cas d'utilisation.

Dependencies
------------

The graph below shows all language dependencies.

..  image:: media/language-graph-pes.png
    :align: center

..  _wikipedia:
    https://en.wikipedia.org/wiki/Create,_read,_update_and_delete