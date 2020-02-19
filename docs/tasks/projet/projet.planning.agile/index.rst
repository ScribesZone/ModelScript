..  _`tâche projet.planning.agile`:

tâche projet.planning.agile
===========================

:résumé: L'objectif de cette tâche est de planifier les tâches à
    effectuer dans le cadre d'un sprint.

:langage: GitHub
:résultats:
    * ``github:<project>``
    * ``github:<issues>``
    * ``github:<milestones>``
    * ``projet/sprint<N>/provisional-plan/*``

Introduction
------------

L'activité de planification est beaucoup plus légère dans le cadre
de projets en mode agile que dans les projets séquentiels
(voir la :ref:`tâche projet.planning.gantt`). Il s'agit ici
de définir d'incrément en incrément les tâches à réaliser.

Dans cette tâche GitHub sera utilisé, d'une part pour représenter les
tâches via des "issues", d'autre part en utilisant la notion de "projet"
pour suivre l'état d'avancement du projet.

(A) Jalons
----------

Définir les différents jalons (milestone) du projet (livraisons,
audits, soutenance, etc.). Utiliser pour cela les "Milestones" GitHub.
Aller sur le dépot de groupe, puis ``Issues > Milestone > New milestone``.

(B) Projet
----------

Créer un tableau de bord (appelé "project" dans GitHub) associé au dépot
de groupe. Utiliser l'onglet ``project`` du dépot puis
``Create a project``.
Définir les colonnes en fonction des besoins.

..  note::

    Les colonnes pourront être ajoutées par la suite au fur et à mesure
    des besoins.

Ce tableau de bord pourra contenir
des tâches sous forme d'issues, mais également de "simples" notes.
Il est possible de définir plusieurs tableaux, par exemple pour
plusieurs sprint ou pour des "projets" s'exécutant en parallèle.
Définir la structure la plus simple possible mais adaptée au besoin
de l'équipe. Cette structure pourra être adaptée au fil de l'eau.

(C) Tâches
----------

Il s'agit ici de définir les tâches du projet sous forme
d'issues GitHub. On cherche plus particulièrement a
**établir la traçabilité** entre :

*   (1) le processus ModelScript
*   (2) le processus suivi effectivement.

Lorsqu'une tâche est dérivée directemment d'une tâche de référence
ModelScript le nom de l'issue y fera référence directement. Par exemple
la tâche ``sprint2.projet.planning.gantt`` indiquera qu'il
s'agit d'effectuer la tâche ``projet.planning.gantt`` pour le ``sprint2``.
De même on pourra utiliser un nom comme ``s1,d1,d2.concepts.classes``
pour la tâche consistant à compléter le modèle de classes avec le
scénario ``s1`` et les incréments ``d1`` et ``d2``.

..  note::

    GitHub permet de créer des références entre issues, sans pour
    autant donner de recommendations sur la manière d'utiliser cette
    fonctionnalité. Ci-dessous cette l'utilisation de cette fonctionnalité
    est formalisée afin d'assurer la traçabilité entre issues.

(D) Références
--------------

Utiliser le nom de la tâche pour référencer la tâche "mère"
n'est pas toujours facile ni souhaitable. Dans le cas de relation
"mère - fille" on utilisera par contre de manière systèmatique le mot
clé ``org`` suivi du numéro d'issue de la tâche mère. Par exemple si
une tâche ``#68`` dérive de la tâche ``#34`` alors le corps de la tâche
``#68`` débutera par : ::

    org #34

Les tâches peuvent ainsi être imbriquées. Si une tâche ne correspond
à aucune tâche ModelScript alors ajouter le label ``Extra`` à cette tâche
pour mettre en l'avant qu'elle sort du processus. Voir la section
suivante pour les labels.

L'exemple ci-dessous montre un arbre des tâches avec la tâche principale
``concepts.classes`` étiquettée ``ModelScript`` car il s'agit d'une
tâche de référence du processus. Les tâches ``#34``, ``#68`` et ``#122``
sont elles des sous-tâches.
La tâche ``#79`` n'a pas de tâche parente. Elle a donc le
label ``Extra`` pour indiquer que cette tâche échappe au processus
ModelScript. ::

    #17 concepts.classes [ModelScript]
        #34 s1,d1-3.concepts.classes     org #17
            #68 Ajouter la notion d'employés et de bureaux    org #34
            #122 Ajouter la notion d'envois    org #34
    #79 Faire de l'espace sur le disque    [Extra]


(E) Labels
----------

Associer à chaque tâche les "labels" correspondant. Par exemple "bd".
Pour cela utiliser ``Labels`` dans le panneau de droite de l'issue
concernée.

(F) Planification
-----------------

Pour estimer la complexité des tâches à réaliser l'une des techniques
est de jouer au "`poker planning`_". Réaliser une telle session avec
l'ensemble des membres de l'équipe. Définir ensuite à quel jalon telle
ou telle tâche doit être associée.

Une fois la liste des tâches établie définir à quel jalon l'issue
doit être associée. Cela permet de définir dans quel incrément la tâche
doit être réalisée. Pour définir le jalon associé à une tâche
utiliser la section ``Milestone`` à droite d'issue à assigner.

(G) Affectations
----------------

Les tâches peuvent être affectées à une ou plusieurs personnes. Utiliser
pour cela la section ``Assignee``. Contrairement aux projet en mode
séquentiel, dans un projet en mode agile il n'est
pas nécessaire de réaliser cette affectation a priori et au début
du projet. Il est classique d'avoir un lot de tâches non assignées et
qu'un membre de l'équipe se saisisse à un moment donné d'une tâche.

(H) Tableau
-----------

Faire une copie d'écran du tableau ("project" github) en début de projet
et la ranger dans ``provisional-plan/diagrammes/plan.github.png``.

..  _`poker planning`: https://en.wikipedia.org/wiki/Planning_poker