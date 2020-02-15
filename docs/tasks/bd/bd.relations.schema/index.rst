..  _`tâche bd.relations.schema`:

.. highlight:: RelationScript

tâche bd.relations.schema
=========================

:résumé: Cette tâche a pour objectif de créer le schéma relationnel
    à partir du modèle de données (si celui-ci existe).

:langage: :ref:`RelationScript`
:artefacts:
    * ``bd/relations/relations.res``


Introduction
------------

Le schéma de production d'une base de données à partir d'un modèle de
classes est le suivant.

::

        +--------------------------------+
        |  Modèle de classes conceptuel  |       <--- langage ClassScript1
        +--------------------------------+
                        |
                        V                        <--- tâche bd.classes
        +--------------------------------+
        |         Modèle de données      |       <--- langage ClassScript1
        +--------------------------------+
                        |
                        V                        <--- TACHE BD.RELATIONS.SCHEMA
        +================================+
        ||       MODELE DE RELATIONS    ||       <--- LANGAGE RelationScript
        +================================+
                        |
                        V                        <--- tâche bd.sql.schema
        +--------------------------------+
        |           Schéma SQL           |       <--- langage SQL
        +--------------------------------+

Dans un tel contexte on s'intéresse à la
troisème étape. Sinon, il s'agit simplement de créer un modèle de
relation à partir de zéro.

.. note::

    Dans cette tâche seul le schéma de données est considéré. On ne prend
    pas en compte d'éventuels jeux de données (datasets).


Le fichier a modifier dans cette tâche est ``bd/relations/relations.res``.
:ref:`RelationScript` est le langage utilisé. Se
référer à la documentation pour plus d'exemples.

(A) Columns
-----------

La première étape consiste à définir les relations et leurs colonnes. ::

    relation LesAppartements
        columns
            nom_ : String
            numero_ : Integer
            superficie : Real
            nbDePieces : Integer

La section ``columns`` définit les colonnes de la relation
``LesAppartements``. D'autres notations sont possibles
(:ref:`documentation<RelationScript_Relations>`).

(B) Transformation
------------------

Dans le cas où le modèle de relations est dérivé à partir
d'un modèle de classe il est important de documenter le
processus de transformation suivi.
La section ``transformation`` est alors ajouté à chaque relation
dérivée. ::

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

Dans cet exemple la transformation effectuée a été basé sur
l'application de trois règles (``R_Class``, ``R_Compo`` et
``R_OneToMany``) (:ref:`documentation<RelationScript_Transformation>`).

(C) Contraintes
---------------

Il s'agit ensuite de définir les contraintes intégrité suivantes :

*   **les contraintes de domaine**.
    Les contraintes de domaine peuvent soit être indiquées dans le
    profil de la relation (par exemple ``R(x:String)`` ou de
    façon plus concise ``R(x:s)``) soit être sous forme de
    contraintes explicites (par exemple
    ``dom(x)=String`` dans la section ``constraints``)
    (:ref:`documentation<RelationScript_ContrainteDeDomaine>`).

*   **les contraintes de clés**.
    Les clés peuvent soit être définies dans le profil de la relation
    (par exemple ``Compte(login_id)``), soit via mot clé ``key``
    (:ref:`documentation<RelationScript_Cles>`).

*   **les contraintes d'intégrité référentielle**. Elles sont exprimées
    en langue naturelle ou en algèbre relationelle
    (:ref:`documentation<RelationScript_ContrainteDIntegrite>`).

Se référer à la documentation de :ref:`RelationScript` pour plus
d'exemples.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.