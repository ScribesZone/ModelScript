..  _`tâche bd.classes`:

tâche bd.classes
================

:résumé: L'objectif de cette tâche est d'annoter le "modèle de
    classes conceptuel" afin de le transformer en un "modèle de données"
    pour base de données.

:langage: :ref:`ClassScript1`
:artefacts:
    * ``concepts/classes/classes.cl1``


Introduction
------------

Le modèle de classes élaboré jusqu'à présent était un modèle
conceptuel, c'est à dire un modèle décrivant des concepts du domaine de
manière abstraite ; et ce indépendamment de toute considération
technique.

Il s'agit maintenant de transformer ce modèle abstrait en un "modèle
de données" pour base de données (voir l'illustration ci-dessous).
Ce modèle de données est un genre de modèle de classes. Il est donc
écrit en :ref:`ClassScript1` comme tout modèle de classes. Sa particularité
est qu'il contient des annotations ``{id}`` pour spécifier les clés.

::

        +--------------------------------+
        |  Modèle de classes conceptuel  |       <--- langage ClassScript1
        +--------------------------------+
                        |
                        V  + {id}                <<<< TACHE BD.CLASSES
        +================================+
        ||        MODELE DE DONNEES     ||       <<<< LANGAGE ClassScript1
        +================================+
                        |
                        V                        <--- tâche bd.relations.schema
        +--------------------------------+
        |       Modèle de relations      |       <--- langage RelationScript
        +--------------------------------+
                        |
                        V                        <--- tâche bd.sql.schema
        +--------------------------------+
        |           Schéma SQL           |       <--- langage SQL
        +--------------------------------+

Dans cette tâche il s'agit de préparer
le modèle de classes conceptuel avant de le transformer en modèle
de relations qui sera par la suite transformé en schéma SQL (cela fait
l'objet de la :ref:`tâche bd.relations.schema` puis de la
:ref:`tâche bd.sql.schema` ).

Pour simplifier le modèle de données sera défini en lieu et place du
modèle de classes conceptuel. Autrement dit dans cette tâche il est
demandé de modifier le fichier ``concepts/classes/classes.cl1``.

(A) Identifiants
----------------

Pour chaque classe, il s'agit de définir quels attributs ou quelles les
combinaisons d'attributs forment une clé. En UML cette information prend
généralement la forme d'annotations ``{id}``.

..  note::

    Rappelons que la notion de "clé" est propre au modèle relationnel.
    Dans le monde objet cette notion n'est normallement pas utilisée.
    Il n'y a pas besoin de "clés" car tout objet est systématiquement
    identifié de manière unique. Les annotations `{id}` sont donc
    uniquement utilisées dans le modèle de données en vue de la
    transformation vers le modèle relationnel.

Les annotations ``{...}`` n'étant pas disponibles en ClassScript1, on
utilisera le suffixe ``_id`` pour les identificateurs clés.
Par exemple l'attribut ``login`` devient ``login_id``.
Cette convention n'est pas parfaite mais elle permet de
visualiser les clés dans les diagrammes de classes avec l'outil USE OCL.

Dans le cas de plusieurs clés candidates le suffixe sera numéroté ;
par exemple ``prenom_id1``, ``nom_id1``, ``numen_id2``. Voir le
langage :ref:`RelationScript` pour d'autres exemples.

De manière consistante avec le langage :ref:`RelationScript` le suffixe
``_`` signifie que l'attribut fait partie d'un identifiant, mais la
notation ne spécifie pas lequel. Cette notation peut être choisie si
l'on désire avant tout améliorer la lisibilité du diagramme.
Lorsque la notation simplifiée ``_`` est utilisée il n'y a pas
d'ambiguité avec un seul identifiant (par exemple ``login_`` seul).
Par contre dans le cas de ``prenom_``, ``nom_``, ``numen_`` il n'est
pas possible de déterminer qu'il y a deux clés. Par défaut et sans
indication contraire on supposera qu'il existe une seule clé composée
de tous les attributs "soulignés". Si ce comportement par défaut
n'est pas adapté le détail des clés peut être indiqué sous forme de
contraintes explicites. Utiliser pour cela la notation pour
les contraintes textuelles (voir le langage :ref:`ClassScript1`).

Voir la :ref:`tâche bd.relations.schema` pour
plus d'information sur la manière de spécifier les clés en
:ref:`RelationScript`.

(B) Compositions
----------------


..  comment POUR LA VERSION AVEC {lid}
    Dans certains cas les objets d'une classe doivent être identifiés
    non pas de manière directe, avec son/ses identifiants, mais par
    rapport aux objets composites les contenant. Dans ce cas on utilise
    le suffixe ``_lid`` pour ``local id``, identificateur local.

Un objet composant est parfois identifié par rapport à l'objet qui
le contient.
Par exemple dans un batiment une salle peut être identifiée en partie
par son numéro, par exemple 127, mais aussi le nom du batiment, par
exemple "condillac". Dans cet exemple l'identifiant de la salle
est le couple ( "condillac" , 127 ).

..  comment
    Le numéro de salle (127)
    est un identificateur "local" par rapport au batiment. ::

..  code-block:: ClassScript1

    class Batiment
        attributes
            nom_id : String             -- exemple: "condillac"
    end

    composition Contient
        between
            Batiment[1] role batiment   -- composite : un Batiment
            Salle[*] role salles        -- composants : les Salles
    end

    class Salle                         -- clé : (nom_id,numero_id)
        attributes
            numero_id : Integer         -- exemple 127
    end



Le fonctionnement ci-dessus, l' "importation" de
l'identifiant du composite, se fait dans le cadre d'une
composition.

Dans l'exemple ci-dessus la nature de l'association, une composition,
est tout à fait logique. Un batiment est bien composé de salles.
Par contre, pour les besoins de la transformations en base de données,
il peut parfois être nécessaire de changer une association "standard" en
une composition alors que cela n'est pas naturel.

Par exemple :

..  code-block:: ClassScript1

    association ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances
    end

peut être changé en une composition :

..  code-block:: ClassScript1

    composition ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances
    end

Même si cette composition pourrait sembler contestable dans le cas d'un
modèle conceptuel, cette modification peut être valide dans un modèle
technique, ici dans le cadre de la conception de bases de données.

(C) Classes associatives
------------------------

Selon le standard UML l'identifiant d'une classe associative est
formé des identifiants des deux classes de chaque coté de la classe
associative. Considérons la classe associative suivante :

..  code-block:: ClassScript1

    class Personne
        attributes
            nom_id : String
    end

    class Societe
        attributes
            siren_id : String
    end

    associationclass Emploi
        attributes
            salaire : Integer
        between
            Personne[*] role employes
            Societe[*] role employeurs
    end

Le standard UML indique explicitement que la clé de la classe
``Emploi`` est (``nom_id``, ``siren_id``).

En complétant cet exemple un emploi pourrait de plus être identifié
par un attribut clé ``nnue_id`` (nnue signifiant par exemple Numéro
National Unique d'Emploi). Dans ce cas ``nnue_id`` est une autre clé
candidate.

Notons que dans cette modélisation on ne modélise que
l'état des employés à un moment donné. La sémantique du standard d'UML
indique en effet *"il n'y a qu'un emploi entre une personne
et une société donnée"*.

Ainsi on ne peut donc pas modéliser le fait que "paul" a travaillé la
première fois en 2007 à dans à la société "MegaTron" et une deuxième fois
en 2020. Dans cette situation il y a deux emplois entre la même société et
la même personne. Situation impossible à modéliser avec le modèle
ci-dessus.

Supposons que l'on veuille maintenant modéliser l'historique des emplois.
Une personne (par exemple paul) peut donc avoir tenu plusieurs
emplois dans la même société mais en débutant à des années
différentes (pour simplifier on consière uniquement la granularité
des années dans cet exemple). La classe associative est modifiée comme
suit :

..  code-block:: ClassScript1

    associationclass Emploi
        attributes
            salaire : Integer
            nnue_id : String
            annee_lid : Integer
        between
            Personne[*] role employes
            Societe[*] role employeurs
    end

Comme on peut le voir l'attribut ``annee`` a été suffixé avec le suffixe
``_lid`` ("lid" pour "local id").

Dans cet exemple il y a deux clés candidates pour la classe ``Emploi`` :

*   (``nnue_id``)
*   et (``nom_id``, ``siren_id``, ``annee_lid``).

Le numéro national unique d'emploi (nnue) est une clé "globale" associée
à la classe associative ``Emploi`` (comme elle l'aurait été à
n'importe qu'elle autre classe, une clé associative étant une classe).

La clé (``nom_id``, ``siren_id``, ``annee_lid``) est
liée au fait que ``Emploi`` est une classe associative.
En pratique l'attribut ``annee_lid``
(local id) a été ajouté aux deux clés "importées" des deux classes
de "chaque coté".

..  attention::

    L'utilisation du préfixe ``_lid`` est complètement incompatible avec
    le standard UML. Cette convention est pratique dans le cadre du
    développement de modèles de données en vue de transformation vers
    le modèle relationnel, mais attention à ne pas utiliser cette
    convention hors de ce contexte !

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.
