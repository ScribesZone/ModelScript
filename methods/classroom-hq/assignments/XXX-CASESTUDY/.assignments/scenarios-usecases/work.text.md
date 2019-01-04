[XXX-CASESTUDY] Scenarios (cas d'utilisation)
===========================================================

Les scénarios réalisés jusque là étaient caractérisés
par le modèle d'objet qu'ils généraient à la fin de leur exécution. Il
s'agissait d'une liste "à plat" de création d'objets et de liens.
Dans cette tâche les scénarios sont considérés comme un emboîtement
d'instances de cas d'utilisation. 

Les modèles de scénarios à raffiner/compléter se trouvent dans les fichiers
``scenarios/S<N>/S<N>.ob1`` (où ``<N>`` est un entier). Se reporter à la 
documentation de 
[ScenarioScript1](https://modelscript.readthedocs.io/en/latest/scripts/scenarios1/index.html) lorsque nécessaire.


### Définition des personnages

Dans un premier temps il s'agit de repérer dans les scénarios quels
"personnages" interagissent **directement** avec le système. Ces
personnages sont, par définition, des instances d'acteurs (à ajouter
si nécessaire).

A chaque fois qu'un personnage est identifié celui-ci doit être ajouté au
modèle de participants (fichier ``participants/participants.pas``). 

Dans l'exemple ci-dessous on suppose que le personnage ``marie`` joue le
rôle de ``Bibliothecaire`` dans le scénario:

```
    persona marie : Bibliothecaire
```

Dans un premier temps il n'est pas nécessaire de détailler les
caractéristiques des personnages (voir la documentation 
[ParticipantScript](https://modelscript.readthedocs.io/en/latest/scripts/participants/index.html)
pour avoir des exemples relatifs à ces caractéristiques).

### Décomposition en instance de cas d'utilisation

Chaque scénario "à plat" doit ensuite être décomposé sous forme de
(d'instance de) cas d'utilisation.
Par exemple l'exemple ci-dessous signifie que le personnage ``marie`` 
intéragit avec le système via (l'instance) de cas d'utilisation 
``RentrerUnLivre``. Ces interactions modifient l'état du système via les 
instructions ``stmt1`` et ``stmt2``. 

```
    --@ marie va RentrerUnLivre
        ! stmt1
        ! stmt2
    --@ end
``` 

Naturellement les cas d'utilisation (``RentrerUnLivre`` ici) doivent être 
définis dans le modèle de cas d'utilisation. 


### Extraction du contexte

Dans cette tâche il s'agit d'isoler les instructions qui font
partie du "contexte" plutôt que du flôt normal du scénario. Par exemple 
l'instruction ``create s203 : Salle`` ne fait pas partie du cas 
d'utilisation ``ReserverUneSalle``car la salle ``s203`` pré-existe : la
salle n'est pas créée par la réservation ! Les instructions 
correspondant au contexte
doivent être inclues dans un block (ou plusieurs) block(s) ``context``. 

```
    --@ context
        ! create s203 : Salle
         ...
    --@ end
    
    ...
    
    --@ toufik va ReserverUneSalle
        ! s203.reservee := true
    --@ end
    
``` 

Déplacer ces blocks en début de scénario et vérifier que cela ne 
provoque aucune erreur dans la "compilation" du scénario.

### Exemple de transformation

L'exemple ci-dessous résume le processus global :
* (1) définition des personnages (``persona x : A``),
* (2) identification des instances de cas d'utilisation (``x va U``), 
* (3) extraction des instructions du contexte (``context``).
```  
    =========================== =========================================
      AVANT: Scénario (plat)        APRES: Scénario (cas d'utilisation) 
    =========================== =========================================
                                --@ context
    ! stmt1                         ! stmt1
    ! stmt2                         ! stmt4 
    ! stmt3                         ! stmt5 
    ! stmt4                     --@ end
    ! stmt5                     --@ toufik va ReserverUneSalle
    ! stmt6                         ! stmt2 
    ! stmt7                         ! stmt3
                                --@ end
                                --@ marie va RentrerUnLivre
                                    ! stmt6       
                                    ! stmt7
                                --@ end
    =========================== =========================================
```

### Alignement Scénarios / Cas d'utilisation

Vérifier (manuellement) que le modèle de scénarios est bien aligné 
avec le modèle de  cas d'utilisation .
Par exemple ``toufik va ReserverUneSalle`` implique qu'un
ChefBibliothequaire peut réserver une salle.

### Alignement Scénarios / Modèle de classes

Vérifier que le scénario est encore aligné avec le modèle de classes.
```
    use -qv Classes/classes.cls Scenarios/n/scenario.scn
```
Cette vérification a été faite précédemment avec le scénario plat
mais il s'agit là de vérifier que la transformation ci-dessus n'a pas
généré de problèmes supplémentaires. Ce peut être le cas si le
réordonnancement des instructions n'est pas correct.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________
Pour chaque scénario S<N> (où ``<N>``<N> est un entier) :

- [ ] (010) Définition des personnages nécessaires au scénario.
    - M ``participants/participants.pas``
- [ ] (020) Définition des instances de cas d'utilisation ("x va y").
    - M ``scenarios/n/scenario.scs``    
- [ ] (030) Extraction du contexte ("context").
    - M ``scenarios/n/scenario.scs``    
- [ ] (100) Vérification de l'alignement Scenario/Participants.
- [ ] (200) Vérification de l'alignement Scenario/Cas d'utilisation.
- [ ] (300) Vérification de l'alignement Scenario/Classes.
- [ ] (900) Ecriture du status final.
    - M ``scenarios/status.md``

    
