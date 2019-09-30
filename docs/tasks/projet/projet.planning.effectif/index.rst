..  _`tâche projet.planning.effectif`:

tâche projet.planning.effectif
==============================

:résumé: L'objectif de cette tâche est d'établir d'une part un planning
    intermédiaire d'autre un planning effectif en fin d'incrément.

:langages: Gantt, GitHub
:résultats:
    * ``sprint<N>/effective-plan/*``

Introduction
------------

Les plannings prévisionnels effectués en début de chaque
d'incrément/sprint sont basés sur les prévisions du déroulement
des tâches à venir. Ici s'agit ici au contraire d'effectuer :

*  un bilan intermédiaire, par exemple en milieu du déroulement
   d'un incrément,

*  un bilan en fin d'incrément/sprint.

Ces bilans rendent compte du déroulement effectif des tâches déjà
réalisées et montrent de manière prévisionnelle le planning ajuster
pour la suite du projet. Le bilan en fin d'incrément sera utilisé
pour établir le bilan prévisionnel au début de l'incrément suivant.

(A) Planning intermediaire - GitHub
-----------------------------------

Si le mode agile a été selectionné, les tâches doivent avoir
été déplacée d'une colonne à l'autre du tableau, pour refléter l'état
d'avancement du projet. Réaliser une copie d'écran
de ce tableau en milieu de sprint par exemple.
Sauvegarder cette copie dans le fichier
``sprint<N>/effective-plan/diagrammes/intermediate-plan.github.png``.

(B) Planning intermediaire - Gantt
----------------------------------

Si le modèle de gantt est utilisé, faire le bilan sur les
tâches effectuées. Utiliser la possibilité de définir l'état d'avancement
d'une tâche. Soit en utilisant le champ ``Avancement`` dans le panneau
de propriété de tâche (``Alt Enter``), soit en déplacant le curseur de
gauche à droite directement sur le diagramme de gantt. L'avancement de
la tâche est représentée par un trait noir à l'interieur de la tâche.
Sauvegarder le modèle intermédiaire dans
``sprint<N>/effective-plan/intermediate-plan.gan``.
Réaliser une copie d'écran dans
``sprint<N>/effective-plan/diagrammes/intermediate-plan.gan.png``.

(C) Planning effectif - GitHub
------------------------------

Si GitHub est utilisé réaliser en fin de sprint la même opération que pour
le plan intermédiaire. Sauvegarder l'image du tableau dans le fichier
``sprint<N>/effective-plan/diagrammes/plan.github.png``

(D) Planning effectif - Gantt
-----------------------------

Si le modèle de gantt est utilisé réaliser en fin d'incrément/de projet
la même opération que pour le plan intermédiaire. Sauvegarder le version
finale du plan dans
``sprint<N>/effective-plan/plan.gan`` et une copie d'écran dans
``sprint<N>/effective-plan/diagrammes/plan.gan.png``.
