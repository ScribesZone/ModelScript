# coding=utf-8

import os
from modelscript.scripts.objects.parser import ObjectModelSource
from modelscript.test.framework import getTestFile


class TestObjectModel(object):
    THE_MODEL = None

    def __init__(self):
        if TestObjectModel.THE_MODEL is None:
            cls_File = getTestFile('obs/ob-main-turbo.obs')
            source_file = ObjectModelSource(cls_File)
            assert source_file.isValid
            TestObjectModel.THE_MODEL = source_file.objectModel
        self.model = TestObjectModel.THE_MODEL

    def testObjects(self):
        r={'zoe', 'babako', 'hardware', 'computing',
           'micro', 'astra', 'turbo', 'perspective'}
        object_names = [c.name for c in self.model.objects]
        assert set(object_names)==r
        assert set(self.model.plainObjects)==set(self.model.objects)
        assert len(self.model.plainLinks)==11
        assert len(self.model.links)==11

    def testSlot(self):
        o=self.model.object('zoe')
        assert len(o.slots)==2
        assert str(o.slot('name').simpleValue)=="'Zoe Zarwin'"
        assert o.slot('name').simpleValue.stringRepr=="'Zoe Zarwin'"
        assert o.slot('name').simpleValue.value=="Zoe Zarwin"
        assert o.slot('name').attribute.name=='name'
        assert o.slot('name').object==o
        assert o.slot('salary').simpleValue.stringRepr=="3500"
        assert o.slot('salary').simpleValue.value==3500


        o=self.model.object('micro')
        assert len(o.slots)==2
        assert o.slot('name').simpleValue.stringRepr=='"micro for all"'
        assert o.slot('name').attribute.name=='name'
        assert o.slot('name').object==o



