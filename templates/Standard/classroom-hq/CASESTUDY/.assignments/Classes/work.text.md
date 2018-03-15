[CASESTUDY][WorkDefinition] Classes
==================================================================

Définir le modèle de classes (``Classes/classes.cld``) en fonction :

* de la [syntaxe USE OCL](http://scribetools.readthedocs.io/en/latest/useocl/index.html#syntax)
* des besoins exprimés par le client (dossier ``Requirements/``)
* de vos connaissances du domaine
* de l'ébauche fournie (``Classes/Diagrams/draft.cld.pdf``)
* des états (dossier ``States/``)
* des scénarios (dossier ``Scenarios/``)

Le modèle de classes doit **IMPERATIVEMENT** pouvoir
être "compilé" sans erreur en utilisant la commande suivante. :
```    
   use -c Classes/classes.cls
```
S'il y a des erreurs elles seront affichées. Aucun affichage
signifie que le modèle est conforme à UML.

Le modèle de classes doit également être aligné avec les
scenarios et les états (voir les tâches correspondantes).

Créer ensuite un [diagramme de classes avec l'outil USE OCL](http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams).
Sauvegarder impérativement le diagramme dans le fichier
``Classes/Diagrams/classes.cld.clt`` (remplacer le fichier
existant). Le diagramme dessiné doit respecter la disposition
spatiale de l'ébauche fournie. Remplacer le fichier 
```Classes/Diagrams/classes.cld.png`` fourni.

Avant de clore ce ticket faire un très bref bilan
sur ce qui a été fait, est à faire, doit être corrigé/amélioré,
etc. Ce bilan devrait être le dernier message posté dans ce
ticket avant cloture.

________

- [ ] (010) Définition du modèle de classes
    - M ``Classes/classes.cls``
- [ ] (015) Compilation sans erreur (``use -c``)
- [ ] (020) Création d'un diagramme de classes global.
    - M ``Classes/Diagrams/classes.cld.clt``
    - M ``Classes/Diagrams/classes.cld.png``
- [ ] (900) Ecriture du bilan.
