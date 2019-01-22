[XXX-CASESTUDY] SQL_Schema
===========================================================

### Artefacts

Ce travail a pour but d'implémenter en SQL le schéma de la base données.
Le résultat doit se trouver dans le fichier ``sql/schema/schema.sql``.
Se référer à la documentation du SGBD utilisé pour toute information
sur le dialecte SQL correnspondant.

### Résumé

Implémenter en SQL le schéma de la base de données. Si un modèle de 
relations existe alors réaliser une traduction aussi fidèle et homogène
faire ce peut.

### Exemple

Le fichier ``sql/schema/schema.sql`` fourni contenient un exemple de schéma.
Un jeu de données est également fourni. Dans un premier temps, ces 
ressources peuvent servir à comprendre/tester la création de la base
de données, réaliser éventuellement des premières requêtes. 
Bien évdemment le contenu des fichiers fournis devra ensuite être
remplacé par le code à produire dans ce travail. Il est conseillé de
lire les tâches SQL avant de réaliser chaque tâches.  

### Implémentation du schéma de données

Implémenter le schéma relationnel en SQL revient concrètement les 
à exécuter différentes instructions ``CREATE TABLE``. Ces instructions
doivent être écrites dans le fichier ``sql/schema.sql``. 
Se référer à le documentation du SQBD utilisépour connaitre le détail de
la syntaxe SQL utilisées, les types de données disponibles, etc.

Tester le schéma en executant le code avec une base de données vide.

### Création de la base de données avec sqlite

Dans le cas où le SGBD utilisé est``sqlite`` un script automatisant la
création de base de données est fourni. Pour créer une base de données vide 
à partir du schéma, entrer la commande suivante à partir du répertoire 
``sql/``:
```
create-database.sh
```
Ce script crée une base de données vide ``sql/database.sqlite3`` et charge
le schéma ``sql/schema/schema.sql``. Si nécessaire se référer au contenu 
du script pour plus d'information ; pour changer par exemple la 
localisation de la base de données.     

### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (100) Implémentation du schéma relationnel en SQL.
    - M ``sql/schema/schema.sql``
- [ ] (200) Création d'une base de données vide.
- [ ] (900) Ecriture du status final.
    - M ``sql/status.md``
