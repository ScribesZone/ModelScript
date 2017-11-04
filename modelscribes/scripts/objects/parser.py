# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from typing import Text
from modelscribes.metamodels.objects import (
    METAMODEL
)
from modelscribes.use.sex.parser import (
    SexSource,
)

from modelscribes.base.preprocessors import (
    Preprocessor,
    RegexpTransfo,
    PrefixToCommentTransfo
)


class ObsToSoilPreprocessor(Preprocessor):
    def __init__(self):
        super(ObsToSoilPreprocessor, self).__init__(
            sourceText='object model',
            targetText='.soil object model',
            targetExtension='.soil'
        )
        self.addTransfo(RegexpTransfo(
            '^ *! *check *',
            'check -v -d -a' ))
        self.addTransfo(PrefixToCommentTransfo((
            'scenario',
            'import',)))


class ObjectModelSource(SexSource):

    def __init__(self, originalFileName):

        super(ObjectModelSource, self).__init__(
            originalFileName,
            preprocessor=ObsToSoilPreprocessor(),
            allowedFeatures=[
                'query',
                'createSyntax',
                'topLevelBlock']
        )

    @property
    def metamodel(self):
        return METAMODEL


METAMODEL.registerSource(ObjectModelSource)
