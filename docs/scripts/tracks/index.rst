.. .. coding=utf-8

.. highlight:: TrackScript

.. index::  ! .trs, ! TrackScript
    pair: Script ; TrackScript

.. _TrackScript:

TrackScript
===========

Examples
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
        date: 2019-05-21
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
        date: 2019-05-21
        who: ADZ NZW PGI ZSE

    decision D2: Entree en retard de plus d'un jour
        | La `Rentree` d'une `Oeuvre` en `Retard` de plus d'un
        | jour doit être prise en compte contrairement à ce
        | que peut laisser supposer la ligne [A34].
        date: 2019-05-21
        who: ADZ NZW PGI ZSE

TaskScript
----------

Un projet le modèle de suivi peut par exemple être utilisé dans deux
contextes :

*   **ordres du jour** de réunions. Le client n'étant pas disponible
    en permanence, les questions et hypothèses doivent être consignées
    et sérialisée pour pouvoir soulever ces élements de suivi lors
    d'une prochaine réunion avec le "client". Un tel modèle peut être
    utilisé pour établir l'ordre du jour d'une réunion future.

*   **compte rendus**. Il est également possible de définir des
    "décisions" dans le modèle de suivi. Bon nombre de décisions
    sont prises lors de réunions, et ces décisions peuvent être
    référencées dans les comptes rendus de réunions.

Concepts
--------

The track model aims to track information about other models, namely
**questions**, **hypothesis**, **decisions**. These items are tracked in
order :

* (1) to prepare the agenda of future meetings and
* (2) to estabish minute meetings afterward.

This also allow to track who was involved in which question/hypothesis/decision.

Questions
---------

**Questions** are interrogations that the members of the team have about
some part of the project. By contrast to **hypothesis**, a **question** is
a blocking event. No assumption is made ; the question has to be answered.

Hypothesis
----------

In case of doubts the team can emit some **hypothesis**. These hypothesis
are recorded so that they can be validated or not during an upcoming meeting
for instance.

Decisions
---------

Decisions that are taken, during a meeting for instance, can be recorded
as **decisions**.

Rules
-----

* Chaque question/hypothèse/décision doit être identifiée de
  manière unique. Par exemple D3, Q3 et H12.

* Réferencer ces identificateurs (e.g. ``[H12]``) dans le(s)
  modèle(s) impactés. En commentaire ou autre selon les
  langages.

* La formulation des questions/hypothèses doit
  impérativement être précise et faire référence aux
  termes définis dans le glossaire (entre backquotes).

* Une question/hypothèse doit avoir un titre court mais
  le plus explicatif possible.

* Les questions/hypothèses doivent être aussi
  pertinentes que possible du point de vue du client.
  En particulier éviter de poser des questions pouvant
  sembler infondées de la part du client.
