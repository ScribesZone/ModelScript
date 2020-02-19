..  _`tâche projet.audit`:

tâche projet.audit
==================

:résumé: L'objectif de cette tâche est (1) de préparer l'audit,
    (2) de réaliser cet audit, puis (3) d'en faire la synthèse.

:artefacts:
    * ``projet/sprint<N>/audit/*``

Introduction
------------

L'objectif d'un audit est de faire le bilan, le plus objectif possible
des résultats obtenus pendant un incrément ainsi que du processus
méthodologique menant à ces résultats.

Il s'agit pour l'équipe de développement d'indiquer :

* ce qui a été fait, doit ếtre amélioré, reste à faire,
  (se baser sur les fichers ``status.md``),

* quels résultats ont été produits,

* quelles tâches ont été réalisées,

* quelles difficultés ont été rencontrées,

* quels empêchements bloquent ou freinent l'avancée du projet.

Il ne s'agit pas de "vendre" ce qui a été fait en en exagérant
les mérites, mais plutôt de convaincre que ce qui a été fait est
solide et que l'équipe est suffisemment fiable pour mériter le
l'octroi des ressources nécessaire à un nouvel incrément.

L'objectif de l'audit lui-même est d'intéragir avec le comité d'audit,
de l'informer, mais aussi de recueillir les recommendations émises
afin d'établir un rapport d'audit suivi d'actions précises.

(A) Transparents
----------------

Chaque audit est basé sur une présentation effectuée à base
de transparents. Les fichiers
``projet/sprint<N>/audit/audit-<N>.odp``
où ``<N>`` est un numéro de version correspondent aux versions
successivent des transparents.
La dernière version doit être convertie en fichier .pdf dans
``projet/sprint<N>/audit/audit.pdf``

Les différentes capture d'écran réalisée au cours de projet doivent
servir de base pour le contenu de la présentation.


(B) Présentation
----------------

Lors de la présentation effective les transparents présentés doivent
être ceux présent dans la dernière version de GitHub.

Chaque membre du groupe doit parler.

Un "secrétaire" doit être nommé afin de prendre des notes tout au long
de l'audit. Ces notes serviront pour le résumé d'audit.

..  attention::

    Perdre des informations ou remarques faites pendant l'audit
    est une faute grave.

(C) Compte rendu
----------------

Après l'audit faire tout d'abord un débriefing entre les membres
de l'équipe.

Etablir ensuite un compte rendu faisant état des principales
remarques faites lors de l'audit, suivi des actions à entreprendre.
Le compte rendu d'audit doit se faire immédiatement après l'audit,
au moins pour la partie "remarques effectuées".

Le compte rendu doit être réalisé sous forme de texte dans le fichier
``projet/sprint<N>/audit/resume.md``. Il peut s'agir simplement
de quelques lignes. Utiliser un style télégraphique,
une liste de points. Il ne s'agit pas d'un document formel mais simplement
d'un memo principalement à destination de l'équipe. La forme n'est pas
primordiale mais le contenu est par contre particulièrement important
car c'est lui qui défini l'orientation du prochain sprint.

Si des décisions importantes ont été prises, les consigner dans le
fichier ``suivis/suivis.trs``.