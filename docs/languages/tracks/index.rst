.. .. coding=utf-8

.. highlight:: TrackScript

.. index::  ! .trs, ! TrackScript
    pair: Script ; TrackScript

.. _TrackScript:

TrackScript
===========

Exemples
--------

::

    track model CyberBibliobus
    import glossary model from '../glossaries/glossaries.gls'

    question Q1: Catalogue des oeuvres
        | Il est fait mention des `Oeuvres` et de leurs `Auteurs` mais
        | le moyen de créer/maintenir ces informations n'est pas précisé.
        | Qui crée/maintient le `Catalogue` ?
        | Est-ce un système externe avec lequel `CyberBibliotheque` doit
        | s'interfacer ?
        github: #3
        priority: low
        status: closed
        who: ERT PGI NZW
        conclusion
            | La gestion du `Cataloque` des `Oeuvres` est en dehors
            | du périmètre de la version v3.2. Pour l'instant le
            | `Catalogue` sera figé et fourni via un fichier XML.

    question Q2: Rendu en retard
        | Aucune information n'est fournie sur le mode de `Rendu`
        | dans le cas ou celui-ci se fait en retard. Le contenu
        | de la ligne [A4] doit être précisé avant de pouvoir réalisé
        | la définition du cas d'utilisation `RendreUnItem`.
        status: open
        who: KET MER

    hypothesis H1: Transfert de stocks
        | On suppose que le transfert de `Stocks` se fait "en dehors"
        | de `CyberBibliotheque` [A31][A32] et que la seule fonctionnalité
        | qui doit ếtre développée est le faire que les `Magaziniers`
        | incrémente/décrémente les `Stocks` de leur `Bibliotheque`
        | respective [A33].
        github: #12
        status: validated
        date: 2020-05-21
        who: NZW

    hypothesis H2: Emprunt enseignant de 30 jours
        | Les lignes [A23] et [A26] semble contradictoire. Il semble
        | logique de ne pas restreindre le `Personel` à la contrainte
        | des 15 jours indiquée en [A23]?
        priority: low
        status: open

    decision D1: Pas de transfert des livres
        | La gestion gestion du `Transfert` des `Livres` ne sera
        | pas prise en compte avant la version v2.
        date: 2020-05-21
        who: ADZ NZW PGI ZSE

    decision D2: Entree en retard de plus d'un jour
        | La `Rentree` d'une `Oeuvre` en `Retard` de plus d'un
        | jour doit être prise en compte contrairement à ce
        | que peut laisser supposer la ligne [A34].
        date: 2020-05-21
        who: ADZ NZW PGI ZSE

    impediment I1: Pas de diagrammes via USE OCL
        | Le logiciel USE OCL fonctionne en mode textuel
        | mais pas en mode graphique. Il est donc impossible
        | à ce stade de créer des diagrammes de classes et des
        | diagrammes d'objets. Les tâches concepts.classes.diag
        | et concepts.objets.diag sont en attente.
        date: 2020-03-18
        who: ADZ JFE

    impediment I2: Pas de salle de réunion disponible
        | La salle de réunion allouée à l'équipe n'est généralement
        | pas disponible le vendredi pour les retrospectives.
        date: 2020-03-20
        who: NZW


TaskScript
----------

Un projet le modèle de suivi peut être utilisé dans de multiples
contextes. Par exemple :

*   **ordres du jour** de réunions. Le client n'étant pas disponible
    en permanence, les questions et hypothèses doivent être consignées
    et sérialisées. Ces différents points peuvent ensuite être soulevés lors
    d'une prochaine réunion avec le "client". Un tel modèle peut donc être
    utilisé pour établir l'ordre du jour d'une réunion future.

*   **compte rendus**. Il est possible de définir des
    "décisions" dans le modèle de suivi. Bon nombre de décisions
    sont prises lors de réunions, et ces décisions peuvent être
    référencées dans les comptes rendus de réunions.

*   **traçabilité**. Le modèle de suivi sert de support à la traçabilité
    tout au long du projet. Il est par exemple possible de déterminer
    quelles personnes, quelles parties prenantes sont ou ont été impliquées
    dans telle ou telle décision.

Concepts
--------

Le modèle de suivi a pour objectifs de de consigner différents
*points de suivis* :

*   des **questions**,
*   des **hypothèses**,
*   des **décisions**,
*   des **empêchements**,
*   des **problèmes**.

La différence entre ces différents points de suivi sont définis ci-dessous.

Questions
---------

Les **questions** sont des interrogations que les membres de l"équipe
peuvent avoir à propos d'une partie du projet. Par contraste avec les
*hypothèses*, une *question* a un certain caractère bloquant : aucune
supposition n'est faite ; la question doit être répondue.

Hypothèses
----------

En cas de doute les membres de l'équipe peuvent émettre des
**hypothèses** lorsqu'un point du projet n'est pas clair. Ces *hypothèses*
permettent à l'équipe de continuer à travailler. Chaque *hypothèse* est
enregistrée de manière à être validée ou invalidée lors d'une
réunion avec le client par exemple. Lorsqu'une *hypothèse* est émise
l'équipe prend un risque par rapport à tous les développements
basés sur cette *hypothèse*. Evaluer ce risque est fondamental.
Si trop de développements dépendent d'une *hypothèse* il est sans
doute préférable de poser une *question* et d'attendre la réponse.

Décisions
---------

Dans un projet, différentes **décisions** sont prises à différents
moments du cycle de vie. Ce peut être le cas lors de réunions entre
différentes parties prenantes. Il est essentiel de rendre explicite
le contenu de la décision, la date à laquelle elle a été prise,
qui a pris cette décision, qui l'a validé, etc. Un compte rendu
de réunion fait typiquement référence à une série de décision.
D'autres décisions peuvent être prises à d'autres moments par
le client ou l'équipe de développement.

Empêchements
------------

Le déroulement d'un projet est parfois freiné par des
**empêchements**. Un *empêchement* correspond à un problème qui
survient dans le déroulement d'un projet et qui limite ou
empêche certaines tâches de progresser normallement. Ce peut
être l'indisponibilité d'une salle de réunion, l'indisponibilité
d'un serveur, le fait qu'une question n'a pas été répondue et
que cela devienne un caractère bloquant, etc. Un *empêchement*
signale à un interlocuteur (tel qu'un chef de projet par exemple)
qu'une action doit être menée pour contrecarrer cet *empêchment*.
Identifier et lister les *empêchements* est un élément important
de la méthode Scrum.

Problèmes
---------

Le développement de tout projet soulève, à un moment ou à un autre,
différents **problèmes**. Ces *problèmes* doivent être identifiés,
décrits, traités, suivis, etc. Le terme "problème" est volontairement
générique. Tombent dans cette catégorie tous les éléments de suivis
n'étant pas dans une autre catégorie plus spécifique (en particulier
les *questions* et les *empêchements*.

..  _Suivi_Règles:

Règles
------

*   Chaque point de suivi doit être identifié de
    manière unique. Par exemple D3, Q3 et H12, I2, P2, etc.

*   Réferencer ces identificateurs entre crochets (e.g. ``[H12]``)
    dans le(s) modèle(s) impactés. En commentaire ou autre selon
    les langages.

*   La formulation des points de suivis doit impérativement être
    précise et faire référence aux termes définis dans le glossaire
    (entre backquotes).

*   Les points de suivis doivent avoir un titre court mais le plus
    explicatif possible.

*   Les points de suivis doivent être aussi pertinents que possible
    du point de de vue des différentes parties prenantes impliquées.
    Par exemple ne pas utiliser de vocabulaire technique si un
    point de suivi est adressé à un client.

