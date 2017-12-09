# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.metamodels.objects import (
    METAMODEL
)

from modelscribes.scripts.scenarios.parser import (
    ScenarioEvaluationModelSource
)

from modelscribes.metamodels.scenarios import (
    ScenarioModel
)



# class ObsToScsPreprocessor(Preprocessor):
#     def __init__(self):
#         super(ObsToSoilPreprocessor, self).__init__(
#             sourceText='object model',
#             targetText='.soil object model',
#             targetExtension='.soil'
#         )
#         self.addTransfo(RegexpTransfo(
#             '^ *object *model *(?P<rest>.*)',
#             'scenario model {rest}'))
#         self.addTransfo(PrefixToCommentTransfo((
#             'scenario',
#             'import',)))


# class ObjectModelSource(SexSource):
#
#     def __init__(self, originalFileName):
#
#         super(ObjectModelSource, self).__init__(
#             originalFileName,
#             preprocessor=ObsToSoilPreprocessor(),
#             allowedFeatures=[
#                 'query',
#                 'createSyntax',
#                 'topLevelBlock']
#         )
#
#     @property
#     def metamodel(self):
#         return METAMODEL

class ObjectModelSource(ScenarioEvaluationModelSource):

    def __init__(self, originalFileName):

        super(ObjectModelSource, self).__init__(
            originalFileName
        )

        # save the model build by scenario (superclass)
        self._scenarioModel=self.model   #type: ScenarioModel

        # FIXME:1 AttributeError: 'NoneType' object has no attribute 'state'
        self.model=self._scenarioModel.scenarioEvaluation.state

        # force the source assignation so that the scenario source
        # as seen as the source of the object model
        self.model.source=self._scenarioModel.source
        # self._issueBox=self._scenarioModel.source._issueBox
    @property
    def objectModel(self):
        return self.model

    @property
    def scenarioModel(self):
        # type: () -> ScenarioModel
        m = self.model  # type: ScenarioModel
        return m

    @property
    def metamodel(self):
        return METAMODEL

    def emptyModel(self):
        # type: () -> ScenarioModel
        return ScenarioModel()  # type: ScenarioModel

METAMODEL.registerSource(ObjectModelSource)
