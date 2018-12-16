[XXX-CASESTUDY] Objets
===========================================================

Les modèles d'objets à compléter se trouvent dans les fichiers
``objects/O<N>/O<N>.ob1`` (où <N> est un entier).

Les modèles d'objets doivent être écrits en ObjectScript1.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/objects1/index.html) lorsque nécessaire.

Cette tâche consiste à traduire les états décrits sous forme 
textuelle en un modèle d'objets annoté. Chaque modèle d'objets se 
concrétise en un fichier ``.ob1`` exécutable. Ces fichiers vont être 
utilisés pour valider le modèle de classes (fichier ``.cl1``).
Il s'agit de répéter les étapes ci-dessous pour chaque modèle d'objets
dans le répertoire ``objects/``.

### Traduire des états en langage ObjectScript

Le fichier ``objects/O<N>/O<N>.ob1`` (où <N> est un entier) 
contient un  modèle d'objets décrit en langue naturelle.
Il s'agit de plus de traduire chaque ligne en utilisant le langage 
[ObjectScript1](https://modelscript.readthedocs.io/en/latest/scripts/objects1/index.html) lorsque nécessaire.

Lorsqu'une valeur n'est pas définie utiliser une instruction
``... := Undefined``. Dans certains cas il peut être pertinent "d'inventer"
une valeur ou des valeurs. Dans ce cas mettre une note dans le modèle de suivi.
Certaines valeurs ne sont pas fondamentale (par exemple la valeur de
certains attributs) alors que d'autres sont plus importantes car le
scénario en dépend de manière plus ou moins directe.

Faire au mieux sachant que l'objectif est de traduire un texte fourni
par (ou écrit en collaboration avec) le client. sera est peut être nécessaire
de voir avec lui comment compléter/valider la description d'un modèle d'objets
sachant qu'un tel modèle pourra par la suite être utilisés pour établir
des tests et en particulier des tests de recette.

### Vérifier l'alignement avec le modèle de classes 

Vérifier que l'état est aligné avec le modèle de classes.
Pour cela utiliser la commande suivante à partir du répertoire principal :
```
    use -qv classes/classes.cl1 objects/o<N>/objects.ob1
```
L'interpreteur affichera les éventuelles erreurs de syntaxe
ainsi que les erreurs de types ou de cardinalités. Si rien ne s'affiche
cela signifie qu'aucune erreur n'a été trouvée.

## Dessiner un diagramme d'objets

Produire un diagramme d'objets représentant le modèle d'objets ``objects/o<N>``.
Pour cela utiliser la même technique que pour les diagrammes de classes.
La disposition des objets doit autant que possible refléter
la disposition du diagramme de classes. 

Observer la présence ou non d'objets isolés. Vérifier s'il s'agit d'un
problème dans le scénario lui même ou un problème dans la traduction qui en
a été faite.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).
________

Pour chaque modèle d'objet O<N> (où N est un entier):
- [ ] (010) Traduction de l'état en langage soil.
    - M ``objects/O<N>/O<N>.obs``
- [ ] (020) Vérification de l'alignement avec le modèle de classes.
- [ ] (030) Production du diagramme d'objets.
    - M ``objects/O<N>/diagrams/O<N>.obd.olt``
    - M ``objects/O<N>/diagrams/O<N>.obd.png``
- [ ] (900) Ecriture du status final.
    - M ``objects/status.md``
