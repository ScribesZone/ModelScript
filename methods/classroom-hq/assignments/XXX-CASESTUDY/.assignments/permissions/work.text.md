[XXX-CASESTUDY] Permissions
===========================================================

Cette tâche a pour but de modifier le modèle de permission
(fichier ``permissions/permissions.pes``)

Après avoir défini un modèle de classes et un modèle de cas d'utilisation 
il est possible de définir le modèle de permissions. Cette tâche a 
*in fine* pour objectif d'aligner :
* le modèle de permissions,
* le modèle de classes,
* le modèle de particpants,
* le modèle de cas d'utilisation,
* les modèles de scénarios.   

Il existe [plusieurs manières](https://modelscript.readthedocs.io/en/latest/scripts/permissions/index.html#methode) de remplir le modèle de permission. 
L'objectif de cette tâche est de mettre en pratique deux de ces 
techniques.


## Technique 1: classes en premier


Commencer par la méthode ["classes en premier"](https://modelscript.readthedocs.io/en/latest/scripts/permissions/index.html#classes-en-premier).
Lorsque des classes/attributs/associations ne sont créé/utilisés/modifiés
par aucun cas d'utilisation, indiquer pourquoi sous forme de commentaires
dans le modèle de permissions.  Ajuster le modèle de cas d'utilisation 
si nécessaire.

## Technique 2: cas d'utilisation en premier

Dans un deuxième temps utiliser la méthode ["Cas d'utilisation en premier"](https://modelscript.readthedocs.io/en/latest/scripts/permissions/index.html#cas-d-utilisation-en-premier) pour remplir 
la suite du modèle. Ajuster le modèle de classes  si nécessaire.

## Alignement avec les modèles de scénarios

Une fois le modèle de permission créé, vérifier que les accès réalisés
dans les scénarios ne violent pas les permissions données.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (010) Application de la technique "Classes en premier"
    - M ``permissions/permissions.pes``
- [ ] (010) Application de la technique "Cas d'utilisation en premier"
    - M ``permissions/permissions.pes``
- [ ] (050) Vérification de l'alignement permissions/scénarios.
- [ ] (900) Ecriture du status final.
    - M ``permissions/status.md``
