# coding=utf-8



import logging

from typing import Union, Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.scripts.textblocks.printer import (
    TextBlockPrinter
)
from modelscript.scripts.stories.printer import (
    StoryPrinter
)
from modelscript.scripts.stories.printer.evaluation import (
    StoryBestPrinter
)
from modelscript.base.styles import Styles
from modelscript.metamodels.scenarios import (
    ScenarioModel,
    METAMODEL
)
from modelscript.metamodels.textblocks import TextBlock

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
                 # ------------------------
                 title=None,
                 issuesMode='top',
                 # ------------------------
                 contentMode='self',  # self|source|model|no
                 summaryMode='top',  # top | down | no,
                 # ------------------------
                 # ------------------------
                 # ------------------------
                 modelHeader='scenario model',
                 displayBlockSeparators=True,
                 displayEvaluation=True,
                 originalOrder=True,
                 useSyntax=True   # <-- TODO:- change to False
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
        self.modelHeader = modelHeader
        self.displayBlockSeparators = displayBlockSeparators
        self.displayEvaluation = displayEvaluation
        self.originalOrder = originalOrder
        self.useSyntax = useSyntax


class ScenarioModelPrinterConfigs(object):
    default = ScenarioModelPrinterConfig()


class ScenarioModelPrinter(ModelPrinter):

    theModel: ScenarioModel
    config: ScenarioModelPrinterConfig

    def __init__(self,
                 theModel,
                 config=None):
        if config is None:
            config = ScenarioModelPrinterConfig()
        else:

            # ----------------------------------------------
            # TODO: Remove the adapter below when possible
            #       Currently the printer created in "framework/output"
            #       takes a ModelPrinterConfig. The attributes below
            #       are not defined. So default valure are provided.
            #       The following code is an adapter that
            #       must be removed when a solution is found
            #       to have configuration-dependent options.
            #       In that case, the config provide will
            #       be directly.
            assert(isinstance(config, ModelPrinterConfig))
            config.modelHeader = 'scenario model'
            config.displayEvaluation = True
            config.originalOrder = True
            # ----------------------------------------------

        self.config = config
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
        self.scenario = theModel
        self.modelHeader = self.config.modelHeader

        # self.doDisplayEvaluation=(
        #     self.config.displayEvaluation
        #     and self.scenarioEvaluation is not None)
        # self.originalOrder=self.config.originalOrder

    def doModelContent(self):
        super(ScenarioModelPrinter, self).doModelContent()
        self.scenarioModel(self.theModel)
        return self.output

    def scenarioModel(self, scenarioModel):

        # ---- descriptors
        for d in scenarioModel.descriptors:
            self.doDescriptor(d)

        # ---- actor instances
        if len(list(scenarioModel.actorInstanceNamed.values())) >= 1:
            self.outLine(self.kwd('actor instances'))
            for ai in list(scenarioModel.actorInstanceNamed.values()):
                self.doActorInstance(ai)

        # ---- contexts
        for c in scenarioModel.contexts:
            self.doStoryContainer(c, 'context')

        # ---- fragments
        for f in scenarioModel.fragments:
            self.doStoryContainer(f, 'story')

        # ---- scenarios
        for s in scenarioModel.scenarios:
            self.doStoryContainer(s, 'scenario')

        return self.output

    def doStoryContainer(self, container, keyword):
        self.outLine('%s %s' % (
            self.kwd(keyword),
            container.name)
        )
        text = StoryBestPrinter(
            story=container.story,
            storyEvaluation=container.storyEvaluation,
            config=self.config,
            forceStory=not self.config.displayEvaluation
            # TODO:- add selection to configuraiton
            # useStory=XXX
        ).do()
        self.outLine(text, indent=1, removeLastEOL=True)
        self.outLine('')

    def doDescriptor(self, descriptor):
        assert isinstance(descriptor.value, TextBlock)
        block_text = TextBlockPrinter(
            textBlock=descriptor.value,
            config=self.config).do()
        self.outLine(self.kwd(descriptor.name))
        self.outLine(block_text, indent=1)
        return self.output

    def doActorInstance(self, ai):
        self.outLine('%s %s %s' % (
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
