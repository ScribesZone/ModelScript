# coding=utf-8

import os
from modelscript.scripts.classes.parser import ClassModelSource
from modelscript.test.framework import getTestFile


class TestClassModel(object):
    THE_MODEL=None

    def __init__(self):
        if TestClassModel.THE_MODEL is None:
            cls_File = getTestFile('cls/cl-main-cybercompany-a.cls')
            source_file = ClassModelSource(cls_File)
            assert source_file.isValid
            TestClassModel.THE_MODEL = source_file.classModel
        self.model=TestClassModel.THE_MODEL

    def testClasses(self):
        r = {'Employee', 'Department', 'Project'}
        class_names = [c.name for c in self.model.classes]
        assert set(class_names)==r
        assert set(self.model.classNames)==r


    def testAssocs(self):
        r = {'WorksIn', 'WorksOn', 'Controls', 'Supervise'}
        assoc_names = {c.name for c in self.model.associations}
        assert assoc_names == r
        assert set(self.model.associationNames) == r
        assert set(self.model.plainAssociationNames) == r

    def testDataTypes(self):
        r = {'Integer', 'Real', 'Boolean', 'String',
           'Date', 'Time', 'DateTime', 'NullType'}
        assert set(self.model.dataTypeNames) == r

    def testRolesShapes(self):
        ac = self.model.association('Controls')
        assert ac.name == 'Controls'
        assert ac.roles[0].name == 'department'
        assert ac.sourceRole.name == 'department'
        assert ac.roles[1].name == 'projects'
        assert ac.targetRole.name == 'projects'
        assert ac.sourceRole.isSource
        assert ac.targetRole.isTarget
        assert ac.isBinary
        assert ac.roles[0].opposite == ac.roles[1]
        assert ac.roles[1].opposite == ac.roles[0]
        assert ac.roles[0].type.name == 'Department'
        assert ac.roles[1].type.name == 'Project'

    def testRolesCardinalities(self):
        ac = self.model.association('Controls')
        assert ac.roles[0].cardinalityMin == 1
        assert ac.roles[0].cardinalityMax == 1
        assert ac.roles[1].cardinalityMin == 0
        assert ac.roles[1].cardinalityMax is None
        assert ac.sourceRole.isOne
        assert ac.targetRole.isMany
        assert ac.isOneToMany
        assert ac.isForwardOneToMany
        assert not ac.isBackwardOneToMany
        assert not ac.isManyToMany
        assert not ac.isOneToOne
        ac = self.model.association('WorksOn')
        assert ac.isManyToMany
        assert not ac.isOneToMany
        assert not ac.isOneToOne

    def testClassRoles(self):
        c = self.model.class_('Employee')
        # ownedOppositeRoles
        ro={'departments', 'projects', 'supervisor', 'subordinates'}
        assert {r.name for r in c.ownedOppositeRoles} == ro
        # ownedPlayedRoles
        rp={'employees', 'employees', 'supervisor', 'subordinates'}
        assert {r.name for r in c.ownedPlayedRoles} == rp

        c = self.model.class_('Department')
        # ownedOppositeRoles
        ro={'employees', 'projects'}
        assert {r.name for r in c.ownedOppositeRoles} == ro
        # ownedPlayedRoles
        rp={'departments','department'}
        assert {r.name for r in c.ownedPlayedRoles} == rp

    def testEnumeration(self):
        assert len(self.model.enumerations) == 0

