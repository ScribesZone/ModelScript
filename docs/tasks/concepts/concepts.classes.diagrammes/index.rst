..  _`tâche concepts.classes.diagrammes`:

tâche concepts.classes.diagrammes
==================================

:résumé: L'objectif de cette tâche est créer un ou plusieurs diagrammes
    de classes.
:langage:  :ref:`ClassScript1`
:artéfacts:
    * ``concepts/classes/classes.cl1``
    * ``concepts/classes/diagrammes/classes.cld.clt``
    * ``concepts/classes/diagrammes/classes.cld.png``
    * ``concepts/classes/diagrammes/<nom>.cld.png``
    * ``concepts/classes/diagrammes/<nom>.cld.png``


(A) Diagramme global
--------------------

Il s'agit de créer un "diagramme global" de classes. Un tel diagramme
doit présenter toutes les classes du modèle ; par opposition avec les
"vues" qui ne présentent que certaines classes sélectionnées.

NOTE: Si une ébauche de diagramme a été fournie le diagramme dessiné
devra en respecter la disposition.

Pour créer un diagramme de classes se référer à la documention
de `USE OCL sur ScribesTools`_.

*   (1) Sauvegarder impérativement le diagramme dans le fichier
    ``concepts/classes/diagrammes/classes.cld.clt`` (remplacer le
    fichier existant). Utiliser pour cela la commande ``Save Layout``
    comme indiqué dans la documentation.

*   (2) Faire ensuite une copie d'écran du diagramme et remplacer le
    fichier ``concepts/classes/diagrammes/classes.cld.png`` fourni.

Respecter **impérativement** les noms de fichiers, entre autre l'extension
``.png``.

**ATTENTION**: le diagramme global doit impérativement montrer les
cardinalités ; afficher si possible les noms de rôles ou d'associations si
le diagramme reste visible.

(B) Vues
--------

Il peut être demandé de réaliser plusieurs diagrammes de vues.
Contrairement au diagramme global qui montre toutes les classes
(et est parfois peu lisible) une "vue" ne montre que certaines classes
sélectionnées, en montrant par exemple le détail de ces classes.

Pour chaque vue les fichiers ``concepts/classes/diagrammes/<NOM>.cld.*``
où ``<NOM>`` fait référence au nom de la vue. Les classes à masquer
peuvent être définies avec le menu contextuel de l'outil
(click droit)



..  _`use ocl`:
    http://scribetools.readthedocs.io/en/latest/useocl/index.html

..  _`USE OCL sur ScribesTools`:
    http://scribetools.readthedocs.io/en/latest/useocl/index.html#creating-diagrams
