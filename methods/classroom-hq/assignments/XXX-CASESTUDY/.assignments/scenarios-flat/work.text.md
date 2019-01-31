[XXX-CASESTUDY] Scenarios_Plats
===========================================================

Les modèles de scénarios à compléter se trouvent dans les fichiers
``scenarios/s<N>/s<N>.ob1`` (où ``<N>`` est un entier).

Les modèles de scénarios doivent être écrits en ScenarioScript1.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/languages/scenarios1/index.html) lorsque nécessaire.

L'objectif de cette tâche est de traduire dans un premier temps
les textes en scénarios "plats", c'est à dire une simple suite 
d'instructions ``!``. Les fichiers de scénarios obtenus seront 
modifiés par la suite pour leur ajouter une structure.

Les tâches ci-dessous doivent être répétées pour chaque scénario.

### Tâche à réaliser

En pratique, comme dans les modèles d'objets, il s'agit dans 
cette tâche simplement de traduire le texte des scénarios 
en une suite d'instructions ``!`` *à plat". Voir la tâche
concernant les modèles d'objets pour plus de détail.

**NOTE 1**: Si le fichier ``s<N>.sc1``  n'est pas vide ignorer 
les éventuelles instructions comme ci-dessous :

    --@ context 
        ...
    --@ end
    --@ ... va ...
        ...
    --@ end

Ignorer également les emboîtements correspondants, s'ils sont présents.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/languages/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status.html#rules).
________

Pour chaque scénario s<N> (où ``<N>`` est un entier) :
- [ ] (010) Traduction du scenario/S<N> en langage soil.
    - M ``scenarios/s<N>/s<N>.scs``
- [ ] (020) Vérification de l'alignement du scenario N avec le modèle de classes.
- [ ] (030) Création du diagramme d'état final pour le scenario N.
    - M ``scenarios/s<N>/diagrams/S<N>.scd.olt``
    - M ``scenarios/s<N>/diagrams/S<N>.scd.png``
- [ ] (900) Ecriture du status final.
    - M ``scenarios/status.md``
