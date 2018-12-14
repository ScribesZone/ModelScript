# [CASESTUDY] Classes

Le modèle de classes à compléter se trouve dans le fichier
``classes/classes.cl1``.

Le modèle de classes doit être écrit en ClassScript1.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/classes1/index.html) lorsque nécessaire.

### Définition du modèle de classes

Compléter le modèle de classes en fonction :

* des besoins exprimés par le client (dossier ``requirements/``)
* des modèles d'objets (dossier ``objects/``)
* des scénarios (dossier ``scenarios/``)
* de vos connaissances du domaine,

### Compilation du modèle de classes

Le modèle de classes doit **IMPERATIVEMENT** pouvoir
être "compilé" sans erreur en utilisant la commande suivante
(à partir du répertoire racine du dépot):

       use -c classes/classes.cl1

S'il y a des erreurs elles seront affichées. Aucun affichage
signifie que le modèle est conforme à UML.

### Création d'un diagramme de classes global

Créer ensuite un [diagramme de classes avec l'outil USE OCL](http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams).
Sauvegarder impérativement le diagramme dans le fichier
``classes/diagrams/classes.cld.clt`` (remplacer le fichier
existant). Le diagramme dessiné doit respecter la disposition
spatiale de l'ébauche fournie. Faire une copie d'écran du diagramme
et remplacer le fichier 
``classes/diagrams/classes.cld.png`` fourni.
Respecter **impérativement** les noms de fichiers, entre autre l'extension
``.png``.

### Alignement avec les objets et les scénarios

Dans la suite, il sera demandé de valider le modèle de classes proposé
avec les états et les scénarios. Voir les tâches/issues correspondantes.
Répéter ces operations jusqu'à ce que le modèle soit satisfaisant.

### Alignement avec le glossaire

Vérifier que les termes importants apparaissant dans les noms de classes,
d'associations, d'attributs ou de rôle sont bien dans le glossaire. Par 
le il peut être important de définir ce qu'est la "DateDeRetour" dans le
contexte d'un bibliothèque. Ce terme fait partie du domaine. Il est sans 
doute nécessaire de l'expliquer s'il ne correspond pas à une définition
de sens commun. D'ailleurs le terme à définir est peut être "Retour". 
Lire et appliquer les [règles associées à la réécriture d'identificateurs](https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rewriting-identifiers).

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).

________

- [ ] (010) Définition du modèle de classes
    - M ``classes/classes.cl1``
- [ ] (020) Compilation sans erreur (``use -c``)
- [ ] (030) Création d'un diagramme de classes global.
    - M ``classes/diagrams/classes.cld.clt``
    - M ``classes/diagrams/classes.cld.png``
- [ ] (100) Ecriture du bilan.
