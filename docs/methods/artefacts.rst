.. _Artefacts:

Artefacts
----------

When using the ModelScript Method, all modeling artefacts are
to be stored in a predefined directory structure. This standard
layout defines the name of each directory but also the content of
each directories, including in most cases the name of the files.

Only a directory subset of the directory can be selected for a
simplified method.

::

    requirements/           Results of (RE)quirements collect/analysis.
        ...

    glossaries/             Glossaries for the project.
        glossaries.gls      Glossaries expressed in GlossaryScript.
        status.md           Work status.

    classes/                Class model.
        classes.cl1         Class model expressed in ClassScript1.
        diagrams/           Class diagrams in different formats.
        status.md           Work status.

    objects/                Object models.
        o<n>/               Nth object model.
            o<n>.ob1        Object model expressed in ObjectScript1.
            diagrams/       Object diagrams in different formats.
        ...                 ...
        status.md           Work status.

    participants/           Participant model.
        participants.pas    Participant model expressed in ParticipantScript.
        status.md           Work status.

    usecases/               Usecase model.
        usecases.uss        Usecase model expressed in UsecaseScript.
        status.md           Work status.

    ui-tasks/               Task models.
        <ucname1>/          Task model for usecase <ucname1>.
            <ucname1>.kxml  Task model expressed in KMade.
            <ucname1>.pdf   Task model show as pdf.
        ...                 ...
        status.md           Work status.

    ui-abstract/            Models for the abstract user interface.

    ui-concrete/            Files for the concrete user interface.

    ui-evaluation/          Files for the evaluation of the user interface.
        analysis/
        tests/

    scenarios/              Scenarios models.
        s<n>/               Nth scenario.
            s<n>.sc1        The scenario represented as a ScenarioScript1.
            diagrams/       Scenario diagrams in different formats.
        ...
        status.md           Work status.

    permissions/            Permission model.
        permissions.pes     Permission model expressed in PermissionScript.
        status.md           Work status.

    relations/              Relation model.
        relations.res       Relation model expressed in RelationScript.
        status.md           Work status.

    sql/                    SQL implementation.
        schema/             Database schema.
            schema.sql      Database schema in SQL.
        datasets/           Datasets
            <n>.sql         Datasets in SQL.
        create-database.sh  Database creation script/
        status.md           Work status.


    tracks/                 Track model.
        tracks.trs          Tracks expressed in TrackScript.
        status.md           Work status.

    dev/                    Development artefacts including code.
        <CASESTUDY>/        Code containing the software
            status.md       Development status

    playground/             Space for learning, prototyping, ...

    status.md               Global status of the work.