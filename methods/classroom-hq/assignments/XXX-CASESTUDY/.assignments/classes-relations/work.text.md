[XXX-CASESTUDY] Classes_Relations
===========================================================

### Artefacts

Le modèle de classes à compléter se trouve dans le fichier
``classes/classes.cl1``.

### Résumé

Le modèle de classes élaboré jusqu'à présent était un modèle
conceptuel, c'est à dire décrivant des concepts du domaine de
manière abstraite ; et ce indépendamment de toute considération
technique. 

Il s'agit maintenant de transformer ce modèle abstrait en un modèle
de de classe pour base de données ; plus particulièrement de
préparer le modèle classes avant de la transformation en modèle
de relations.

### Définition des identifiants de chaque classe

Pour chaque classe, il s'agit de définir quel(s) attribut(s)
peuvent appatenir à une clé. Chacun de ces attributs doit être
entouré par des caractères soulignés ('_'). Par exemple l'attribut
``login`` devient ``_login_`` s'il s'agit d'un identifiant. Dans
certains cas une "clé" peut être composée, dans d'autres cas plusieurs
"clés" peuvent exister. Quoi qu'il en soit, la convention
"attributs soulignés" sera raffinée et précisée lors de la
transformation en modèle de relations.

### Composition et identification composite

Dans certains cas les objets d'une classe doivent être identifiés
non pas de manière directe, avec son/ses identifiants, mais par
rapport aux objets composites les contenant. 

Par exemple une salle peut être identifiée en partie par son numéro, 
par exemple 13, mais aussi le numéro de l'étage à laquelle elle se trouve, 
par exemple 6. Dans cet exmple l'identifiant de la salle est le couple 
( 6 , 13 ).
 
Dans le cas du modèle de base de données, l' "importation" de 
l'identifiant du composite se fait dans le cadre d'association de 
composition. Il est alors nécessaire, parfois, de changer une 
association "normalle" en une composition.

Par exemple : ::

    association ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances            
    end
            
peut être changé en : ::

    composition ComporteSeance
        between
            Salle[1] role salle
            Seance[*] role seances
    end
              
Même si cette composition pourrait sembler contestable dans le cas d'un 
modèle conceptuel, cette modification peut valide dans un modèle technique,
ici dans le cadre de la conception de bases de données.                
            
### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (010) Définition des identifiants pour chaque classes.
    - M ``classes/classes.cl1``
- [ ] (020) Compilation sans erreur (``use -c``)
- [ ] (900) Ecriture du status final.
    - M ``classes/status.md``
