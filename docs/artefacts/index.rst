.. _Artefacts:

Artefacts
----------

La méthode ModelScript défini une structure d'artefacts, c'est à dire
de répertoires et de fichiers, avec des noms précis.
Chaque tâche indique comment définir le contenu de chaque fichier.

concepts/
'''''''''

::

    concepts/                   Description des concepts.

        besoins/                Résultats de la collecte/analyse des besoins
            ...

        glossaires/             Glossaires du projet.
            glossaires.gls      Glossaires exprimés en GlossaryScript.
            status.md           Status.

        classes/                Modèle de classes.
            classes.cl1         Modèle exprimé en ClassScript1.
            diagrammes/         Diagrammes de classes.
            status.md           Status.

        objets/                 Modéles d'objets.
            o<N>/               Modèle d'objets n°N (modèle positif)
                o<N>.ob1        Modèles d'objets exprimés en ObjectScript1.
                diagrammes/     Diagrammes d'objets en différents formats.
            ...                 ...
            on<N>               Modèle d'objets négatifs.
            ...                 ...
            status.md           Status.

dynamique/
''''''''''

::

    dynamique/                  Description du comportement du système.

        cu/                     Modèles de cas d'utilisation.
            cu.uss              Cas d'utilisation en UsecaseScript.
            diagrammes/         Diagrammes de cas d'utilisation.
            status.md           Status.

        scenarios/              Scénarios conceptuels.
            s<N>/               Scénario n°N.
                s<N>.sc1        Scenario representé en ScenarioScript1.
                diagrammes/     Diagrammes liés au scénario.
            ...
            status.md           Status.

        permissions/            Modèle de permissions.
            permissions.pes     Modèle exprimé en PermissionScript.
            status.md           Status.

ihm/
''''

::

    ihm/

        taches/                 Modèles de tâches.
            <cu1>/              Modèle de tâches pour le cu <cu1>.
                taches-<cu1>.kxml      Modèle de tâches exprimé en KMade.
                taches-<cu1>.pdf       Modèle de tâches représenté en pdf.
            ...                 ...
            status.md           Status.

        ihm-abstraite/          Modèles d'interface abstraite.
            <cu1>/              Interface abstraite pour le cu <cu1>.
                ihma-<cu1>.pdf  Interface abstraite représentée en pdf.
            status.md           Status.

        ihm-concrete/           Interface concrète du système.
            charte-graphique.pdf    Charte graphique
            ...
            status.md           Status.

        evaluation/             Evaluation de l'interface
            analysis/
                evaluation-heuristique.pdf
            tests/
                protocole.pdf
                rapport.pdf
            status.md           Status.

bd/
'''

::

    relations/              Modèle de relations.
        relations.res       Modèle de relations exprimé en RelationScript.
        status.md           Status.

    sql/                    Implémentation SQL de la base de données.
        schema/             Schéma de la base de données.
            schema.sql      Schéma de la base de données exprimé en SQL.
        jdds/               Jeux de données.
            jdd<N>.sql      Jeux de données positif numéro N
            jddn<M>.sql     Jeux de données négatif numéro M
            ...
        requetes/           Requêtes
        cree-la-bd.sh       Script de création de la base de données.
        status.md           Status.

projet/
'''''''

::

    projet/
        sprint<N>/          Information à propos du Nième sprint.
            audit/
                audit.pdf
                resume.md
        plannings/
            planning-previsionnel.gan
            planning-intermediaire.gan
            planning-effectif.gan
            diagrammes/
                planning-previsionnel.gan.png
                planning-previsionnel.res.png
                planning-previsionnel.github.png
                planning-intermediaire.gan.png
                planning-intermediaire.res.png
                planning-intermediaire.github.png
                planning-effectif.gan.png
                planning-effectif.res.png
                planning-effectif.github.png
        audit/
            audit.pdf
            resume.pdf
        retrospective/
            retrospective.md
        suivi-du-temps/
            <XXX>.md
        suivi/
            suivi.trs
        done.md
        status.md


dev/
''''

::

    dev/                    Development artefacts including code.
        <CASESTUDY>/        Code containing the software
            status.md       Development status




    participants/           Participant model.
        participants.pas    Participant model expressed in ParticipantScript.
        status.md           Work status.


    playground/             Space for learning, prototyping, ...

    status.md               Global status of the work.