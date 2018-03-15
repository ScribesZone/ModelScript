[CyberBibliotheque] Scenarios
==================================================================

Il s'agit d'aligner le Scenarios/1 avec :

* le modèle de classes
* le modèle de cas d'utilisation
* le modèle de permissions

En fonction du temps restant créer d'autres scénarios pour
augmenter leur couverture globale.

Alignement avec le modèle de classes
------------------------------------

Traduire le scénario ``Scenarios/1`` en language d'actions
"soil" (associé à USE OCL). Les instructions (!) doivent se
trouver sous les phrases traduites.

Vérifier que le scénario est conforme au modèle de classes.
Utiliser la commande ``use -qv xxx.cls  yyy.scs``.

Réaliser un diagramme d'objets correspondant à l'état à la
fin du scénario (voir ``Scenarios/1/Diagrams/index.rst``).


Alignement avec le modèle de cas d'utilisation
----------------------------------------------

Définir au début du scénario les instances d'acteurs impliqués
(par exemple ``--@actor pedro : Guichetier``).
Si nécessaire ajouter les acteurs correspondants dans
le modèle de cas d'utilisation.

Regrouper en blocs les étapes correpondant à chaque instance
de cas d'utilisation en respectant les règles suivantes :

*   Chaque bloc doit commencer par une directive de la forme
    ``--@usecase pedro valideUneEntree``.
*   Chaque bloc doit se terminer par ``--@end``
*   Le contenu du bloc doit être indenté (commentaires+actions !)
*   Seuls les commentaires/actions correspondant au contexte
    doivent être au niveau principal. Déplacer les éventuelles
    commentaires/actions à l'exterieur d'un bloc si nécessaire.


Alignement avec le modèle de permissions
----------------------------------------

Vérifier (manuellement) pour ce scénario que les accès fait
par chaque acteur/cas d'utilisation sont conformes au modèle de
permissions. Compléter si nécessaire le modèle de permissions.


Scénarios additionnels
----------------------

S'il vous reste du temps écrire d'autres scénarios
(Scenarios/2, Scenarios/3, etc.). L'objectif est
d'augmenter la couverture du modèle de classes et du modèle
de cas d'utilisation. Indiquer en commentaire dans chaque
scénarios quelle est l'intention du scénario, par exemple
"couvrir l'association A, montrer un exemple de modification
de l'attribut C.a, montrer un exemple ou le cas d'utilisation
CU se termine avec un échec du au manque de XXX".

Bilan
-----

Avant de clore ce ticket faire un très bref bilan
(sous la forme d'un message dans le ticket) sur ce qui a été
fait, est à faire, doit être corrigé/amélioré, etc.


________

- [ ] (010) Traduction du Scenarios/1 en langage soil.
    - M ``Scenarios/1/scenario.scs``
- [ ] (020) Vérification de l'alignement du Scenario/1 avec le modèle de classes.
- [ ] (030) Création du diagramme d'état final pour le Scenarios/1.
    - M ``Scenarios/1/Diagrams/scenario-end.olt``
    - M ``Scenarios/1/Diagrams/scenario-end.std.png``
- [ ] (040) Définition des instances d'acteur du Scenarios/1.
    - M ``Scenarios/1/scenario.scs``
- [ ] (050) Définition des instances de cas d'utilisation du Scenarios/1.
    - M ``Scenarios/1/scenario.scs``
- [ ] (060) Vérification de l'alignement avec le modèle de permissions
- [ ] (100) Ecriture d'un Scenarios/2 aligné avec les autres modèles
    - M ``Scenarios/2/scenario.scs``
- [ ] (110) Ecriture d'un Scenarios/3 aligné avec les autres modèles
    - M ``Scenarios/3/scenario.scs``
- [ ] (120) Ecriture d'autres Scenarios
- [ ] (900) Ecriture du bilan.

    
