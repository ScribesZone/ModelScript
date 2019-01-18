[XXX-CASESTUDY] Relations
===========================================================

Cette tâche a pour but de créer le modèle de relations
(fichier ``relations/relations.res``). Utiliser la
documentation du langage [ModelScript](https://modelscript.readthedocs.io/en/latest/scripts/relations/index.html) lorsque nécessaire.

### Creation / Transformations

Le modèle de relations doit être créé à partir du modèle de classes,
s'il existe. Les règles de transformation standards doivent alors être 
respectées  autant que possible. Justifier l'application de ces 
transformations (mot-clé ``transformation``) en particulier lorsque les 
règles standards ne peuvent pas être appliquées directement.

### Contraintes

Définir les contraintes intégrité suivantes:
* les contraintes sur les colonnes,
* les contraintes d'intégrité référentielle,
* les autre contraintes.

Les contraintes sur les attributs doivent être exprimées directement
dans les colonnes correspondantes. Les contraintes d'intégrité référentielle
et les autres contraintes doivent être définies via le mot-clé 
``constraint``.

### Jeux de données positifs

Définir un ou plusieurs jeux de données positifs, c'est à dire 
correspondant à l'ensemble des spécifications du modèle de relations,
et en particulier à l'ensemble des contraintes enoncées. Utiliser pour 
cela les mots clés ``negative dataset``.

### Jeux de données négatifs

Définir un ou plusieurs jeux de données négatifs, c'est à dire 
violant une ou plusieurs contraintes d'incorrespondant à l'ensemble des spécifications du modèle de relations,
et en particulier à l'ensemble des containtes enoncées. Utiliser pour cela
le mot clé ``dataset``.

### Alignement avec le modèle de classes

Vérifier que toutes les informations présentes dans le modèle de
classes se retrouvent, d'un manière ou d'une autre, dans le modèle
de relations.

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
    - M ``permissions/status.md``
