[CyberBibliotheque] Contraintes en langage naturel
==================================================

Il s'agit ici de définir les contraintes à ajouter au modèle de classes.
Dans cette tâche les contraintes sont décrites en langue naturelle.
Par la suite ces contraintes pourraient être traduire en langage OCL,
mais ce n'est pas l'objectif de cette tâche. 
On s'intéresse de plus aux invariants que doivent vérifier chaque état
du système. Les pré et post conditions ne sont pas prises en compte ici.

## Représentation des invariants

Chaque contrainte doit comporter les éléments suivants :

1.  un **identificateur** (p.e. ``FormatMotDePasse``), 
2.  une **portée** d'application, c'est à dire la partie du diagramme
    de classes qui permet d'expliquer "où se trouve" la contrainte. 
    La zone est représentée par une liste de noms :
    * de classe (p.e. ``Personne``), 
    * d'associations (p.e. ``Concerne``),
    * d'attributs (p.e. ``Personne.nom``),
    * et/ou de roles (p.e. ``Personne.parents``).
3.  une **description** en langue naturelle. Idéalement la description 
    doit pouvoir être lue par le "client' aussi bien que par les 
    développeurs. 
    Elle doit à la fois faire référence au glossaire, mais également autant
    que possible aux identificateurs se trouvant dans le diagramme. La
    correspondance entre les éléments décrivant la portée du modèle doit
    être claire et non ambigüe.

## Exemple d'invariants

Ci-dessous un exemple d'invariant. A ajouter en fin du modèle de classes 
(``.cls``).

```
--@ invariant MomentConcerne
--     scope
--         Atelier.dateDeDebut
--         Atelier.dateDeFin
--         Concerne
--         Emprunt.dateDeSortie 
--     Si un emprunt concerne un atelier alors cet 
--     emprunt a eu lieu dans la période correspondant à l'atelier.
```
Dans l'exemple ci-dessus la notion de période n'est pas nécessairement
claire et la locution "a eu lieu" non plus. Il est possible de préciser 
la phrase ainsi :
```
--     Si un emprunt concerne un atelier alors cet 
--     la date de sortie de l'emprunt a eu lieu entre la date de début 
--     de l'atelier et sa date de fin.
```

## Méthode d'identification de contraintes

L'une des façons de trouver les contraintes et de passer un à un les 
différents éléments d'un modèle de classes. Il s'agit de lister les
contraintes portant sur :
* un attribut, typiquement les contraintes de domaine (e.g. age>0) 
* plusieurs attributs d'une classe (e.g. min<=max)
* une association
* plusieurs associations

Lorsque plusieurs associations forment un cycle il assez probable qu'une
ou des contraintes s'appliquent au sein de ce périmètre.

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).
________

Définition des contraintes portant :
- [ ] (010) sur un seul attribut
    - M ``classes/classes.cls``
- [ ] (020) sur plusieurs attributs
    - M ``classes/classes.cls``
- [ ] (030) sur une association
    - M ``classes/classes.cls``
- [ ] (040) sur plusieurs associations
    - M ``classes/classes.cls``
