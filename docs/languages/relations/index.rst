.. .. coding=utf-8

.. highlight:: RelationScript

.. index::  ! .res, ! RelationScript
    pair: Script ; RelationScript

.. _RelationScript:

RelationScript
==============

Exemples
--------

::

    relation model CyberStore
    import glossary model from '../glossaries/glossaries.gls'
    import qa model from '../qa/relations.qas'

    relation Employee(firstname_, salary, address, department)
        | All the employee in the store.
        intention
            (n, s, a, d) in Employee <=>
            | the `Employee` identified by her/his firstname <n>
            | earns <s> € per cycle. She/he lives
            | at the address <a> and works in the `Department` <d>.
        examples
            ('John', 120, 'Randwick', 'Toys')
        constraints
            dom(firstname) = String
            dom(salary) = Integer
            dom(address, department) = String
            key firstname
            firstname -> salary
            firstname -> address, department

    relation Leaders(department_:String, boss:s)
        | The department leaders.
        intention
            (p, d) in Leaders <=>
            | The `Leader` of the `Department` <d> is the person <p>.
        constraints
            key department

    relation Leaders2   # columns defined "vertically"
        | The department leaders.
        columns
            departement:String
            boss:String

    constraints
        Leaders[department] = Employee[department]
        Leaders[boss] C= Employee[firstname]

    constraint SalaryDifference
        | The difference of salary in a department must not exceed 100%.

    dataset DS1
        | Employees and leaders of Alpha Super store.
        Employee
            ('John', 120, 'Randwick', 'Toys')
            ('Mary', 130, 'Wollongong', 'Furniture')
            ('Peter', 110, 'Randwick', 'Garden')
            ('Tom', 120, 'Botany Bay', 'Toys')
        Leaders
            ('John', 'Toys')
            ('Mary', 'Furniture')
            ('Peter', 'Garden')

    negative dataset NDS1
        | Octavia and bookstore do not exist.
        | Violation of referential integrity constraints.
        Employee
            ('John', 120, 'Randwick', 'Toys')
            ('Mary', 130, 'Wollongong', 'Furniture')
        Leaders
            ('Octavia', 'Bookstore')

    query JohnBoss(boss)
        | The department leaders.
        (Employee:(firstname='John')[department] * Leaders)[boss]

    view Salaries(name_:s, salary:i)
        | The salary of each employee.
        Employee[firstname, salary]

    relation LesAppartements
        transformation
            from R_Class(Appartement)
            from R_Compo(EstDans)
            from R_OneToMany(Partage)
        columns
            nom_ : String
            numero_ : Integer
            superficie : Real
            nbDePieces : Integer
            jnum : Integer
        constraints
            key nom_, numero_
            LesAppartements[jnum] C= LesJardins[jnum_]
            LesAppartements[nom_] C= LesBatiments[nom_]


RelationScript
--------------

Le langage RelationScript permet d'exprimer des "schemas_" au sens du
`modèle relationnel`_.

.. note::

    Attention, le terme "modèle de relations" ne doit pas être confondu
    avec le terme `modèle relationnel`_. Un modèle de relations
    permet de définir des relations, tout comme un modèle de cas
    d'utilisation définit des cas d'utilisation, un modèle de classes
    définit des classes, etc. Le `modèle relationnel`_ correspond
    au contraire à un concept plus général. Il s'agit d'une manière de
    structurer et d'interroger des données.

Concepts
--------

Le langage RelationScript est basé sur les concepts suivants :

* les schémas, appelés modèles de relations, (relation models),
* les relations (relations),
* les colonnes (columns),
* les clés et les clés étrangères (keys et foreign keys),
* les contraintes (constraints),
* les dépendences fonctionnelles (functional dependencies),
* les formes normales (normal forms),
* les jeux de données (data sets),
* les requêtes (queries)
* les vues (views)
* les transformations.

.. _`RelationScript_Relations`:

Relations
---------

Les relations peuvent être déclarées sur une seule ligne, en utilisant
la notation simple que l'on trouve typiquement dans les livres ; par
exemple : ::

    R(x, y, z).

Il est également possible, et de manière tout à fait équivalente,
de définir les colonnes de manière verticale (et optionellement
d'ajouter le mot clé ``relation``) : ::

    relation R
        columns
            x
            y
            z

.. _`RelationScript_Cles`:

Clés
----

Dans les livres et par convention les attributs clés sont soulignés.
En l'absence de soulignement des caractères ascii,
en RelationScript le nom des attributs clés est
suffixé par un caractère souligné "``_``". ::

    R(x_, y_, z).

Dans l'exemple ci-dessus la clé est (x,y). Dans le cas où il y aurait
plusieurs clés, les attributs peuvent être suffixés. Par exemple la
relation suivante possède 3 clés : ::

    R(x_id1, y_id2_id3, z_id3, t, u).


Telle qu'elle est définie la relation possède 3 clés : < (x), (y), (y,z) >.
Dans tous les cas les clés peuvent être spécifées de manière plus
explicites dans la section ``constraints``. ::

    relation R(x, y, z)
        constraints
            key x
            key y
            key y,z

Intention
---------

L'intention d'une relation correspond à sa signification, à la manière
d'interpréter le contenu d'une relation. L'intention peut soit être
implicite, soit de être définie de manière explicite et
structurée. Dans l'exemple ci-dessous l'intention est implicite, la
relation est définie sous forme de documentation non structurée. ::

    relation R4(a_,c,d)
        | The list of X. This relation means that ...

Il est préférable de définir l'intention de manière structurée comme
ci-dessous. Notons que ``dans`` est un mot-clé (``in`` en anglais)
et que la ligne correspondante à une structure. Le nombre de paramètres
du tuple doit correspondre au nombre d'attributs de la relation.
Dans le texte de l'intentation les variables doivent apparaître entre
crochets (p.e. ``<a>``) ::

    relation R4(a_,c,d)
        | The list of X.
        intention
            (a,c,d) dans R4 <=>
            | the person <a> is ... with <c> ... and <d> ...

.. _`RelationScript_ContrainteDeDomaine`:

Contraintes de domaine
----------------------

Le domaine des attributs peut être défini de différentes manière comme
le montre les exemples suivants : ::

    relation R1(a,b,c,d)
        constraints
            dom(a) = String
            dom(b) = dom(c) = Date
            dom(d) = Real ?

    relation R2(a:String, b:Date, c:Date, d:Real ?)

    relation R3
        columns
            a : String
            b : Date
            c : Date
            d : Real ?

Un type basique suivi de de l'opérateur ``?`` signifie que le domaine est
étendu avec la valeur ``null``. En d'autres termes cela signifie que
l'attribut correspondant est optionnel.

..  note::
    Le modèle relationnel n'autorise pas les attributs optionnels. Ces
    cette possibilité est offerte pour faciliter la traduction vers SQL.

Différents types de données sont définis par le langage RelationalScript.
Chaque type de données possède sa propre notation abbréviée, ce qui
s'avère pratique lors de la définition de relations sur une seule ligne.

=============== ==============
Datatype        Shortcut
=============== ==============
String          s
Real            r
Boolean         b
Integer         i
Date            d
DateTime        dt
Time            t
=============== ==============

En utilisant la notation abbréviée une relation peut être définie comme
suit : ::

    relation LesEmployés(nom:s, prenom:s, age:i, dateNaissance: d)

.. _`RelationScript_ContrainteDIntegrite`:

Contraintes d'intégrité
-----------------------

Les contraintes d'intégrité (et en particulier les
`contraintes d'intégrité référentielle`_) peuvent être définies
sous forme de documentation en langue naturelle. ::

    constraint Parent
        | Les parents d'une personne doivent être
        | plus agés que cette personne, d'au moins 7 ans.

Si le modèle de relations est dérivé d'un modèle de classes, il n'est
pas nécessaire de répeter le corps des contraintes qui sont simplement
"héritées" ; seul le nom suffit. ::

    constraint AuMoins7Ans

Le corps de certaines contraintes peut également être défini en utilisant
l'`algèbre relationnelle`_. ::

    constraint FK_34h
        | The h of the relation R3 is one of the h of R4.
        R3[h] C= R4[h]

    constraints
        R1[d] C= R2[d]
        R1[d1,d1] C= R2[d1,d2]
        R[X] u R[z] = {}
        R[X] n R[z] = Persons[X]

Voir la section concernant l'`algèbre relationnelle`_
pour plus de détails sur la notation utilisée.

Dépendences fonctionnelles
--------------------------

Les `dépendances fonctionnelles`_ et les concepts associés peuvent être
définis comme suit : ::

    relation R(a,b,c,d)
        constraints
            key a,b
            a,b -> c,d
            prime a
            prime b
            /prime c
            a -/> c
            c -ffd> d
            a -/ffd> b
            {a}+ = {a,b,c}

Formes normales
---------------

::

    relation R(a,b,c,d)
        constraints
            3NF

.. _`RelationScript_Transformation`:


Transformations
---------------

Un modèle de relations peut être obtenu par transformation à partir
d'un modèle de classes. Une telle transformation peut correspondre à
l'application d'une suite de règles définies dans une catalogue.
Un exemple de catalogue est montré ci-dessous à titre d'illustration
(:download:`télécharger <media/Catalog-UMLToRelational-MCornax.pdf>`).

..  image:: media/regles-m-cornax.png
    :align: center

Considérons de plus le modèle de classes ci-dessous.

..  image:: media/jardins-uml.png
    :align: center

En utilisant la règle ``R_Class`` la classe ``Batiment``
est transformée en la relation ``LesBatiments`` définie comme
suit :

..  note::

    La version française de la règle fait le renommage suivant : ``X``
    devient ``LesXs``.

::

    relation LesBatiments
        transformation
            from R_Class(Batiment)
        columns
            nom_ : String
            capacite : Integer
        constraints
            key nom_

Remarquer la section ``transformation`` et le mot clé ``from``.
Vient ensuite le nom de la règle utilisée ``R_Class`` qui ici
est appliquée à la classe ``Batiment``. Le reste de la définition
de la relation est standard.

La transformation de la classe ``Appartement`` est montrée ci-dessous
à titre d'illustration. ::

    relation LesAppartements
        transformation
            from R_Class(Appartement)
            from R_Compo(EstDans)
            from R_OneToMany(Partage)
        columns
            nom_ : String
            numero_ : Integer
            superficie : Real
            nbDePieces : Integer
            jnum : Integer
        constraints
            key nom_, numero_
            LesAppartements[jnum] C= LesJardins[jnum_]
            LesAppartements[nom_] C= LesBatiments[nom_]

Dans la section ``transformation`` ont voit que trois règles ont été
appliquées :

*   la règle de transformation de classe ``R_Class``,
*   la règle de transformation de composition ``R_Compo``. Cette
    règle a été appliquée à la composition ``EstDans``,
*   la règle ``R_OneToMany`` appliquée à l'association ``Partage``.

Dans certains cas il est nécessaire de changer le nom de
certains attributs, de fusionner deux attributs en une même colonne, etc.
Certaines règles peuvent être manquantes ou doivent être appliquée
de manière différente. Toutes ces modifications peut être documentées
sous forme de documentation dans la section transformation. ::

    relation LesX
        transformation
            from R1(X)
            | Le type de l'attribut z a été changé vers String car ...
            | L'attribut u a été préfixé par le nom du rôle car ...
            | ...

Requêtes
--------

Les requêtes sont simplement des relations dont le corps est
exprimé à l'aide de l'`algèbre relationnelle`_.

::

    query Q1(boss)
        | The department leaders
        (Employe:(firstname='John')[department] * Leaders)[boss]

Vues
----

Au niveau du modèle relationnel les requêtes et les vues sont
en tout point équivalentes. Le concept de vue est défini ici
pour simplifier la transformation vers le langage SQL.

::

    view V1(boss)
        | The department leaders
        (Employe:(firstname='John')[department] * Leaders)[boss]


..  _`algèbre relationnelle`:

Algèbre relationnelle
---------------------

Le langage RelationScript définit tous les opérateurs classiques
de l'algèbre relationnelle
(`wikipedia <https://en.wikipedia.org/wiki/Relational_algebra>`_).
A chaque opérateur est associé une notation en ascii.

==================  ====================================================
Operateur           Exemple
==================  ====================================================
Projection          Employee[salary]
Selection           Employee :( address='Randwick' )
Renaming            L(employee, address) := Employee[firstname, address]
Cartesian product   Employee x Leaders
θ join              Employee * ( Employee.dept=Leaders.dept ) Leaders
Natural join        Employee * Leaders
Union               Employee[firstname] u Leaders[firstname]
Intersection        Employee[firstname] n Leaders[firstname]
Difference          Employee[firstname] - Leaders[firstname]
Empty set           {}
Set inclusion       Employee C= Person
Set inclusion       Employee C Person
Set equality        Employee = Person
Intersection        Employee n Person
Union               Employee u Person
Tuple               (10, 3, 'Hello)
==================  ====================================================


Dépendances
-----------

Le graphe ci-dessous montre les dépendances entre langages avec un focus
sur le langage RelationScript.

..  image:: media/language-graph-res.png
    :align: center


..  _schemas:
    https://en.wikipedia.org/wiki/Database_schema

..  _`modèle relationnel`:
    https://en.wikipedia.org/wiki/Relational_model

..  _`relational algebra wikipedia`:
    https://en.wikipedia.org/wiki/Relational_algebra

..  _`contraintes d'intégrité référentielle`:
    https://en.wikipedia.org/wiki/Referential_integrity

..  _`dépendances fonctionnelles`:
    https://en.wikipedia.org/wiki/Functional_dependency