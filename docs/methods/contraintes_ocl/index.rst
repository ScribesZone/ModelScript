tache:contraintes_ocl
=====================

:résumé: L'objectif de cette tâche est de traduire les contraines
    exprimées en langage naturel en contraintes OCL.

:langage:  :ref:`ClassScript1`
:résultat:
    * ``classes/classes.cl1``


(A) Ecriture des contraintes
----------------------------

L'expression des contraintes en langage naturel est indispensable pour
garantir l'alignement avec les contraintes métier (business rules).
Sans cela le logiicel ne correspondera pas au besoin du client. Dans
cette tâche il s'agit de formaliser ces contraintes en langage OCL,
le langage standardisé d'UML pour les contraintes. Voir la
`feuille de résumé OCL`_  pour des précisions sur le langage.
Vérifier que la traduction en OCL est fidèle à la contrainte en
langage naturel.

(B) Tests positifs
------------------

Vérifier que l'ensemble des modèles d'objets positifs ne
génère aucune erreur. Utiliser la commande ``use -qv`` pour cela.
Si des erreurs sont produites cela veut dire que les contraintes
sont trop restrictives.

(C) Tests négatifs
------------------

Vérifier que les tests négatifs concernant telle ou telle contrainte
génèrent bien une erreur. Si toutes les erreurs attendues ne sont pas
générées alors c'est que les contraintes écrites ne sont pas assez
restrictives. Revoir les contraintes.

(Z) Suivi et status
-------------------

**Suivi**: Si des questions ou des hypothèses surgissent lors de ce travail
appliquer les :ref:`règles relatives au suivi <Tracks_Rules>`.

**Status**: Avant de terminer cette tâche écrire le status en appliquant
les :ref:`règles relatives au status <Status>`.


..  _`feuille de résumé OCL`:
    https://scribestools.readthedocs.io/en/latest/_downloads/UMLOCL-CheatSheet-18.pdf
