tâche projet.planning.agile
===========================

:résumé: L'objectif de cette tâche est de planifier les tâches à
    effectuer dans le cadre d'un sprint.

:langage: GitHub
:résultats:
    * ``github:<project>``
    * ``github:<issues>``
    * ``github:<milestones>``
    * ``sprint<N>/provisional-plan/*``

Introduction
------------

L'activité de plannification est beaucoup plus légère dans le cadre
de projets en mode agiles que dans les projets séquentiels. Il s'agit
de définir d'incrément en incrément les tâches à réaliser.

Dans cette tâche GitHub sera utilisé, d'une part pour représenter les
tâches via des "issues", d'autre part en utilisant la notion de "projet"
pour suivre l'état d'avancement du projet.

(A) Jalons
----------

Définir les différents jalons (milestone) du projet (livraisons,
audits, soutenance, etc.). Utiliser pour cela les "Milestones" GitHub.
Aller sur le dépot de groupe, "Issues > Milestone > New milesone".

(B) Projet
----------

Créer un tableau de bord (appelé "project" dans GitHub) associé au dépot
de groupe. Utiliser l'onglet "project" du dépot puis "Create à project".
Definir les colonnes en fonction des besoins. Des colonnes pourront
être ajoutées par la suite. Ce tableau de bord pourra contenir
des tâches sous forme d'issues, mais également de "simples" notes.
Il est possible de définir plusieurs tableaux, par exemple pour
plusieurs sprint ou pour des "projets" s'exécutant en parallèle.
Définir la structure la plus simple adaptée au besoin de l'équipe.

(C) Tâches
----------

Définir les différentes tâches à réaliser sous forme d'issues.
Les tâches doivent faire autant que possible référence aux identificateurs
de tâches (par exemple ``projet.planning.gantt``). Ajouter, lorsque
nécessaire, un suffixe ou un préfixe (par exemple
``projet.planning.gantt.sprint2``). Le planning peut être par exemple le
nom d'un cas d'utilisation ou d'un scénario ; par exemple
``s1.bd.sql.jdd``.

Associer à chaque tâche les "labels" correspondant. Par exemple "bd".
Pour cela utiliser "Labels" dans le panneau de droite de l'issue
concernée.

(D) Décomposition
-----------------

Il pratique de lier une issue à d'autres issues. Cela peut être
utile dans le cas de tâches que l'on veut décomposer en sous tâches.
Pour cela il est suffisant de mettre ``#<N>`` dans le corps de la
sous tâches. Cette technique doit être utilisée pour faire référence
aux tâches du dépot "root", par exemple la tâche
``projet.planning.gantt.sprint2`` contiendra la référence
``l3miage/l3miage-1819-bdsi-root#13`` si le dépot root est
``l3miage/l3miage-1819-bdsi-root`` et si l'issue #13 est l'issue
``projet.planning.gantt``.

(E) Plannification
------------------

Pour estimer la complexité des tâches à réaliser l'une des techniques
est de jouer au "`poker planning`_". Réaliser une telle session avec
l'ensemble des membres de l'équipe. Définir ensuite à quel jalon telle
ou telle tâche doit être associée.

Une fois la liste des tâches établie définir à quel jalon l'issue
doit être associée. Cela permet de définir dans quel incrément la tâche
doit être réalisée. Pour définir le jalon associé à une tâche
utiliser la section "Milestone" à droite d'issue à assigner.

(F) Affectations
----------------
Les tâches peuvent être affectées à une ou plusieurs personnes. Utiliser
pour cela la section "Assignee". Contrairement aux projet en mode
séquentiels, Dans un projet en mode agile il n'est
pas nécessaire de réaliser cette affectation a priori et au début
du projet. Il est classique d'avoir un lot de tâches non assignées et
qu'un membre de l'équipe se saisisse à un moment d'une tâche.

(G) Tableau
-----------

Faire une copie d'écran du tableau ("project" github) en début de projet
et la ranger dans ``provisional-plan/diagrams/plan.github.png``.

..  _`poker planning`: https://en.wikipedia.org/wiki/Planning_poker