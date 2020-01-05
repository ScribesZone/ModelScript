.. _`tâche concepts.objets`:

tâche concepts.objets
=====================

:résumé: L'objectif de cette tâche est (1) de traduire les modèles d'objets
    textuels en modèle d'objets annotés en :ref:`ObjectScript1` et
    (2) de compiler ces modèles d'objets.
:langage:  :ref:`ObjectScript1`
:artefacts:
    * ``concepts/objets/o<N>/o<N>.ob1``
    * ``concepts/objets/status.md``

Introduction
------------

Cette tâche consiste à traduire les modèles d'objets décrits
sous forme textuelle en modèles d'objets annotés. Chaque modèle d'objets se
concrétise en un fichier ``.ob1``. Ces fichiers vont être
utilisés pour valider le modèle de classes (fichier ``.cl1``).
Il s'agit de répéter les étapes ci-dessous pour chaque modèle d'objets
dans le répertoire ``concepts/objets/``.

(A) Traduction
--------------

Le fichier ``concepts/objets/o<N>/o<N>.ob1`` (où ``o<N>`` est l'identifiant
du modèle d'objet) contient un modèle d'objets décrit en langue naturelle.
Il s'agit de traduire chaque ligne en utilisant le langage
:ref:`ObjectScript1`.

NOTE: les modèles d'objet annotés peuvent être
"compilés". Voir la section suivante pour plus de détails.

Lorsqu'une valeur n'est pas définie utiliser une instruction
``... := Undefined``. Dans certains cas il peut être pertinent "d'inventer"
une valeur ou des valeurs. Dans ce cas mettre une note dans le modèle de suivi.

Faire au mieux sachant que l'objectif est de traduire un texte fourni
par (ou écrit en collaboration avec) le "client". Il sera peut être
nécessaire de voir avec lui comment compléter/valider la description
d'un modèle d'objets sachant qu'un tel modèle pourra par la suite être
utilisé pour établir des tests et en particulier des tests de recette.

(B) Classes
-----------

Lorsqu'un modèle d'objet est créé il est **IMPERATIF** de Vérifier qu'il
est aligné avec le modèle de classes.
Pour cela utiliser la commande suivante : ::

    use -qv concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

ou <N> correspond au numéro du modèle d'objet. L'interpreteur affichera
les éventuelles erreurs de syntaxe ainsi que les erreurs de types ou de
cardinalités. Si rien ne s'affiche cela signifie qu'aucune erreur n'a été
trouvée.

La localisation des erreurs n'est parfois pas indiquée clairement. Si
ce problème apparaît utiliser l'interpreteur USE en utilisant la commande
suivante : ::

    use -nogui concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

Si l'objectif est de vérifier les cardinalités utiliser ensuite la commande
use ``check`` ou ``check -v``. Terminer finalement avec la command ``quit``
ou ``Ctrl C`` pour sortir de l'interpréteur.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.