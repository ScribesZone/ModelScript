.. .. coding=utf-8

.. highlight:: ObjectScript1

.. index::  ! .obs, ! ObjectScript1
    pair: Script ; ObjectScript1

.. _ObjectScript1:

ObjectScript1
=============

Exemples
--------

Le code ci-dessous montre un modèle d'objets basique :

..  code-block:: ObjectScript1

    ! create bob : Personne
    ! bob.nom := 'bob'
    ! bob.age := 37
    ! insert(bob, c232) into EstResponsableDe
    ! create nourry : Enseignant
    ! nourry.nom := 'Nourry Blanc'
    ! nourry.matiere := 'musique'
    ! nourry.login := Undefined
    ! nourry.motDePasse := Undefined
    ! create s876 : Classe
    ! s876.code := 'S876'
    ! insert (nourry, s876) into IntervientDans

Le code ci-dessous montre un modèle d'objets annoté :

..  code-block:: ObjectScript1

    --| (1) Bob a 37 ans et est responsable de la classe c232
        ! create bob : Personne
        ! bob.nom := 'bob'
        ! bob.age := 37
        ! insert(bob, c232) into EstResponsableDe
    --| (2) Nourry Blanc est professeur de musique.
        ! create nourry : Enseignant
        ! nourry.nom := 'Nourry Blanc'
        ! nourry.matiere := 'musique'
        ! nourry.login := Undefined
        ! nourry.motDePasse := Undefined
    --| (3) Nourry Blanc intervient en terminale S876.
    --| (4) Il a vraiment de la chance.
    --| (5) La terminale S876 est plaisante.
        ! create s876 : Classe
        ! s876.code := 'S876'
        ! insert (nourry, s876) into IntervientDans
    --| (6) Alicia Ganto est professeur de math.

Le code suivant montre un modèle d'objets négatif :

..  code-block:: ObjectScript1

    --@ violates EstResponsableDe.responsable.max
    --@ violates ResponsableAdulte

    --| (1) Bob a 30 ans et est responsable de la classe c232
        ! create bob : Personne
        ! bob.age := 30
        ! insert(bob, c232) into EstResponsableDe
    --| (2) Octavia a 17 ans et est responsable la classe c232.
        ! create octavia : Personne
        ! octavia.age := 17
        ! insert(bob, c232) into EstResponsableDe

ObjectScript1
-------------

**ObjectScript1** est une notation textuelle pour écrire des
`diagrammes d'objets`_ UML.
ObjectScript1 est une version réduite du langage SOIL (`USE OCL`_).
L'extension ``.ob1`` est utilisée à la place de l'extension ``.soil``.

Concepts
--------

Les modèles d'objets sont basés sur les concepts suivants :

*   les valeurs d'énumérations,
*   les objets,
*   les valeurs d'attributs,
*   les liens,
*   les objets-liens,
*   les textes annotés,
*   les violations.

Valeur d'énumérations
---------------------

ObjectScript1 (basé sur USE OCL):

..  code-block:: ObjectScript1

    Season::winter

Objets
------

ObjectScript1 (basé sur USE OCL):

..  code-block:: ObjectScript1

    ! create bob : Person
    ! bob.nom := 'bob'
    ! bob.dateDeNaissance := '21/10/1994'

Liens
-----

ObjectScript1 (basé sur USE OCL):

..  code-block:: ObjectScript1


    ! insert(tian,c232) into Owns


Diagramme d'objets UML :

..  image:: media/USEOCLAssociationSOIL.png
    :align: center

Objet-liens
-----------

ObjectScript1 (basé sur USE OCL):

..  code-block:: ObjectScript1

    ! c := new Hate between (chita,kaa)
    ! c.reason := "kaa is really mean"
    ! c.intensity = 1000

Textes annotés
--------------

ObjectScript1


..  code-block:: ObjectScript1

    --| Bob was born  ow
        ! create bob : Personne
        ! bob.nom := 'bob'
        ! insert(tian,c232) into Owns
    --| (1) Nourry Blanc est professeur de musique.
        ! create nourry : Enseignant
        ! nourry.nom := 'Nourry Blanc'
        ! nourry.matiere := 'musique'
        ! nourry.login := Undefined
        ! nourry.motDePasse := Undefined
    --| (2) Nourry Blanc intervient en terminale S876.
    --| (3) Il a vraiment de la chance.
    --| (4) La terminale S876 est plaisante.
        ! create s876 : Classe
        ! s876.code := 'S876'
        ! insert (nourry, s876) into IntervientDans
    --| (3) Alicia Ganto est professeur de math.

..  _violations:

Violations
----------

Les violations sont des erreurs produites par un
modèle d'objets appelé "modèle d'objets négatifs". Les violations sont
déclarées à l'aide du mot clé ``violates``. Il y a deux genres de
violations ;

*   **Violations de cardinalités**. Une telle violation se produit
    soit lorsque la cardinalitée effective associée à un role est
    supérieure à la cardinalité maximale déclarée,
    soit lorsque la cardinalité effective est inférieure à la
    cardinalité minimale. Voici deux exemples possibles de violations : ::

        --@ violates EstResponsableDe.responsable.min
        --@ violates Dirige.directeur.max

    Dans cet exemple ``EstResponsableDe`` et ``Dirige`` sont des
    associations. ``responsable``, ``directeur`` sont des rôles.
    ``min`` et ``max`` font référence à la cardinalité minimale et
    maximale associées aux rôles.

*   **Violations de contraintes**. Ces violations se produisent
    lorsqu'un ou plusieurs objets violent une contrainte. Voici un
    exemple de contrainte de violations : ::

        --@ violates DirecteurAdulte

    Dans cet exemple ``DirecteurAdulte`` est une contrainte définie
    dans le modèle de classes.

    NOTE: les violations de contraintes ne sont détectées par l'outil
    USE OCL uniquement si la contrainte est définie en OCL.


Outils
------

.. _AnalyseDesModelesDObjets:

Analyse des modèles d'objets
''''''''''''''''''''''''''''

La conformité des modèles d'objets vis à vis du modèle de classes
peut être vérifiée avec l'outil `USE OCL`_. Lorsque la
:ref:`méthode ModelScript<ModelScriptMethod>` est utilisée entrer la
commande suivante dans un terminal (on suppose que le répertoire courant
est le répertoire racine du projet de modélisation) :

..  code-block:: none

    use -qv concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

L'analyseur vérifie qu'il n'y a pas d'erreurs de syntaxe, pas d'erreurs
de type, pas d'erreurs de cardinalités et pas d'erreurs de contraintes.
Si aucune erreur n'est affichée alors les deux modèles sont corrects et
sont alignés.

..  note::

    Si des violations sont définies (instructions ``@violates``) le
    modèle d'objets doit produire les erreurs escomptées. Cette
    vérification n'est pas automatisée. Il faut donc vérifier
    "manuellement" que toutes les erreurs mentionnées sont effectivement
    produites.

La localisation des erreurs n'est parfois pas indiquée clairement. Si
ce problème apparaît utiliser l'interpreteur USE en utilisant la commande
suivante : ::

    use -nogui concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

Si l'objectif est de vérifier les cardinalités utiliser ensuite la commande
use ``check`` ou ``check -v``. Terminer finalement avec la command ``quit``
ou ``Ctrl C`` pour sortir de l'interpréteur.


.. _GenerationDeDiagrammesDObjets:

Génération de diagrammes
''''''''''''''''''''''''

Créer des diagrammes d'objets est possible en utilisant l'outil `USE OCL`_.

..  code-block:: none

    use -nr concepts/classes/classes.cl1 concepts/objets/o<N>/o<N>.ob1

Se référer à la page "`creating UML object diagrams`_" pour plus
d'information.

La disposition (layout) du diagramme doit être sauvé dans le fichier
``concepts/objets/O<N>/diagrammes/o<N>.obd.clt``. Une copie d'écran
doit être effectuée et sauvé dans
``concepts/objets/O<N>/diagrammes/O<N>.obd.png``.


Dépendances
-----------

Le graphe ci-dessous montre les dépendances entre langages.

..  image:: media/language-graph-obs.png
    :align: center

..  _`USE OCL`: http://sourceforge.net/projects/useocl/

..  _`diagrammes d'objets`: https://www.uml-diagrams.org/class-diagrams-overview.html#object-diagram

.. _`creating UML object diagrams`: https://scribestools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams
