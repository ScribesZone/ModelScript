[XXX-CASESTUDY] SQL_JeuxDeDonnees
===========================================================

### Artefacts

Le résultat de ce travail doit se trouver dans le dossier 
``sql/datasets/``.

### Résumé

Il s'agit d'implémenter en SQL un ou des jeux de données positifs et un
ou des jeux de données négatifs.

### Exemple

Le repertoire ``sql/datasets/`` contient des exemples de jeux de données.
Il s'agit d'illustrer l'approche et de permettre de tester des requêtes
sur des données existantes. Le contenu de ces fichiers devra être 
remplacé par des jeux de donnés appropriés.
 
### Implémentation des jeux de données

Les jeux de donnéees doivent être implémentés via des instructions SQL
``INSERT``. Ces instructions doivent être écrites dans les fichiers 
``sql/datasets/<N>.sql`` ou ``<N>`` est le nom du jeu de données.

Si des modèles d'objets ou des jeux de données relationnels ont été
définis auparavant ces derniers doivent réutilisés autant que possible.

### Chargement des jeux de données

Le script de creation de base de données peut être utilisé pour charger
un jeu de données. Par exemple pour un jeu de données ``ds1`` la création
de la base de données se fait avec la commande suivante 
(le fichier ``datasets/ds1.sql`` doit exister) :
```
create-database.sh ds1
```

### Jeux de données positifs 

Par définition les jeux de données positifs doivent être conformes au
schéma de données. Aucune erreur ne devra donc être détectée lors du 
chargement. 

L'exécution du script ``create-database.sh`` avec le jeu de données
positif ``ds1`` devrait ressembler à cela :
```
Clearing database ... done.
Creating database schema ... done.
Loading dataset ds1 ... done.
Dataset ds1 loaded in database.
```

### Jeux de données négatifs

Inversement les jeux de données négatifs doivent générer des erreurs 
partout où les contraintes associées au schéma ne sont pas respectées.
Un jeu de données négatif pourrait produire un résultat comme suit :
```
Clearing database ... done.
Creating database schema ... done.
Loading dataset nds1 ...Error: near line 13: UNIQUE constraint failed: Movies.title
Error: near line 39: UNIQUE constraint failed: Cinemas.name
Error: near line 53: UNIQUE constraint failed: Spectators.name
Error: near line 68: UNIQUE constraint failed: IsOn.movie, IsOn.cinema
Error: near line 70: FOREIGN KEY constraint failed
...
```

Chacune des erreurs doit être répertoriée sous forme de commentaires
dans le fichier ``.sql``. Pour chaque erreur, indiquer la contrainte
violée. Utiliser pour cela le mot clé ``violates``. Un jeu de données
négatif pourrait ressembler à cela :
```
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts CBD');
--@ violates Spectators.PK
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Hoyts CBD');
--@ violates Spectators.FK_movie
INSERT INTO IsOn VALUES ('==> VIOLATION <==','Hoyts CBD');
--@ violates Spectators.FK_cinema
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','==> VIOLATION <==');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema Myer');
INSERT INTO IsOn VALUES ('Guardians Of The Galaxy','Event Cinema');
``` 

### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (100) Implémentation du schéma relationnel en SQL.
    - M ``sql/schema/schema.sql``
- [ ] (200) Création d'une base de données vide.
- [ ] (900) Ecriture du status final.
    - M ``sql/status.md``
