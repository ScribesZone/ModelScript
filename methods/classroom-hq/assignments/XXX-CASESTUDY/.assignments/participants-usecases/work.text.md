[XXX-CASESTUDY] Participants_CasDUtilisation
===========================================================

Le modèle de participants à compléter se trouve dans le fichier
``participants/participants.pas``.

Le modèle de participants doit être écrit en ParticipantScript.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/participants/index.html) lorsque nécessaire.

### Définition des acteurs

Définir tout d'abord les "acteurs" qui interviendont par la suite 
dans le modèle  de cas d'utilisation. Donner pour chaque acteur un
nom (``ResponsableDesAchats``) ainsi qu'une courte définition faisant
référence aux éléments du glossaire.

### Définition des personnages

Les "personnsages" sont des instances particulières d'acteurs. Ceux-ci 
interviennent dans les modèles de scénarios. Repérer "qui", dans chaque
scénario, existant ou à définir, joue le rôle d'un acteur Définir chaque
personnage en donnant a minima son nom et son type. Par exemple
``mario : ResponsableDesAchats``. 

### Alignement

Les participants et les personnages pourront être définis "à la demande"
lors des tâche "Usescases" et "Scenarios Sequences". Par la suite  il 
s'agira  aussi d'aligner les participants au modèle le modèle de 
permissions.

Infine le modèle de particiants doit être affiné/aligné avec les modèles
suivants: 
** le modèle de cas d'utilisation
** les différents modèles de scénarios. 
** le modèle de pemission.


### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).
________

- [ ] (030) Ajout/modification d'acteurs pour les cas d'utilisation.
    - M ``participants/participants.pas``
- [ ] (050) Ajout de personnages pour les scénarios.
    - M ``participants/participants.pas``
- [ ] (100) Alignement entre participants et cas d'utilisation
- [ ] (200) Alignement entre participants et scénarios séquences
- [ ] (900) Ecriture du status final.
    - M ``participants/status.md``

    
