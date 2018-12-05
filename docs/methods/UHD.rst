UHD - UML/HCI/DB Layouts
========================

The learning objectives of UHD projects includes:
* glossaries
* class diagrams
* object diagrams
* conformity between class diagrams and object diagrams
* TBC

Directory Layout
----------------

The layout for a UML/HCI/DB project is as following (TBC) ::

    requirements/           The result of (RE)quirements collect/analysis.

    glossaries/             Glossaries for the project.
        glossary.gls        Glossary represented as a (GL)lossary (S)cript.

    classes/                The class model.
        classes.cls         Class model represented as a (CL)ass (S)cript.
        diagrams/           Class diagrams in different flavors.

    objects/                Object models.
        1/                  First object model.
            objects.obs     Object model represented as an (OB)ject (S)cript.
            diagrams/       Object diagrams in different flavors.

    relations/              Relation models
        relations.res

    participants/           The participant model.
        participants.pas    Participant model represented as a (PA)rticipant (S)cript.

    usecases/               The usecase model.
        usecases.uss        Usecase model represented as a (US)ecase (S)cript.

    ...

    scenarios/              Scenarios models.
        1/                  First scenario.
            scenario.scs        The scenario represented as a (SC)enario (S)cript.
            Diagrams/           Scenario diagrams.

    permissions/            Permission model.
        permissions.pes     Permission subjects/actions/resources

    issues/                 Issue models.
        issues.iss          Issues expressed represented as a (IS)sue (S)cript.
