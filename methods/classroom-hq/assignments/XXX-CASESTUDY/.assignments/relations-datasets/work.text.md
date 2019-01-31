[XXX-CASESTUDY] Relations_Datasets
===========================================================

### Artefacts 
Ce travail a pour but de compléter le modèle de relations
(fichier ``relations/relations.res``) en ajoutant un ou des 
jeux de données. Utiliser la documentation du langage [ModelScript](https://modelscript.readthedocs.io/en/latest/languages/relations/index.html) 
lorsque nécessaire.

### Résumé

Le "schéma" relationnel défini auparavant, s'il n'a pas été créé
à partire de "zero", est une "traduction" du modèle de classes relationnel.
Dans cette tâche il s'agit de définir un ou des jeux de données positifs 
ou négatifs. Si des modèles d'objets ont été définis auparavant, les jeux 
de données produits ici doivent correspondre à ces modèles d'objets.

### Jeux de données positifs

Définir un ou plusieurs jeux de données "positifs", c'est à dire 
respectant l'ensemble des spécifications du modèle de relations
(nombre et type des colonnes, contraintes de clés, clés étrangères,
contraintes provenant du domaine, etc.).

Si un ou des modèles d'objets existent, traduire en priorité ces
derniers.

Les jeux de données positifs doivent être écrits en utilisant les
mots clés ``dataset`` ou ``positive dataset``.

### Jeux de données négatifs

Définir un ou plusieurs jeux de données négatifs, c'est à dire
violant une ou plusieurs contraintes mentionnées ci-dessous.
Documenter le ou les problèmes (utiliser les lignes ``|``).

Utiliser les mots clés ``negative dataset`` pour définir les
jeux de données négatifs.

### Status final

Avant de clore ce ticket définir le status courant pour ce travail.
Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (100) Création/transformation du/en modèle de relations.
    - M ``relations/relations.res``
- [ ] (200) Explication en cas de non application des règles standards
    - M ``relations/relations.res``
    
- [ ] (300) Verification de l'alignement avec le modèle de classes.
    - M ```relations/relations.res``
- [ ] (900) Ecriture du status final.
    - M ``relations/status.md``
