..  _`tâche projet.standup`:

tâche projet.standup
====================

:résumé: Cette tâche consiste à réaliser chaque jour un
     "standup meeting" ou "daily scrum meeting".

Introduction
------------

Le "daily scrum meeting" (ou "standup meeting") est l'un des rituels
les plus populaires associé à la méthode scrum_.

..  note::

    L'issue ``projet.standup`` dans le dépot de groupe sera utilisée pour
    le suivi des standup meetings. Différents commentaires seront ajoutés
    dans cette issues au fur et à mesure de l'avancement du projet. Voir
    ci-dessous pour plus de détails.

(A) Patrons
-----------

Contrairement à ce que l'on peut imaginer les standup meetings sont
bien plus que des meetings debout. Ces réunions peuvent
et doivent être organisés autour d'un certain nombre de patrons.
Si un scrum master a été nommé, l'article "It's Not Just Standing Up:
Patterns for Daily Standup Meetings" (`article`_)
est une lecture de choix. L'article peut être survolé. La section
"Patterns of daily stand-up meetings" est la plus intéressante. Cette
section donne des indications sur la manière de gérer les standup meetings.

(B) Horaire
-----------

Il est important de choisir un horaire fixe pour les standup meeting,
en début de journée.  Indiquer cet horaire sous forme de commentaire dans
l'issue ``projet.standup`` du groupe. Si a un moment donné l'horaire est
changé il est impératif d'indiquer ce changement. Donner les raisons de ce
changement ainsi que le nouvel horaire.

..  attention::

    Le standup meeting doit démarrer toujours à l'heure prévue, même si
    un membre du groupe est en retard. Les retards doivent être
    exceptionnels.

(C) Présence
------------

Il est absolument indispensable que tous les membres du groupe assistent
systématiquement et sans exception à tous les standup meetings.

(D) Standup meetings
--------------------

Les standup meetings doivent avoir lieu de manière *systématique* chaque
jour, sauf les jours où d'autres événements ont lieu (audits par exemple).
Chaque jour, le commentaire *"fait, durée MM"* sera ajouté à la liste des
commentaires, indiquant simplement que la réunion a été faite et à duré
environ MM minutes.

..  attention::

    RAPPEL: les standup meetings ne doivent pas excéder 15 minutes,
    mais en revanche ils doivent être fait de manière systèmatique.

(E) Empêchements
----------------

Si un empêchement ("impediment" dans la terminologe scrum) survient et
qu'il ne peut pas être résolu immédiatement, le noter dans le
modèle de suivi (``projet/suivis/suivis.trs``). Utiliser le mot clé
``impediment`` en :ref:`TrackScript`.

(F) Discussions
---------------

Les discussions entre deux ou plusieurs membres du groupe sont à
proscrire. L'idée du standup meeting n'est pas de résoudre des
problèmes mais plutôt d'informer chaque membre du groupe de
l'état d'avancement des différentes tâches ainsi que de
donner une vision sur ce qui va être accompli dans la journée.
Si des dicussions sont nécessaires celles-ci peuvent être tenues
immédiatement après le standup meeting ou à tout autre moment.

Utiliser le modèle de suivis (``projet/suivis/suivis.trs``)
pour consigner en :ref:`TrackScript` les décisions prises et pour
modéliser un éventuel plan d'action.


..  _scrum:
    https://en.wikipedia.org/wiki/Scrum_(software_development)

..  _article:
    https://www.martinfowler.com/articles/itsNotJustStandingUp.html