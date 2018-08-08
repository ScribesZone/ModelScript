# coding=utf-8



import logging

from typing import Union, Optional

from modelscripts.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscripts.scripts.textblocks.printer import (
    TextBlockPrinter
)
from modelscripts.scripts.stories.printer import (
    StoryPrinter
)
from modelscripts.scripts.stories.printer.evaluation import (
    StoryBestPrinter
)
from modelscripts.base.styles import Styles
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    METAMODEL
)
from modelscripts.metamodels.textblocks import TextBlock

__all__ =(
    'ScenarioModelPrinter',
    'ScenarioModelPrinterConfig',
    'ScenarioModelPrinterConfigs'
)


# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

class ScenarioModelPrinterConfig(ModelPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top',
                 #------------------------
                 contentMode='self',  #self|source|model|no
                 summaryMode='top',  # top | down | no,
                 #------------------------
                 #------------------------
                 #------------------------
                 modelHeader='scenario model',
                 displayBlockSeparators=True,
                 displayEvaluation=True,
                 originalOrder=True,
                 useSyntax=True   #<-- TODO:- change to False
                 ):
        super(ScenarioModelPrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet,
            title=title,
            issuesMode=issuesMode,
            contentMode=contentMode,
            summaryMode=summaryMode)
        self.modelHeader=modelHeader
        self.displayBlockSeparators=displayBlockSeparators
        self.displayEvaluation=displayEvaluation
        self.originalOrder=originalOrder
        self.useSyntax=useSyntax

class ScenarioModelPrinterConfigs(object):
    default=ScenarioModelPrinterConfig()

class ScenarioModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (Union[ScenarioModel, ScenarioModel],  Optional[ScenarioModelPrinterConfig]) -> None
        if config is None:
            config=ScenarioModelPrinterConfig()
        else:

            #----------------------------------------------
            #TODO:- remove the adapter when possible
            #       the following code is an adapter that
            #       must be removed when a solution is found
            #       to have configuration dependent options
            #       In that case, the config provide will
            #       be directly
            assert(isinstance(config, ModelPrinterConfig))
            config.modelHeader='scenario model'
            config.displayEvaluation=True
            config.originalOrder=True
            #----------------------------------------------



        self.config=config #type: ScenarioModelPrinterConfig
        super(ScenarioModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )


        # Check if it make sense for ScenarioEvaluation
        assert isinstance(theModel, ScenarioModel)
        # super(ScenarioModelPrinter, self).__init__(
        #     theModel=theModel,
        #     summary=summary,
        #     displayLineNos=displayLineNos
        # )
        self.scenario=theModel
        self.modelHeader=self.config.modelHeader

        # self.doDisplayEvaluation=(
        #     self.config.displayEvaluation
        #     and self.scenarioEvaluation is not None)
        # self.originalOrder=self.config.originalOrder

    def doModelContent(self):
        super(ScenarioModelPrinter, self).doModelContent()
        self.scenarioModel(self.theModel)
        return self.output

    def scenarioModel(self, scenarioModel):

        #---- descriptors
        for d in scenarioModel.descriptors:
            self.doDescriptor(d)

        #---- actor instances
        if len(scenarioModel.actorInstanceNamed.values())>=1:
            self.outLine(self.kwd('actor instances'))
            for ai in scenarioModel.actorInstanceNamed.values():
                self.doActorInstance(ai)

        #---- contexts
        for c in scenarioModel.contexts:
            self.doContext(c)

        #---- scenarios
        for s in scenarioModel.scenarios:
            self.doScenario(s)

        return self.output

    def doContext(self, context):
        self.outLine('%s %s' % (
            self.kwd('context'),
            context.name)
        )
        text = StoryBestPrinter(
            story=context.story,
            storyEvaluation=context.storyEvaluation,
            # TODO:- add selection to configuraiton
            # useStory=XXX
        ).do()
        self.out(text)

    def doScenario(self, scenario):
        self.outLine('%s %s' % (
            self.kwd('scenario'),
            scenario.name)
        )
        text = StoryBestPrinter(
            story=scenario.story,
            storyEvaluation=scenario.storyEvaluation,
            # TODO:- add selection to configuraiton
            # useStory=XXX
        ).do()
        self.out(text)

    def doDescriptor(self, descriptor):
        #TODO:- generalize the value of descriptor
        #      currently only textBlock
        #      To be changed in the parser and may be add a
        #      descriptor value
        assert isinstance(descriptor.value, TextBlock), 'current limitation'
        block_text=TextBlockPrinter(
            textBlock=descriptor.value,
            config=self.config).do()
        self.outLine(self.kwd(descriptor.name))
        self.outLine(block_text, 1)
        return self.output

    def doActorInstance(self, ai):
        self.outLine('%s %s %s'%(
                ai.name,
                self.kwd(':'),
                ai.actor.name),
            indent=1)
        return self.output


    def doAccessSet(self, accessSet):
        self.outLine(self.ann('->  %i accesses' % len(accessSet.accesses)))
        for a in accessSet.accesses:
            self.doAccess(a)
        return self.output

    def doAccess(self, access):
        self.outLine(self.ann('   %s %s' % (
            access.action,
            access.resource.label )))
        return self.output

METAMODEL.registerModelPrinter(ScenarioModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
