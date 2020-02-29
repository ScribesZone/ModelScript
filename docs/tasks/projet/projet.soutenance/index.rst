..  _`tâche projet.soutenance`:

tâche projet.soutenance
=======================

:résumé: Cette tâche vise a définir les tâches liées à la préparation
    de la soutenance ainsi qu'à la soutenance elle même.


Introduction
------------

Contrairement aux audits qui peuvent être considérés comme des réunions
de travail avec le comité d'audit, la soutenance vise à présenter à
l'auditoire (qui peut être plus large) les mérites du travail réalisé,
mérites en termes de :

*   développement,
*   conception,
*   méthodologie.

Il ne s'agit pas de montrer que l'équipe de développement est arrivée à
réaliser une "démo" qui semble marcher, mais plutôt que le produit est
de qualité, qu'un processus clair et solide a été suivi et que le
logiciel a été conçu dans les règles de l'art.

**Il s'agit de donner de la confiance** ; de donner à l'auditoire
confiance dans ce qui a été réalisé, avec l'eventuelle envie de continuer
de travailler ensemble sur des extensions du projet, voire sur de nouveaux
projets.

..  note::

    La cérémonie Scrum qui s'approche le plus de la soutenance et le
    "Sprint Review".

(A) Fichiers
------------

La dernière étape du dernier sprint correspondant à une soutenance
plutôt qu'à un audit. Les noms de fichiers doivent éventuellement
être ajustés comme ci-dessous.

Le répertoire à utiliser est le répertoire ``projet/sprint<N>/soutenance``
où ``<N>`` est le numéro du dernier sprint. Si ce répertoire n'existe pas
renommer le répertoire ``audit`` en ``soutenance``.
Faire de même pour les fichiers se trouvant dans le répertoire.

Le fichier ``resume.md`` peut être éliminé car la soutenance ne
donne pas lieu à compte rendu.

(B) Transparents
----------------

La version finale des transparents, en pdf, doit se trouver dans
``projet/sprint<N>/soutenance/soutenance.pdf``. La version présentée
lors de la soutenance doit impérativement correspondre à la version
présente sur GitHub.

(C) Contenu
-----------

Comme pour les audits, les transparents de la soutenance doivent faire
explicitement référence aux différents artefacts créés (plannings,
diagrammes de classes, modèles de tâches, etc.). Les résultats
obtenus doivent être clairement mis en avant et il est indispensable de
faire référence explicitement aux scénarios, aux incréments, etc.

(D) Traçabilité
---------------

La traçabilité dans la conception et le développement est un des
critères important de l'évaluation. Voir la section
:ref:`Traçabilité<projet.audit.tracabilite>` de la
:ref:`tâche projet.audit` pour plus de détails.

..  _`projet.soutenance.demonstration`:

(E) Démonstration
-----------------

Une démonstration du produit devra être faite. Cette démonstration doit
**impérativement être préparée, pas à pas**. La démonstration peut être
intégrée dans la présentation où faite dans une partie spécifique.

Il peut être utile de fournir à l'auditoire un "script" de la
démonstration permettant de montrer ce qui est démontré, étape par étape,
en termes d'objectifs, de résultats attendus, d'interactions, etc.

Le contenu de la démonstration doit également être enoncé à l'oral
avant le déroulement des actions.

Le contenu global de la démonstration devra être établi plusieurs jours
avant la soutenance, de manière à définir le script, les données utilisées
dans la démonstration, les personnes impliquées, etc.

La démonstration peut éventuellement être faite en deux sessions :

*   une première session, avec un scénario figé et bien délimité
    correspondant à un déroulement normal d'un utilisateur. Cette
    session montrera un scénario "métier" sans trop rentrer dans les
    détails techniques. Elle doit raconter une histoire bien identifiée.

*   une deuxième session plus "ouverte", plus "technique", plus
    "exploratoire", c'est à dire en suivant des chemins qui ne seraient
    normallement pas suivis par un utilisateur standard. Ce peut être par
    exemple pour montrer des scénarios d'erreurs ou des détails techniques
    jugés important.

Répeter impérativement la démonstration, en faisant attention notamment
à ne pas aller trop vite, en s'assurant que le niveau de la voix du
présentateur soit audible, etc. A tout moment, l'auditoire doit être
en mesure de comprendre "ce qui se passe et pourquoi cela se passe ainsi".
Lors d'une répétition il peut être utile qu'une personne extérieure ou
qu'un autre membre du groupe assiste à la démonstration et fasse part
de ses commentaires.

Les jeux de données utilisés dans la démonstration devront correspondre
aux jeux de données élaborés en début de cycle de vie. Ces jeux de données
peuvent par exemple provenir des modèles d'objets (``concepts/objets/``)
ou modèle de scénarios (``cu/scenarios/``).

Dans un cycle de vie en V, l'exécution de scénarios prédéterminés
et définis en début de projet peut constituer un "test de recette",
c'est à dire un test qui détermine l'acceptation ou non de la
livraison du projet. Montrer en quoi le ou les scénarios exécutés
divergent ou non des scénarios prévus initialement.

Pendant la démonstration, attention à utiliser au maximum les termes
métiers définis dans le glossaire. Le narrateur peut jouer le rôle
d'un utilisateur en disant par exemple *"Je suis Paul, un bibliothécaire
et je veux ... Maintenant j'ai besoin de ... et je fais ... "*, etc.

Si certains détails ne peuvent pas être montrés pendant la démo
n'hésitez pas à dire *"pour ceux intéressés par ce point là, nous
pourrons y revenir pendant la scéance de questions"*. Cela permet
entre autre de diriger les questions vers des éléments qui seront
déjà préparés.

Faire quelques copies d'écrans et les intégrer en fin de présentation
pour palier d'éventuelles difficultés à dérouler la demonstration.

(F) Documents
-------------

Comme pour les audits il peut être utile de distribuer des documents aux
membres du jury. C'est le cas notamment d'informations relatives aux
scénario(s) suivi(s) dans la démonstration. Tous les documents
permettant de mieux suivre la démonstration ou la soutenance seront
les bienvenus.

(G) Soutenance
--------------

Déterminer avant la soutenance sur quel machine la présentation et la
démonstration vont être faites. Vérifier **avant** la soutenance
que les problèmes de connections sont résolus. Prévoir éventuellement
une machine de repli.

Tous les membre du groupe doivent parler.

Chaque membre du groupe doit parler et répondre aux questions qui le
concerne.