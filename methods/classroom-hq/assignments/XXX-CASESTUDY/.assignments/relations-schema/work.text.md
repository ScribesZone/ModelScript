[XXX-CASESTUDY] Relations_Schema
===========================================================

### Artefacts

Ce travail a pour but de créer le modèle de relations
(fichier ``relations/relations.res``). Utiliser la
documentation du langage [ModelScript](https://modelscript.readthedocs.io/en/latest/scripts/relations/index.html) lorsque nécessaire.

### Résumé

Le modèle de relations doit être créé à partir du modèle de classes,
s'il existe. Il s'agit plus précisemment de créé le "schéma" relationnel,
c'est à dire l'ensemble des relations et des contraintes que l'on peut
déduire à partir du modèle de classes-relations. Dans un second temps
seulement, d'éventuels jeux de données (datasets) seront ajoutés. Dans
ce travail on se limite à la création du schéma, pas de contenus.

### Transformations

Si le modèle de relations est créé à partir de zero (sans modèle
de classe alors cette partie peut être ignorée ainsi que toute
référence à la notion de transformation de modèle.

Lorsque des règles de transformation "standards" existent alors celles-ci
doivent être respectées à chaque fois que faire ce peut. Plus précisemment 
si une liste précise de transformations nommées a été fournie, il s'agit
alors d'indiquer voir de justifier l'application de ces transformations 
(mot-clé ``transformation`` et ``rule``). Ajouter un commentaire 
lorsque les  règles standards ne peuvent pas être appliquées directement.

### Contraintes

Définir les contraintes intégrité suivantes:

* les contraintes sur les colonnes (p.e. contraintes de domaine, mot
  clé ``dom``),

* les contraintes de clés (mot clé ``key``). Rappel: la notation
  "souligné" indique simplement que la colonne soulignée fait partie
  d'au moins une clé. Il peut y avoir plusieurs clés et une clé
  peut être composite. Ces informations ne peuvent pas être déduites
  de la notation "soulignée". Les contraintes de clés doivent donc 
  être exprimées explicitement.

* les contraintes d'intégrité référentielle (par exemple
  ``R[x] C= S[y]``),

* les autre contraintes. Si une contrainte ne peut pas être exprimées
  avec le modèle relationnel, celle-ci doit être spécifiée. Si cette
  contrainte provient du modèle de classes conceptuel, alors répéter
  uniquement le nom de la contrainte (par exemple 
  ``constraint AtLeastForItemPerDay``).

Les contraintes sur les colonnes doivent être exprimées directement
dans la relation correspondantes. Les contraintes d'intégrité 
référentielle et les autres contraintes doivent être définies au
"premier niveau" via le mot-clé ``constraint`` (ou ``constraint`` sur 
plusieurs lignes).

### Jeux de données

Dans ce travail les jeux de données (``dataset``) peuvent être ignorés.


### Alignement avec le modèle de classes

Vérifier que toutes les informations présentes dans le modèle de
classes se retrouvent, d'un manière ou d'une autre, dans le modèle
de relations et vice-versa.

### Status final

Avant de clore ce ticket définir le status courant pour ce travail.
Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (100) Création/transformation du/en modèle de relations.
    - M ``relations/relations.res``
- [ ] (300) Verification de l'alignement avec le modèle de classes.
    - M ``relations/relations.res``
- [ ] (900) Ecriture du status final.
    - M ``relations/status.md``
