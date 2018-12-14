# [CASESTUDY] Permissions

Après avoir défini un modèle de classes et un modèle de cas d'utilisation 
il est possible de définir le modèle de permissions. Ce modèle
doit en outre être aligné avec les accès réalisés par les différents
scénarios. Cette tâche a *in fine* pour objectif d'aligner :
* le modèle de permissions,
* le modèle de classes,
* le modèle de particpants,
* le modèle de cas d'utilisation,
* les modèles de scénarios.   

## Méthodologie

Les tâches listées par la suite ne peuvent que difficilement être réalisées 
en séquentiel. Cependant plusieurs pratiques existent, selon que l'on 
part d'un modèle ou d'un autre :
*   **modèle de classes en premier**. Il s'agit de partir d'un modèle de
    classes, de lister les différentes ressources et de répondre à la 
    question *"qui change telle ou telle ressource ?"*.
*   **modèle de cas participants en premier**. Il s'agit de répondre à
    la question *"que peut faire tel ou tel acteur ?"**   
*   **modèle de cas d'utilisation en premier**. Il s'agit de répondre à
    la question *"que peut faire tel ou tel cas d'utilisation ?"*
*   **matrice de permissions**. Il est également classique de combiner
    les deux méthodes ci-dessus en produisant d'abord une matrice
    listant d'un coté toutes les resources (classes, etc.) et de l'autre
    tous les sujets (acteurs, etc.). Il s'agit ensuite de répondre
    pour chaque élément de la matrice à la question *"quelles actions
    peut être réalisées par ce sujet sur cette ressource"*
    
Quelque soit la méthode retenue, ou certainement combinaison de méthodes,
l'objectif est de construire un modèle de permissions aligné avec
le modèle de classes et avec le modèle cas d'utilisation.

## Modèle de permissions

Le modèle de permission utilisé ici est très simple. Il est basé sur une 
suite de tripets:
*   "subjects"
*   "actions"
*   "ressources"

Un tel triplet peut par exemple prendre la forme ci-dessous :
```
Manager,BookRoom can RU Room.booked
```
Les actions sont les suivantes:
*   **C**reate
*   **R**ead
*   **U**pdate
*   **D**elete
*   **E**xecute

Les sujets et les ressources sont définis ci-dessous. 

## Alignement avec le modèle de participants / de cas d'utilisation
Il s'agit de définir pour chaque sujet quelles actions peuvent
être réalisées sur quelles ressources. Un *"sujet"* est soit:
* (1) un acteur (provenant du modèle de participants)'
* (2) un cas d'utilisation (provenant du modèle de cas d'utilisation)

Si un "acteur" peut réaliser une action sur une ressource alors
toutes les cas d'utilisation de cet acteur peuvent réaliser cette action. 

## Alignement avec le modèles de classes

Les ressources sont définies dans le modèle de classes. Une "resource" est
soit :
* (1) une classe, 
* (2) une association, 
* (3) un attribut, 
* (4) une opération.

Les ressources définissent les actions autorisées :
* "**C**reate" s'applique à une classe ou à une association
* "**R**ead" s'applique à un attribut ou à un role. 
    *   Lorsque cette action est donnée à une classe n'importe 
        quel attribut peut être attribut de la classe peut être lu. 
    *   Lorsque cette action est associée à une association, 
        celle-ci peut être traversée dans n'importe quel sens.

* "**U**pdate" s'applique à un attribut
* "**D***elete" s'applique à une classe ou à association
* "**E**xecute" s'applique à une operation 

## Alignement avec les modèles de scénarios

Une fois le modèle de permission créé, vérifier que 
les accès réalisés dans les scénarios ne violent pas les permissions
données.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).

________

- [ ] (010) Définition d'une premiere version du modèle de permissions
    - M ``permissions/permissions.pes``
- [ ] (020) Vérification de l'alignement permissions/classes
- [ ] (030) Vérification de l'alignement permissions/participants
- [ ] (040) Vérification de l'alignement permissions/cas d'utilisation
- [ ] (050) Vérification de l'alignement permissions/scénarios.
- [ ] (900) Ecriture du status final.
    - M ``permissions/status.md``
