# [XXX-CASESTUDY] Scenarios (plats)

Les modèles de scénarios à compléter se trouvent dans les fichiers
``scenarios/S<N>/S<N>.ob1`` (où <N> est un entier).

Les modèles de scénarios doivent être écrits en ScenarioScript1.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/scenarios1/index.html) lorsque nécessaire.

L'objectif de cette tâche est de traduire dans un premier temps
les textes en scénarios "plats", c'est à dire une simple suite 
d'instructions ``!``. Les fichiers de scénarios obtenus seront 
modifiés par la suite pour leur ajouter de la structure.

Les tâches ci-dessous doivent être répétées pour chaque scénario.

### Tâche à réaliser

En pratique il s'agit dans cette tâche simplement de traduire le texte des
scénarios dans une suite d'instructions ``!`` *à plat", comme pour 
les modèles d'objets.


**NOTE 1**: Si le fichier ``S<N>.sc1``  n'est pas vide ignorer 
les éventuelles instructions comme ci-dessous :

    --@ context 
        ...
    --@ end
    --@ ... va ...
        ...
    --@ end

Ignorer également les emboîtements correspondants.

**NOTE 2** Tout comme pour les modèles d'objets,  il peut être utile de remanier le
texte pour éliminer les phrases qui n'apportent rien au 
scénario. Certaines phrases expliquant le contexte peuvent cependant 
être gardées. Le scénario doit rester compréhensible par le client, tout
en ne comportant pas d'éléments superflus.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).
________

Pour chaque scénario S<N> (où <N> est un entier) :
- [ ] (010) Traduction du scenario/S<N> en langage soil.
    - M ``scenarios/S<N>/S<N>.scs``
- [ ] (020) Vérification de l'alignement du scenario N avec le modèle de classes.
- [ ] (030) Création du diagramme d'état final pour le scenario N.
    - M ``scenarios/S<N>/diagrams/S<N>.scd.olt``
    - M ``scenarios/S<N>/diagrams/S<N>.scd.png``
- [ ] (900) Ecriture du status final.
    - M ``scenarios/status.md``
