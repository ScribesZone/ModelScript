# [CASESTUDY] Glossaire

Le glossaire à compléter se trouve dans le fichier
``glossaries/glossaries.gls``.
Le glossaire doit être écrit en GlossaryScript.
Se reporter à la [documentation](https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html) lorsque nécessaire.

### Ecriture du glossaire

Compléter le glossaire en respectant impérativement les [règles associées aux glossaire](https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rules).
    
### Alignement avec le texte des scénarios et des objets

Le glossaire doit être aligné avec les termes utilisés par le client.
En particulier il s'agit de "réécrire" les différents textes fournis
par celui-ci. Dans le contexte de cette tâche il est demandé plus
précisemment de réécrire les textes associés aux modèles d'objets et 
de scénarios.

En principe tous les autres 
textes devraient être réécrits, mais ce n'est pas demandé. 
Se concentrer sur les modèles de scénarios et objets.

Pour la réécriture suivre les [règles associées à la réécriture de textes](https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rewriting-texts).
     
### Alignement les autres modèles

Tout au long du projet il sera nécessaire de s'assurer en permance de 
l'alignement avec le glossaire de tous les modèles mais aussi 
du code (SQL, Java, etc.). Cela implique entre autre d'aligner non
seulement les textes, mais aussi les identificateurs.
Lire et appliquer les [règles associées à la réécriture d'identificateurs](https://modelscript.readthedocs.io/en/latest/scripts/glossaries/index.html#rewriting-identifiers).

### Questions et hypothèses

Si des questions ou des hypothèses surgissent lors de ce travail
définir celles-ci explicitement dans le modèle de suivi
(dossier ``tracks``). Reporter le numéro de ces questions/hypothèses
là où elles interviennent. Lire et appliquer les [règles associées au suivi](https://modelscript.readthedocs.io/en/latest/scripts/tracks/index.html#rules). 
 
### Status final

Avant de clore ce ticket définir le status courant pour ce travail. Lire et appliquer les [règles associées aux status](https://modelscript.readthedocs.io/en/latest/methods/status/index.html#rules).
________

- [ ] (100) Ajout d'entrées dans le glossaire.
    - M ``glossaries/glossary.gls``
- [ ] (300) Vérification des règles internes associées au glossaire
    - M ``glossaries/glossary.gls``
- [ ] (400) Réécriture du texte des modèles d'objets
    - M ``objects/*``
- [ ] (500) Réécriture du textes modèles de scénarios.
    - M ``scenarios/*``
- [ ] (600) Vérification de l'alignement avec les autres modèles.
- [ ] (900) Ecriture du status final.
    - M ``glossaries/status.md``
