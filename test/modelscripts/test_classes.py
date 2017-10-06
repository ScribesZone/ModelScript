# coding=utf-8

from test.modelscripts import TEST_CASES_DIRECTORY

import os
import modelscribes.use.use.parser

def test_UseOclModel_Simple():
    testFile = 'Demo.use'
    use_model_file = modelscribes.use.use.parser.UseModelSource(
        os.path.join(TEST_CASES_DIRECTORY, 'use', testFile))
    assert use_model_file.isValid
    classModel = use_model_file.classModel
    print(classModel)
    class_names = [c.name for c in classModel.classes]
    for n in ['Employee', 'Department', 'Project' ]:
        assert n in class_names
    assoc_names = [c.name for c in classModel.associations]
    for n in ['WorksIn','WorksOn','Controls' ]:
        assert n in assoc_names

    ac = classModel.associationNamed['Controls']
    assert ac.name == 'Controls'
    assert ac.roles[0].name == 'department'
    assert ac.sourceRole.name == 'department'
    assert ac.roles[1].name == 'project'
    assert ac.targetRole.name == 'project'
    assert ac.sourceRole.isSource
    assert ac.targetRole.isTarget
    assert ac.isBinary
    assert ac.roles[0].opposite == ac.roles[1]
    assert ac.roles[1].opposite == ac.roles[0]
    assert ac.roles[0].type.name == 'Department'
    assert ac.roles[1].type.name == 'Project'
    assert ac.roles[0].cardinalityMin == 1
    assert ac.roles[0].cardinalityMax == 1
    assert ac.roles[1].cardinalityMin == 0
    assert ac.roles[1].cardinalityMax == None
    assert ac.sourceRole.isOne
    assert ac.targetRole.isMany
    assert ac.isOneToMany
    assert ac.isForwardOneToMany
    assert not ac.isBackwardOneToMany
    assert not ac.isManyToMany
    assert not ac.isOneToOne

    ac = classModel.associationNamed['WorksOn']
    assert ac.isManyToMany
    assert not ac.isOneToMany
    assert not ac.isOneToOne


    department=classModel.classNamed['Department']
    assert set(r.name for r in department.outgoingRoles) == set(['employee', 'project'])
    assert set(r.name for r in department.incomingRoles) == set(['department'])

