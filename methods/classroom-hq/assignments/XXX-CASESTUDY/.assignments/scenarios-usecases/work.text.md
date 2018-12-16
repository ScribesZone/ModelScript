[XXX-CASESTUDY] Scenarios ()cas d'utilisation)
===========================================================
























XXXXXXXXXXXXXXXXXXXXXXXLe modèle de cas d'utilisation à compléter se trouve dans le fichier
``usecases/usecases.uss``.

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXLe modèle de cas d'utilisation doit être écrit en UsecaseScript.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/classes1/index.html) lorsque nécessaire.

Les scénarios réalisés jusque là étaient caractérisés
par l'état qu'ils généraient à la fin de leur exécution. Il
s'agissait d'une liste "à plat" de création d'objets et de liens.

Dans cette tâche les scénarios sont considérés comme une **séquence**
d'instance de cas d'utilisation. Il s'agit en fait d'aligner chaque 
scénario avec le modèle de cas d'utilisation. Les étapes listées 
ci-dessous permettent cet alignement. Elles ne peuvent cependant pas 
être menées de manière puremment séquentielle.

### Définition des personnages

Les instances d'acteurs qui vont agir dans un scénarios sont doivent être 
déclarés dans le modèle de participants sous la forme suivante. Ce sont des 
personnages. 
```
    persona marie : Bibliothecaire
```

### Décomposition en instance de cas d'utilisation

Il s'agit de décomposer la liste existante d'instructions en blocs, 
chaque bloc correspondant à une instance de cas d'utilisation. 
Par exemple l'exemple ci-dessous signifie que ``marie`` intéragit avec
le système et que ces interactions modifient l'état du système. 
```
    -- @marie va RentrerUnLivre
         ! stmt1
         ! stmt2
    -- @end
``` 
Naturellement les cas d'utilisation doivent être définis dans le modèle
de cas d'utilisation.
Voir l'exemple dans la section ci-dessous pour un exemple plus complet.

### Extraction du contexte

Certaines instructions ne correspondent pas au flôt normal du scénario
mais au contraire à des objets et des associations qui font partie
du "contexte" dans lequel est exécuté le scénario. Par exemple 
l'instruction ``create r203 : Salle`` fait partie du contexte du cas 
d'utilisation ``ReserverUneSalle``car la salle r203 pré-existe et n'est pas
créée par le scénario. Ces instructions doivent être inclues dans un block 
``context``. 
```
    --@ context
         ! create s203 : Salle
         ...
    --@ end
``` 


### Exemple de transformation

L'exemple ci-dessous montre le résultat du processus :
* identification des instances de cas d'utilisation (``va``) 
* extraction des instructions du contexte (``context``)
```  
    =========================== ===================================
        AVANT: Scénario-état          APRES: Scénario-séquence 
    =========================== ===================================
                                --@ context
                                    ! stmt1
                                    ! stmt4 
                                    ! stmt5 
                                --@ end
    ! stmt1                     --@ marie va ReserverUneSalle
    ! stmt2                         ! stmt2 
    ! stmt3                         ! stmt3
    ! stmt4                     --@ end
    ! stmt5                     --@ toufik va RentrerUnLivre
    ! stmt6                         ! stmt6       
    ! stmt7                         ! stmt7
                                --@ end
    =========================== ===================================
```

### Alignement Scénarios / Cas d'utilisation

Vérifier (manuellement) que le modèle de scénarios est bien aligné 
avec le modèle de  cas d'utilisation (L'outil ``use`` ne prend pas 
en compte la notion de cas d'utilisation et aucune vérification ne
peut donc être faire avec cet outil). Il s'agit de vérifier 
(manuellement) que les personnage et de l'instances de 
cas d'utilisation ont bien leur contre partie. Vérifier également
que les (instances) d'interactions définies dans le scénario sont
compatibles avec celles définies dans le modèle de cas d'utilisation.
Par exemple ``marie va ReserverUneSalle`` implique qu'une
bibliothéquaire secrétaire peut réserver une salle.

### Alignement Scénarios / Modèle de classes

Vérifier que le scénario est encore aligné avec le modèle de classes.
```
    use -qv Classes/classes.cls Scenarios/n/scenario.scn
```
Cette vérification a été faite précédemment avec le scénario-état
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

- [ ] (010) Définition des personnages nécessaires au scénario.
    - M ``Participants/participants.scs``
- [ ] (020) Définition des instances de cas d'utilisation.
    - M ``Scenarios/n/scenario.scs``    
- [ ] (030) Extraction du contexte.
    - M ``Scenarios/n/scenario.scs``    
- [ ] (100) Vérification de l'alignement Scenario/Participants.
- [ ] (200) Vérification de l'alignement Scenario/Cas d'utilisation.
- [ ] (300) Vérification de l'alignement Scenario/Classes.
- [ ] (900) Ecriture du status final.
    - M ``scenarios/status.md``

    
