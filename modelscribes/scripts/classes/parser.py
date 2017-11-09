# coding=utf-8

from __future__ import print_function

from modelscribes.base.preprocessors import (
    Preprocessor,
    RegexpTransfo,
    PrefixToCommentTransfo
)

from modelscribes.use.use.parser import UseModelSource
from modelscribes.metamodels.classes import METAMODEL

class ClsToUsePreprocessor(Preprocessor):
    def __init__(self):
        super(ClsToUsePreprocessor, self).__init__(
            sourceText='class model',
            targetText='.use class model',
            targetExtension='.use'
        )
        self.addTransfo(RegexpTransfo(
            '^ *class +model (?P<rest>.*)',
            'model {rest}'))
        self.addTransfo(PrefixToCommentTransfo((
            'package',)))


class ClassModelSource(UseModelSource):

    def __init__(self, originalFileName):
        super(ClassModelSource, self).__init__(
            originalFileName,
            preprocessor=ClsToUsePreprocessor())

    @property
    def metamodel(self):
        return METAMODEL

METAMODEL.registerSource(ClassModelSource)