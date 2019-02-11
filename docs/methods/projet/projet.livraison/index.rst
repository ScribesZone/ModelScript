tâche projet.livraison
======================

:résumé: L'objectif de cette tâche est de livrer le logiciel.

:résultat:
    * ``github:release``
    * ``CHANGES.txt``

Introduction
------------

La livraison est une opération formelle (qui peut contractuelle) dans
laquelle l'équipe de développement délivre l'état le plus avancé
du logiciel au client. Le logiciel passe typiquement d'un environement
de développemment à un environnement de test, de pre-production ou
autre.

(A) Tests
---------

Avant de livrer un logiciel il est bien sûr nécessaire de s'assurer que
le version la plus stable et la plus à jour est mise à disposition du
client. Toute livraison doit être précédée par des tests poussés.

(B) Notes de livraison
----------------------

Les "notes de livraison" (releases notes) sont d'une importance capitale
dans le processus de livraison. Les notes de livraison constituent la
première source d'information pour un client pour déterminer si les
modifications/évolutions demandées ont été implémentées, si les bugs
ont été corrigés, etc. La satisfaction du client dépend du contenu de
ses notes. Il va sans dire que les notes de livraisons doivent être
fidèles au contenu de la livraison.

Les notes de livraisons doivent donc être rédigées avec le plus grand
soin. Il peut être utile de consulter les messages de "log" de git pour
être sûr de ce qui a été modifié. Utiliser la commande ``git log``.

Concrètement les notes de livraison seront associées à la livraison
(rélease GitHub). Voir ci-dessous.  Le projet `bootstrap`_  fourni
des exemples de notes de livraison.

(C) Livraison
-------------

Dans GitHub la livraison du logiciel se fait via le bouton
``Releases`` (suivi du nombre de releases) sur la page principale du
dépot du groupe. Utiliser ensuite ``Create a new release``.
A la fin du sprint 2, utiliser "v2.0" comme "tag". Attacher les
notes précedemment élaborées. Dans un premier temps indiquer qu'il
s'agit d'une pré-release.

Si pour une raison ou pour une autre un release mineures devaient
être produite avant la date de livraison, utiliser un numéro
de verion tel que "v2.1".

Immédiatement avant la livraison décocher la case ``this is a pré release``
de la derniere release



..  _bootstrap:
    https://github.com/twbs/bootstrap/releases



