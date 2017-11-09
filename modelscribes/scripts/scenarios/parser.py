# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.metamodels.scenarios import (
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


class ScsToSoilPreprocessor(Preprocessor):
    def __init__(self):
        super(ScsToSoilPreprocessor, self).__init__(
            sourceText='scenario model',
            targetText='.soil scenario model',
            targetExtension='.soil'
        )
        self.addTransfo(RegexpTransfo(
            '^ *! *check *',
            'check -v -d -a' ))

        # remove megastatement as they are used
        # before preprocessing and are no longer useful.
        self.addTransfo(RegexpTransfo(
            '^ *(scenario|import|object)', # remove mega
            '' ))
        self.addTransfo(PrefixToCommentTransfo((
            'actor',
            'uci',
            'usecase',
            'end',
            'enduci',
            'context',
            'endcontext')))


class ScenarioEvaluationModelSource(SexSource):

    def __init__(self, originalFileName):

        super(ScenarioEvaluationModelSource, self).__init__(
            originalFileName,
            preprocessor=ScsToSoilPreprocessor())

    @property
    def metamodel(self):
        return METAMODEL


METAMODEL.registerSource(ScenarioEvaluationModelSource)