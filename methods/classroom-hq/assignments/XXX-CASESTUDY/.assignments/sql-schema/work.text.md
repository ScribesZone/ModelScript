[XXX-CASESTUDY] SQL_Schema
===========================================================

### Artefacts

Le résultat de ce travail doit se trouver dans le 
fichier ``sql/schema/schema.sql``.

### Résumé

Il s'agit d'implémenter en SQL le schéma de la base de données. Si un
modèle de relations existe alors on cherchera a réaliser une traduction 
aussi fidèle et homogène faire se peut.

### Exemple

Le fichier ``sql/schema/schema.sql`` fourni contient un exemple de schéma.
(un jeu de données est également fourni). Dans un premier temps, ces 
ressources peuvent servir à comprendre/tester la création de la base
de données, réaliser éventuellement des premières requêtes, etc. 
Bien évdemment le contenu des fichiers fournis devra ensuite être
remplacé par le code à produire dans ce travail. Il est conseillé de
lire les tâches SQL avant de réaliser de commencer.  

### Implémentation du schéma de données

Implémenter le schéma relationnel en SQL revient concrètement 
à exécuter différentes instructions ``CREATE TABLE``. Ces instructions
doivent être écrites dans le fichier ``sql/schema.sql``. 
Se référer à le documentation du SQBD utilisé pour connaitre le détail de
la syntaxe SQL, les types de données disponibles, la manière d'écrire
les contraintes, etc.

Tester le schéma en executant le code avec une base de données vide.

### Script de création de la base de données

Un script de création ``sql/create-database.sh`` a pour rôle d'automatiser
la création de la base de données à partir du schéma. Le contenu de
ce script est fourni pour le SGBD ``sqlite``. Dans le cas d'un autre 
SGBD ce script pourra être réécrit/adapté afin d'avoir une seule et 
unique commande pour créer la base de données.
 
Avec sqlite entrer la commande suivante à partir du répertoire 
``sql/``:
```
create-database.sh
```
Ce script crée une base de données vide ``sql/database.sqlite3`` et charge
le schéma ``sql/schema/schema.sql``. L'exécution du script devrait
ressembler à cela :
```
Clearing database ... done.
Creating database schema ... done.
Empty database created.
```
Si nécessaire se référer au contenu du script pour plus d'information ;
pour changer par exemple la localisation de la base de données. Si un autre
SQBD est utilisé le contenu de ce script devra être adapté.

### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).

________

- [ ] (100) Implémentation du schéma relationnel en SQL.
    - M ``sql/schema/schema.sql``
- [ ] (200) Création d'une base de données vide.
- [ ] (900) Ecriture du status final.
    - M ``sql/status.md``
