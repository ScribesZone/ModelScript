# [XXX-CASESTUDY] Objets

Les modèles d'objets à compléter se trouvent dans les fichiers
``objects/O<N>/O<N>.ob1`` (où <N> est un entier).

Les modèles d'objets doivent être écrits en ObjectScript1.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/objects1/index.html) lorsque nécessaire.

Cette tâche consiste à traduire les états décrits sous forme 
textuelle en un modèle d'objet. Chaque modèle d'objet se concrétise
en un fichier ``.ob1`` executable. Ces fichiers vont être 
utilisés pour valider le modèle de classes (fichier ``.cl1``).
Il s'agit de répéter les étapes ci-dessous pour chaque modèle d'objets
dans le répertoire ``objects``.

### Traduire des états en langage ObjectScript

Le fichier ``objects/O<N>/O<N>.ob1`` (où <N> est un entier) 
contient un  modèle d'objets décrit en langue naturelle.
Dans un étape précédante, ce texte a du être rephrasé pour l'aligner avec
le glossaire. Il s'agit maintenant de le remanier pour établir
une texte correspondant à un modèle d'objet. Il s'agit de plus de traduire
chaque ligne en utilisant le langage 
[ObjectScript1](https://modelscript.readthedocs.io/en/latest/scripts/objects1/index.html) lorsque nécessaire.

En pratique il s'agit dans cette tâche d'écrire les instructions 
préfixée par ``!`` sous les phrases correspondantes.

Supprimer du texte les éléments non pertinents, c'est à dire n'ayant
pas de lien direct avec l'état du système modélisé.

Lorsqu'une valeur n'est pas définie utiliser une instruction
``... := Undefined``. Dans certains cas il peut être pertinent "d'inventer"
une valeur. Dans ce cas mettre une note dans le modèle de suivi.
Faire au mieux sachant que l'objectif est de traduire un texte fourni
par (ou écrit en collaboration avec) le client. Il est peut être nécessaire
de voir avec lui compléter et éta.

### Vérifier l'alignement avec le modèle de classes 

Vérifier que l'état est aligné avec le modèle de classes.
Pour cela utiliser la commande suivante à partir du répertoire principal :
```
    use -qv classes/classes.cl1 objects/o<N>/objects.ob1
```
L'interpreteur affichera les éventuelles erreurs de syntaxe
ainsi que les erreurs de types ou de cardinalités. Si rien ne s'affiche
cela signifie qu'aucune erreur a été trouvée.

## Dessiner un diagramme d'objets

Produire un diagramme d'objets représentant l'état ``objects/o<N>``.
Pour cela utiliser la même technique que pour les diagrammes de classes.
La disposition des objets doit autant que possible refléter
la disposition du diagramme de classes. 

Observer la présence ou non d'objet isolés. Vérifier s'il s'agit d'un
problème dans le scénario lui même ou dans la traduction qui en a été
faite.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).
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

    

    
