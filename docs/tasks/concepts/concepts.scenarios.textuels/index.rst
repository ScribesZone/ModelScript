.. _`tâche concepts.scenarios.textuels`:

tâche concepts.scenarios.textuels
=================================

:résumé: L'objectif de cette tâche d'obtenir, à partir des résultats
    de la capture des besoins, des scénarios textuels éventuellement
    accompagnés de modèles d'objets.

:langage: :ref:`ScenarioScript1`, :ref:`ObjectScript1`
:résultat:
    * ``objects/o<N>/o<N>.ob1``
    * ``scenarios/s<N>/s<N>.sc1``

Introduction
------------

L'activité de capture des besoins donne lieu à différents textes
accompagnés d'autres ressources (images par exemple). Ces documents
se trouvent dans le dossier ``besoins``. L'objectif de cette tâche
est de :

*   extraire de ces documents une liste de scénarios accompagnés
    éventuellement de modèles d'objets,

*   de produire des scénarios textuels épurés et basé sur le glossaire.

Il peut être utile de compléter le jeu de scénarios ainsi extrait par
d'autres scénarios qu'il conviendra de faire valider auprès du client.

(A) Objets
----------

Les documents fournis peuvent faire référence à des exemples ou à des jeux
de données particuliers. Dans ce cas définir des modèles d'objets sous
forme de texte. Associer à chaque modèle un identificateur, par exemple "o3".
Créer ainsi le fichier ``objets/o3/o3.ob1`` en respectant la syntaxe
du langage :ref:`ObjectScript1`. Dans un premier dans les modèles d'objets
seront uniquement représentés sous forme de documentation (utilisation
de ``|``). Les modèles d'objets seront "codés" par la suite dans la
:ref:`tâche concepts.objets`.

Si aucun jeu de données n'est fourni il peut être nécessaire
d'en "inventer" un (ou plusieurs). Cela permettera d'instancier des
scénarios comme indiqué ci-dessous. Les modèles d'objets serviront
également de base pour valider le modèle de classe. Ils serviront
finalement comme jeux de données pour valider le schéma de la base
de données.

(B) Scénarios
-------------

Des élements correspondant à des scénarios ou parties de scénarios
peuvent être fournis. Identifier ou numéroter les scénarios si ce n'est
pas déjà fait. Cela donnera lieu par exemple à des fichiers comme
``scenarios/s3/s3.sc1``.

Si les scénarios ne sont pas "instanciés" les instancier. Par exemple
la phrase "*Le client achète des places pour un spectacle*" sera
instancié en "*Paul achète 3 places pour 15€ pour le spectacle
L'homme invisible programmé le 19/02/2020 à 17h15*". La liste des
spectacles disponibles devra peut être être "inventée" si elle n'est pas
présente. Elle pourra être définie sous la forme d'un modèle d'objets
(voir ci-dessus) qui servira de "contexte" à ce scénario. Le fait que
"*Paul achète 3 places*" fait par contre partie du scénario puisqu'il
s'agit d'une action donnant lieu à un changement d'état.

Les scénarios auxquels on s'intéresse ici sont des scénarios systèmes :
on s'intéresse au système plutôt qu'aux raisons pour lequelles
les utilisateurs prennent telles ou telles décisions. Par exemple la
phrase "*Après avoir amener son fils à l'école ...*" peut être simplifiée
en se concentrant sur les interactions avec le système. Les informations
concernant les motivations de l'utilisateurs seront par contre
intéressantes pour la conception d'interface homme machine. Mais il
n'est pas nécessaire qu'elles figurent dans les scénarios auxquels
on s'intéresse ici.

(Z) Suivi et status
-------------------

**Suivi**: Des questions ou des hypothèses ? Voir la
:ref:`tâche projet.suivis`.

**Status**: Avant de terminer cette tâche écrire le status. Voir la
:ref:`tâche projet.status`.