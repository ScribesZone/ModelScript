# coding=utf-8
from __future__ import print_function
import os
from modelscripts.scripts.classes.parser import ClassModelSource
from test.modelscripts.drivers import getTestFile

class TestClassModel(object):

    def __init__(self):
        cls_File = getTestFile('cls/cl-main-cybercompany-a.cls')
        source_file = ClassModelSource(cls_File)
        assert source_file.isValid

        self.model=source_file.classModel

    def testClasses(self):
        r={'Employee', 'Department', 'Project'}
        class_names = [c.name for c in self.model.classes]
        assert set(class_names)==r
        assert set(self.model.classNames)==r


    def testAssocs(self):
        r={'WorksIn','WorksOn','Controls', 'Supervise'}
        assoc_names = {c.name for c in self.model.associations}
        print('SS'*10, assoc_names)
        assert assoc_names==r
        assert set(self.model.associationNames)==r

        assert set(self.model.regularAssociationNames)==r

    def testDataTypes(self):
        r={'Integer', 'Real', 'Boolean', 'String',
           'Date', 'Time', 'DateTime'}
        assert set(self.model.dataTypeNames)==r

    def testRolesShapes(self):
        ac = self.model.associationNamed['Controls']
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
        ac = self.model.associationNamed['Controls']
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
        ac = self.model.associationNamed['WorksOn']
        assert ac.isManyToMany
        assert not ac.isOneToMany
        assert not ac.isOneToOne

    def testClassRoles(self):
        c = self.model.classNamed['Employee']
        # ownedRoles
        ro={'departments', 'projects', 'supervisor', 'subordinates'}
        assert {r.name for r in c.ownedRoles}==ro
        # playedRoles
        rp={'employees','employees','supervisor', 'subordinates'}
        assert {r.name for r in c.playedRoles}==rp

        c = self.model.classNamed['Department']
        # ownedRoles
        ro={'employees', 'projects'}
        assert {r.name for r in c.ownedRoles}==ro
        # playedRoles
        rp={'departments','department'}
        assert {r.name for r in c.playedRoles}==rp

    def testEnumeration(self):
        assert len(self.model.enumerations)==0

#
#     department=classModel.classNamed['Department']
#     print('AA'* 10, department._ownedRoles)
#
#     assert set(r.name for r in department._ownedRoles) == set(['employee', 'projects'])
#     assert set(r.name for r in department._playedRoles) == set(['department'])
#
