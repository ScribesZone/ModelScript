tâche projet.planning.gantt
===========================

:résumé: L'objectif de cette tâche est de planifier la suite du
    projet à l'aide de diagrammes de gantt.

:langage: Gantt
:résultats:
    * ``sprint<N>/provisional-plan/*``

Introduction
------------

Dans le cas de cycles de vies séquentiels (cascade ou V) ou incrémentaux
l'utilisation de diagrammes de gantt est classique. Il s'agit de
définir *en avance*, autant que faire se peut, les tâches à réaliser.
Plannifier consiste à affecter à ces tâches des ressources, dont des
ressources humaines, ainsi qu'à répartir les tâches dans le temps.

Ici, l'outil open source `gantt project`_ sera utilisé.

La plannification du projet, se fera en début de chaque sprint ou
incrément. Contrairement à ce qui se fait dans le cadre de méthodes
agiles la plannification devera couvir la période du début du projet
*jusqu'à la fin du projet*, donc au delà de la fin du sprint/incrément à
venir. Bien évidemment ce dernier sera plus détaillé.

Un "planning prévisionnel" est défini au début de chaque sprint/incrément.
Un "planning effectif" est établi à la fin de chaque sprint/incrément.
Voir la :ref:`tâche projet.planning.effectif`. On s'interesse ici à au
planning prévisionnel.

Dans le cadre d'une gestion de projet traditionnelle, c'est le chef de
projet qui assure la plannification du projet ainsi que sont suivi.

(A) Calendrier
--------------

Définir le calendrier du projet, c'est à dire le début, la fin du projet,
les jours travaillés, jours fériés, vacances, examens, etc.

Avec `gantt project`_ utiliser le menu
``Projet > Paramètres du projet > Calendrier``.

(B) Jalons
----------

Les dates des différents jalons (milestones) du projet doivent être
définies. Ces jalons correspondent aux livraisons, audits, soutenance,
etc. Toutes les événements connus dont la date est fixe et défnie.

Pour définir un jalon avec `gantt project`_ réaliser l'opération
suivante : ``Ctrl T`` puis ``Alt Enter > Général > Point bilan``.

(C) Resources
-------------

Dans le cadre de la gestion de projet traditionnelle, les membres de
l'équipe de dévelopement sont considérées comme des "ressources" ; plus
particulièrement des "ressources humaines". Dans le cadre de
`gantt project`_ ces resources doivent être déclarées. Utiliser le menu
``Ressource > Nouvelle ressource (Ctrl H)``. Utiliser le trigramme de
chaque membre en lieu et place du du nom.

(D) Tâches
----------

Dans un premier temps lister les tâches à réaliser,
*sans chercher à les ordonnancer*. Ceci se fera dans une étape utltérieure.
Utiliser dans un premier temps ``Ctrl T`` pour introduire rapidement
les différentes tâches. Ne pas chercher à déterminer la durée de chaque
tâche. Lister simplement les tâches.

Les tâches doivent faire autant que possible référence aux identificateurs
de tâches (par exemple ``projet.planning.gantt``). Ajouter, lorsque
nécessaire, un suffixe (par exemple ``projet.planning.gantt.sprint2``).

(E) Décomposition
-----------------

La granularité des tâches à prendre en compte dépend du projet.
Définir des tâches trop fines risquent d'être trop lourd. Cela rend la
gestion de projet inefficace dans la mesure où trop de tâches doivent
être plannifiées. L'unité de `gantt project`_ (ainsi que d'autres logiciels
similaires) est le jour. Une tâche d'une durée inférieure à 1 jour devra
*peut être* être regroupée avec d'autres tâches (voir ci-dessous).
Dans tous les cas de figures, plannifier un projet à la journée près
est déjà une gageure.

Les tâches peuvent être emboitées, par exemple pour décomposer une tâche
abstaite en tâches concrètes.
Utiliser ``Alt flêche->`` pour imbriquer une tâche dans une autre.

Le nom des tâches utilisées peut *éventuellement* servir pour
regrouper certaines tâches (par exemple ``bd`` pourrait regrouper les
tâches ``bd.sql.jdd`` et ``bd.sql.schema``). Cette solution n'est
cependant pas toujours la meilleure. Il peut être préférable de grouper
des tâches par incréments ou autre.

(F) Affectation
---------------

Un ou plusieurs membres de l'équipe de développement peuvent être affecté
à une tâche, et avec une quotité éventuellement inférieur à 100%. Par
exemple ``NZN`` peut être affecté à la tâche ``bd.sql.schema`` à 50%.

Pour réaliser cette affectaton avec `gantt project`_ utiliser
``Alt Enter > Ressources > Ajouter``. Il peut être utile de définir
un référent ou responsable pour la tâche. Utiliser dans ce cas
la case à cocher ``Responsable``.

L'affectation des ressources doit être faire conjointement à la
plannification. Voir ci-dessous.

(G) Plannification
------------------

Une fois les tâches et les ressources définies il s'agit de
réaliser la plannification, c'est à dire de :

*   affecter des ressources aux tâches (voir ci-dessus).
*   établir la durée prévue pour chaque tâche,
*   définir les éventuelles dépendances entre tâches,
*   définir la date de départ de chaque tâche.

Le résultat de ces différentes opérations permet de définir un planning
prévisionnel et de "caler" chaque tâche dans le temps.

Dans `gantt project`_ les propriétés d'une tâche peuvent facilement
être modifiées en tapant ``Alt Enter``. Il est ensuite possible de définir
le nombre de jour estimé ainsi que les ressources associées.

La durée des tâches dépend évidemment des ressources associées. Les
dates de début dépendent des dépendances entre les tâches et de la durée
des tâches. La plannification est donc un exercice difficile car
différentes variables doivent être prises en compte simultanément.

Dans le cadre d'une gestion de projet traditionnelle c'est le chef de
projet qui gére le planning du projet.

(H) Diagramme de gantt
----------------------

Après avoir réaliser la plannification faire une copie d'écran du
diagramme de gantt. Modifier au préalable les paramètres
d'affichage. Utiliser pour cela le menu ``Edition > Préférence`` puis
l'onglet ``Propriétés du diagramme de Gantt``, en bas d'écran la section
"Détails". Faire afficher les noms des ressources ainsi que le nom
des tâches plutôt que leur id. Créer une vue globale du diagramme
(fichier ``diagrams/plan.gan.png``) et éventuellement une ou plusieurs
autres vues plus détaillées (fichier ``diagrams/<NOM>.gan.png`` ou
``<NOM>`` est le nom de la vue).

(I) Diagramme des ressources
----------------------------

Créer un diagramme des ressources. Utiliser pour cela l'onglet
``Diagramme des Ressources`` sur l'écran principal et immédiatement au
dessus de la liste des tâches. Faire une copie d'écran correspondant
à la vision globale (fichier ``diagrams/plan.res.png``) accompagnée
éventuellement d'une ou plusieurs vues d'intérêt
``diagrams/<NOM>.res.png`` ou ``<NOM>`` est le nom de la vue)

..  _gantt project:
    https://scribestools.readthedocs.io/en/latest/ganttproject/index.html