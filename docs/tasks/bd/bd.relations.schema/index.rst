..  _`tâche bd.relations.schema`:


tâche bd.relations.schema
=========================

:résumé: Cette tâche a pour objectif de créer le schéma relationnel
    à partir du modèle modèle de données si celui-ci existe.

:langage: :ref:`RelationScript`
:artefacts:
    * ``bd/relations/relations.res``


Introduction
------------

Le modèle de relations (aussi appelé "schéma relationnel") doit être créé
à partir du modèle de données si celui-ci existe. Le modèle de relations
est alors l'ensemble des relations et des contraintes que l'on peut
déduire à partir du modèle de données (exprimé sous forme d'un modèle
de classes décoré par des annotations ``_id``). L'enchaînement des
tâches est généralement le suivant :

::

        +--------------------------------+
        |  Modèle de classes conceptuel  |       <--- langage ClassScript1
        +--------------------------------+
                        |
                        V                        <--- tâche bd.classes
        +--------------------------------+
        ||        Modèle de données      |       <--- langage ClassScript1
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


.. note::

    Dans cette tâche seul le schéma de données est considéré. On ne prend
    pas en compte d'éventuels jeux de données (datasets).
    Dans cette tâche aucun contenu n'est créé.

Le fichier a modifier dans cette tâche est ``bd/relations/relations.res``.
:ref:`RelationScript` est le langage utilisé. Se
référer à la documentation pour plus d'exemples.

(A) Transformations
-------------------

..  attention::

    Si le modèle de relations est créé à partir de zéro (en
    l'absence de modèle de données) alors cette partie peut être ignorée.

Lorsque des règles de transformation "standards" existent alors
celles-ci doivent être respectées à chaque fois que faire ce peut.
Plus précisemment si une liste précise de transformations nommées
a été fournie, il s'agit alors d'indiquer et de justifier
l'application de ces transformations. Cela se fait à l'aide
des mots-clés ``transformation``, ``from`` et ``rule`` comme illustré
dans l'exemple suivant :

..  code-block:: RelationScript

    relation LesResponsables(departement_id:String, boss:String)
        ...
        transformation
            from Responsable
            rule ClasseVersRelation
            | L'attribut boss a été transformé en String car
            | ...

Dans cet exemple ``Responsable`` est un élement du modèle de classes
à l'origine de la transformation. On suppose de plus qu'il existe une
règle nommée ``ClasseVersRelation``.
Dans des exemples plus complexes une relation peut être le résultat
de la transformation de plusieurs éléments (classes, association, etc.)
et peut être de plusieurs règles.

Dans certains cas la transformation est plus complexe ou sort du cadre
des transformations standards. On utilise alors la documentation de la
transformation pour justifier quelle(s) (autres) transformation(s) a/ont
été appliquée(s). Dans l'exemple ci-dessus ces justifications correspondent
au texte commençant par ``| L'attribut ...``.

(B) Contraintes
---------------

Il s'agit ensuite de définir les contraintes intégrité suivantes :

*   **les contraintes sur les colonnes**.
    En :ref:`RelationScript` les contraintes de domaine peuvent soit
    être indiquées dans le profil de la relation (par exemple
    ``R(x:String)``) ou sous forme de contraintes explicites (par exemple
    ``dom(x)=String`` dans la section ``constraints``). Voir la
    documentation de :ref:`RelationScript` pour plus de détails.

*   **les contraintes de clés**.
    Les contraintes de clés proviennent directement des annotations
    ``{id}`` du modèle de données (si il existe). Les clés peuvent
    soit être définies dans le profil de la relation (par exemple
    ``Compte(login_id)`` soit le mot clé ``key`` dans la section
    ``constraints``. Voir la documentation de :ref:`RelationScript`
    pour plus de détails.

*   **les contraintes d'intégrité référentielle**. Elles sont exprimées
    en algèbre relationelle sous forme de :ref:`RelationScript`
    (par exemple ``R[x] C= S[y]``).

*   **les autres contraintes**. Si une contrainte ne peut pas être
    exprimées en utilisant l'algèbre relationnelle,
    la contrainte sera spécifiée sous forme textuelle. Si cette
    contrainte provient du modèle de classes conceptuel, alors répéter
    uniquement le nom de la contrainte (par exemple
    ``constraint AtLeastForItemPerDay``).

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.