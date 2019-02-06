.. _ModelScriptMethod:

Methods
=======

ModelScript comes with a simple method, the "ModelScript Method".
Strictly speaking instead of one method, this is a set of methods since
some method elements can be added or removed.

The method is decomposed in (1) tasks and (2) artefacts to be used/produced
by eash tasks. The method is modular in the sense that only a
few artefacts and/or steps can be used.

The method is based on a project layout for modeling *artefacts*.
It also relies on a set of tasks to be performed for the *process*.
Each tasks have to be concluded by an status file, a file which is not
currently written as a script.

..  toctree::
    :maxdepth: 3

    artefacts

    glossaires/index

    classes_conceptuel/index
    objets/index
    contraintes_ln/index
    objets_negatifs/index
    contraintes_ocl/index

    classes_relations/index
    relations_schema/index
    relations_jdd/index
    relations_jdd_negatifs/index
    sql_schema/index
    sql_jdd/index
    sql_jdd_negatifs/index

    scenarios_plats/index
    participants_cu/index
    cu_preliminaire/index
    cu_detaille/index
    scenarios_cu/index
    permissions_cu_classes/index
    ihm_taches/index
    ihm_abstraite/index
    ihm_concrete/index
    ihm_evaluation/index

    projet_participants/index
    projet_planning/index
    projet_planning_effectif/index
    projet_retrospective/index
    projet_livraison/index
    projet_audit/index
    projet_soutenance/index


    suivis/index
    status