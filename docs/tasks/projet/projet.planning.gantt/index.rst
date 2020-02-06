..  _`tâche projet.planning.gantt`:

tâche projet.planning.gantt
===========================

:résumé: L'objectif de cette tâche est de planifier la suite du
    projet à l'aide de diagrammes de gantt.

:langage: Gantt
:résultats:
    * ``sprint<N>/provisionnel/*``

Introduction
------------

Dans le cas de cycles de vies séquentiels (cascade ou V) ou incrémentaux
l'utilisation de diagrammes de gantt est classique. Il s'agit de
définir *en avance*, autant que faire se peut, les tâches à réaliser.
Planifier consiste à affecter à ces tâches des ressources, dont des
ressources humaines, ainsi qu'à répartir les tâches dans le temps,
en estimant, entre autre, la durée des tâches.

Ici, l'outil open source `gantt project`_ sera utilisé.

La planification du projet, se fera en début de chaque sprint ou
incrément. Contrairement à ce qui se fait dans le cadre de méthodes
agiles la planification devra couvrir la période du début du projet
*jusqu'à la fin du projet*, donc au delà de la fin du sprint/incrément à
venir. Bien évidemment ce dernier sera plus détaillé.

Un "planning prévisionnel" est défini au début de chaque sprint/incrément.
Un "planning effectif" est établi à la fin de chaque sprint/incrément.
Voir la :ref:`tâche projet.planning.effectif`. **Dans cette tâche on
s'interesse au planning prévisionnel.**

Dans le cadre d'une gestion de projet traditionnelle, c'est le chef de
projet qui assure la planification du projet ainsi que son suivi.

..  note::

    Le resultat de cette tâche sera déposé dans le répertoire
    ``projet/sprint<N>/plannings/previsionnel`` où ``<N>`` est le
    numéro du sprint.

Lancer `gantt project`_ (il doit au préalable avoir été installé) : ::

    ganttproject

Ouvrir le fichier correspondant à l'incrément concerné. Par
exemple pour le sprint 1, ouvrir le fichier suivant : ::

    projet/sprint1/plannings/previsionnel/planning-previsionnel.gan

Le reste de cette tâche va consister à définir le planning
prévisionnel, et donc à compléter ce fichier.

..  note::

    Si un projet initial est fourni il s'agit de le compléter ou
    de l'adapter selon les cas. Certaines tâches présentées ci-dessous
    peuvent ne pas être nécessaires.

..  note::

    Ci-dessous on suppose que l'interface graphique de `gantt project`_
    est en Français. Pour choisir la langue utiliser le menu
    ``Edit > Settings > Application UI > Language``.

(A) Calendrier
--------------

La première tâche consiste à définir le calendrier du projet, c'est à dire
le début, la fin du projet, les jours travaillés, jours fériés, vacances,
examens, etc.

Utiliser pour cela le menu
``Projet > Paramètres du projet > Calendrier``.

(B) Jalons
----------

Les dates des différents jalons (milestones) du projet doivent être
définies. Ces jalons correspondent par exemple aux livraisons,
audits et à la soutenance. Ajouter tous les événements connus et dont la
date est fixe et défnie.

Dans `gantt project`_ un jalon est un cas particulier de tâche.
La création d'un jalon se fait en deux temps :

*   créer une tâche avec ``Ctrl T``

*   transformer cette tâche en jalon avec
    ``Alt Enter > Général > Point bilan``.

(C) Resources
-------------

Dans le cadre de la gestion de projet traditionnelle, les membres de
l'équipe de dévelopement sont considérées comme des "ressources" ; plus
particulièrement des "ressources humaines". Dans le cadre de
`gantt project`_ ces resources doivent être déclarées car elles vont
être affectées aux tâches. Utiliser l'onglet
``Resource Chart`` pour voir l'ensemble des ressources.

Utiliser le menu ``Ressource > Nouvelle ressource (Ctrl H)``.
Utiliser le trigramme de chaque membre en lieu et place du du nom.

(D) Tâches
----------

Dans un premier temps lister les tâches à réaliser,
*sans chercher à les ordonnancer*. Ceci se fera dans une étape utltérieure.
Utiliser dans un premier temps ``Ctrl T`` pour introduire rapidement
les différentes tâches. Ne pas chercher à déterminer la durée de chaque
tâche. Lister simplement les tâches.

Lorsque les tâches font références à des tâches ModelScript utiliser leur
idendificateur (par exemple ``projet.planning.gantt``). Ajouter, lorsque
nécessaire, un suffixe (par exemple ``projet.planning.gantt.sprint2``).

(E) Décomposition
-----------------

La granularité des tâches à prendre en compte dépend du projet.
Définir des tâches trop fines risquent d'être trop lourd. Cela rend la
gestion de projet inefficace dans la mesure où trop de tâches doivent
être planifiées. L'unité de `gantt project`_ (ainsi que d'autres logiciels
similaires) est le jour. Une tâche d'une durée inférieure à 1 jour devra
*peut être* être regroupée avec d'autres tâches (voir ci-dessous).
Dans tous les cas de figures, planifier un projet à la journée près
est déjà une complexe.

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
à une tâche, et avec une quotité éventuellement inférieure à 100%. Par
exemple ``NZN`` peut être affecté à la tâche ``bd.sql.schema`` à 50%.

Pour réaliser cette affectaton avec `gantt project`_ utiliser
``Alt Enter > Ressources > Ajouter``. Il peut être utile de définir
un référent ou responsable pour la tâche. Utiliser dans ce cas
la case à cocher ``Responsable``.

L'affectation des ressources doit être faire conjointement à la
planification. Voir ci-dessous.

(G) planification
------------------

Une fois les tâches et les ressources définies il s'agit de
réaliser la planification, c'est à dire :

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
des tâches. La planification est donc un exercice difficile car
différentes variables doivent être prises en compte simultanément.

Dans le cadre d'une gestion de projet traditionnelle c'est le chef de
projet qui gére le planning du projet.

(H) Diagramme de gantt
----------------------

Après avoir réalisé la planification faire une copie d'écran du
diagramme de gantt. Modifier au préalable les paramètres
d'affichage. Utiliser pour cela le menu ``Edition > Préférence`` puis
l'onglet ``Propriétés du diagramme de Gantt``, en bas d'écran la section
"Détails". Faire afficher les noms des ressources ainsi que le nom
des tâches plutôt que leur id. Créer une vue globale du diagramme
(fichier ``diagrammes/plan.gan.png``) et éventuellement une ou plusieurs
autres vues plus détaillées (fichier ``diagrammes/<NOM>.gan.png`` ou
``<NOM>`` est le nom de la vue).

(I) Diagramme des ressources
----------------------------

Créer un diagramme des ressources. Utiliser pour cela l'onglet
``Diagramme des Ressources`` sur l'écran principal et immédiatement au
dessus de la liste des tâches. Faire une copie d'écran correspondant
à la vision globale (fichier ``diagrammes/plan.res.png``) accompagnée
éventuellement d'une ou plusieurs vues d'intérêt
``diagrammes/<NOM>.res.png`` ou ``<NOM>`` est le nom de la vue)

..  _gantt project:
    https://scribestools.readthedocs.io/en/latest/ganttproject/index.html