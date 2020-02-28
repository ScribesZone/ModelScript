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
l'octroi des ressources nécessaires à un nouvel incrément.

L'objectif de l'audit lui-même est d'intéragir avec le comité d'audit,
de l'informer, mais aussi de recueillir les recommendations émises
afin d'établir un rapport d'audit suivi d'actions précises.

..  note::

    En Scrum le "sprint review" et la cérémonie correspondant
    le plus aux audits, bien que l'esprit ne soit pas exactement
    le même.

(A) Transparents
----------------

Chaque audit est basé sur une présentation effectuée à base
de transparents. La dernière version doit être convertie en fichier
.pdf dans ``projet/sprint<N>/audit/audit.pdf``

(B) Contenu
-----------

La présentation doit être basée sur :

*   les différentes captures d'écran réalisées au cours du sprint
    (plannings, diagrammes de classes, tableau GitHub etc.),
*   les différents fichiers produits pendant le sprint,
*   les différentes tâches ModelScript réalisées.

Il doit être possible, pour chaque transparent, de savoir à quel
artefact et/ou quelle tâche, le transparent fait référence. Voir
la section "Traçabilité" ci-dessous.

Si une rétrospective récente à eu lieu faire part des résultats de
cette rétrospective dans la présentation.

(C) Suivis
----------

Les éléments du modèle de suivis doivent être utilisés dans la présentation
pour montrer quelles décisions, hypothèses ont été faites, quelles
questions sont à l'ordre du jour et quels empéchements ont freiné le
projet. Faire référence à chaque suivi par son identifiant (par
exemple ``Q3``) et par son titre.

(D) Glossaire
-------------

Les transparents doivent impérativement faire référence aux termes du
glossaire. Autant que faire se peut utiliser les backquotes "`" pour
faire référence à ces termes.

(E) Traçabilité
---------------

Chaque transparent, chaque élément de présentation doit faire référence,
autant que faire se peut, aux entités définies dans les modèles ou plus
généralement dans le projet. Faire référence aux scénarios (p.e. ``S1``),
aux incréments (p.e. ``I3``), aux questions (p.e. ``Q2``),
aux tâches (p.e. ``concepts.glossaires``), etc. Faire référence aux
artefacts par leur nom court (p.e. ``classes.cl1``).

..  attention::

    La possibilité d'identifier de manière précise "de quoi on parle"
    est un critère important d'évaluation de l'audit.

(F) Présentation
----------------

Lors de la présentation effective, c'est la dernière version des
transparents sur GitHub qui doit être présenté.

Chaque membre du groupe doit parler.

Un ou deux "secrétaires" doivent être nommés afin de prendre des notes
tout au long de l'audit. Le deuxième secrétaire n'est là que pour
se substituer au premier lorsque celui-ci intervient.

Ces notes prises pendant l'audit serviront de résumé d'audit.

..  attention::

    Perdre des informations ou remarques faites pendant l'audit
    est une faute grave. Aucun client n'apprécie d'avoir à redire
    une fois de plus ce qui a été déjà dit lors d'une précédente
    réunion. Cela démontre un manque de professionalisme.

(D) Compte rendu
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

..  attention::

    Si des décisions importantes ont été prises, les consigner dans le
    fichier ``suivis/suivis.trs``.