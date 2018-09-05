# coding=utf-8

# check failing tests


#================================================================
#   General
#================================================================


#TODO:1 Deal with Unexpected exception
#   when in source "except FatalError" -> FatalError exception
#   globally as well
#   generate a file with diagnosis ?
#   To be tested

#TODO:1 review print statement
#   remove space in command line output

#TODO:1 add a parameter in modelc for issue selection
#   the default should be ignoring hint.info (i.e. for info check)

#TODO:1 check if broken issue reporting
#   see us-import03 04
#   is seems that removing the parent in issue box
#   cause problem for understanding print display
#   or at least the error display has changed
#   Only "serious issue(s)" is displayed

#TODO:2 deployment: check how to deploy modelscript
#   should it be with ScribesInfra ?
#   a python package ?
#   check if it works at uni

#TODO:2 add first documentation
#   This could at least be one page per language
#   with objectives / examples / concepts / current states


#TODO:2 the list of source in testFinalMegamodel is not accurate
#   see the end of the tests
#   This problem might have been solved with sourceList algo

#TODO:2 finish coloring scheme for GEdit
#   check how to deploy the styles at uni

#TODO:3 restore/finalize modela
#   check how to configure it at uni

#TODO:3 fix strange printing for models

#TODO:2 metamodel uniquness in graph
#   see test imp-2-oksep01.cls
#   check how a dag based uniqueness can be implemented
#   uniqueness attrib has been added to class Metamodel
#   FYI import is done in class SourceImport
#   a method allUsedMetamodels  has been added
#   all metamodel.uniqueness has to be changed

#TODO:4 check what happen with cyclic import structure
#   at the moment this case is not relevant since
#   the metamodel types make it impossible

#================================================================
#   Glossary Model
#================================================================

#TODO:1 glossary: check what works or not
#   Using glossary is much better when using GEdit integration
#   since `ok`!  and `ko`? are displayed. Otherwise in colored
#   terminal.

#TODO:1 glossary: add tests

#TODO:2 add management of errors

#TODO:2 generalize astTextBlock2TextBlock to collect block
#   Somewhere (usecases?) a little framework has been defined
#   so that source element can define which textblock it owns.
#   A method should be added. This is cumbersome. It might be
#   better to use astTextBlock2TextBlock to collect easily all
#   TextBlock. To be checked.

#TODO:3 add some memoization or store some stuff


#================================================================
#   Class model
#================================================================

#FIXME:1 Duplicated issue box
# see for instance us-actor02.uss
# the number of issue box is strange
# the child/parent relationship is strange

#TODO:1 add inheritance of oppositeRoles/playedRoles
#   => add_inherited_attached_roles

#TODO:1 add/test link-object
#   ??? on a postit "link object copy"
#   -> check syntax in class model
#   -> check syntax in story model
#   -> check current implementation
#   the resolution order should be
#   object > link object > link
#   but this could fail if link object depends on link object
#   Not a priority a priori


#TODO:2 add composition
#   -> schema: constraint [0..1,1]
#   -> state : no cycle in object  (statechecker.py)

#TODO:2 add full support for textual constraints
#   To be done independenty from OCL support which is more complex
#   Check what works currently (mostly parsing?)

#TODO:2 add interface with USE for diagramming

#TODO:2 single class model
#   Having more than glossary/class model do not make too much
#   sense. This imply strange configuration where a model is used
#   in one place and another in the same import graph.
#   This could be added in the megamodel infrastructure.
#   This should apply for 'cl', 'gl', 'us', 'pe',
#   everything apart from 'ob', 'sc'

#TODO:3 improve/consolidate plantuml diagrams

#TODO:3 add class diagram specification

#TODO:4 add stereotype/tags to classes

#TODO:4 add stereotype/tags to associations

#TODO:???  on post it 'inv resolve -> variant str ???'

#TODO:3 check status of textal invariant
#   Resolution of items musy be done

#TODO:4 deal with operations


#TODO:2 add [0..1] constraint   not self.x->isUndefined

# TODO:3 restore the ability to call USE
#   this could be
#   1. for the user interface (drawing diagrams, OCL queries)
#   2. for the CLI (OCL queries)
#   3. as a compiler (not useful with new syntax)
# See modelscripts.tools.use.interfaces

#================================================================
#   OCL
#================================================================

#TODO:3 OCL: check status of OCL in classes models
#   Check engine / add tests ...
#   => oclchecker.py
#   No point in having OCL in class but not i objects

#TODO:3 OCL: ocl bracket
#   Currenly the ocl expression for invariants must
#   follow the regular nested indentation.
#   This is not convenient. One good option would be
#   to make some kind of preprocessing in the module brackets.py
#   to allow any string between line 'ocl' and a dedent line.
#   => brackets.py

#TODO:3 OCL for stories/scenarios/objects
#   This requires quite some work:
#   (1) Having a list of check point from StoryEvaluation
#   (2) Generating "soil" from StoryEvaluation
#   (3) Executing USE / Checking execution errors
#   (4) Parsing result with nth check correspondance
#   (5) Integrate the results as various statecheck violations


#================================================================
#   Stories
#================================================================

#TODO:2 add check for 'abstract' classes -> scenario
#   x : C is not allowed for abstract class

#TODO:2 check state of datatype/conformity

#TODO:2 add implementation of verb step
#   This should work for persona and usecases
#   Later this should work for task
#   May be introduce a verb or Activty superclass
#   It might be enough to start just with usecases

#TODO:3 connect frozenState issue box to parent box
#   When a state is copied a new
#TODO:3 solve problem with consecutive TextStep
#   Currently it is impossible to have empty TextSteps
#   This is due to a problem in the stories.grammar.tx parser
#   The problem is that it make it immpossible to have pieces
#   of text that are not linked to a piece of code. This
#   is annoying because this situation is quite common,
#   for instance when a piece of scenario text is not
#   related to the system.
#   If there is no solution with grammar.tx one option
#   is to change bracket so that comments are classified
#   top, middle, bottom depending on blank line before
#   and after.

#TODO:3 full support for readOnly
#   {readOnly} attributes can be initialized 'init' but not
#   updated 'update'.

#TODO:3 full support for addOnly
#   {addOnly} not supported for attributes (no multivaluated att)
#   Currently all roles can be {addOnly} since there is not deletion
#   Otherwise is is enough to remove 'delete' (a,R,b)

#TODO:3 datatype Date < String
#   This mostly impact story with value conformity

#TODO:3 improve numbering scheme for Step
#   Numbering is important because it is shown in issue message.
#   This is important when a issue is occurs in a check.
#   Currently Step numbering is like A.2.4 or A.2.before_4
#   It could make sense to have user define step numbering like
#       (1) create lea : Person
#   Adding user defined numbering require quite some analysis.
#
#TODO:3 add user numbering of StepEvaluatn
#   First check whzt this is useful for in practice
#   What exist is really poor.
#   Quite some analysis required.
#   Step could be repeated so something like SCA.CA2.3.2.before_4


#================================================================
#   Scenarios/object model
#================================================================

#TODO:3 add a check for "context/fragment" unused

#TODO:3 add OCL assert support in scenario
#        add name in metamodel and output
#        assert inv a: False
#        assert inv b: Failure
#        assert inv b
#        assert 2+3=5
#        assert b : 2+6=3

#TODO:3 scenario must use permission model

#TODO:3 deal with link deletion
#   This case should be rather easy to implement as there
#   is *a priori* nothing to check.
#   It should be possible to remove the
#   link from the current state. This is due to the fact that
#   the whole story infrastructure has been designed for this.

#TODO:3 deal with (link) object deletion
#   Like link deletion (see to do) but a bit more complicated
#   since we need to check that there is no link around
#   (option around).
#   (2) A bit more complicated that for

#TODO:2 check that there is only one class metamodel imported
#   TODO duplicated with
#   since a story interpret the object model with respect to the
#   current class model, it could be different from the class model
#   used to validate the object model. It can therefore give less
#   or more errors such as cardinality or so.
#   Currently the error seems to be ok, but it is most certainly
#   better to send a, error message if there is more than one
#   class model imported.

#================================================================
#   Object model
#================================================================

#TODO:3 avoid duplicate object state model
#   At some point objects models seem to have two analysis
#   most probably for the last frozenState generated by the
#   story evaluation and another one from the object model.
#   Check in the trace if still the case.

#TODO:2 remove useless location for checks in error messages
#   For instance
#       ... link01.obs:16:story.after_11:The attribute
#   -> adding an attribute to ObjectModel to distingush
#   object creation from scenario creation
#   -> locate ObjectModelSource et ScenarioModelSource

#TODO:2 add inheritance in ObjectModel.classExtension()
#   This is used at least to compute {id} properties


#================================================================
#   Usecase model
#================================================================

#TODO:2 usecase: check what works or not

#TODO:3 add a user model (projet d'integration)
#   Usecase model can define actors and import more
#   Task model can define actors and import more
#   Scenario model can define actors/personas and import more


#================================================================
#   Permission model
#================================================================

#TODO:3 permission model: check what works
#   This could require quite some work and adjustment.

#================================================================
#   User Model
#================================================================



#================================================================
#   Task Model
#================================================================

#TODO:3 add ConceptExpression

#TODO:3 add KMade printer

#================================================================
#   AUI Model
#================================================================

#TODO:3 Add Concept+Link

#TODO:3 Check what works


#================================================================
#   Quality Model
#================================================================

#TODO:3  Add a simple quality assurance model (qa?)
#   => voir le model
#   with rule, enforce rule
#   control in quality control (qc) model

#================================================================
#   Relational class model / relation model
#================================================================

#TODO:3  relational class model checks
# - pas d'association n-n
# - pas de classes associatives
# - pas de composition avec 0..1 du coté du composite
# - pas d'aggregation
# - pas de generalisation
# - pas de classe abstraite

#TODO:3 add support for code generation/transformation


#================================================================
#   Misc
#================================================================


#TODO:3 Installation procedure.
#       chmod +x for internal model-use
#       chmox +x for bin/*

#TODO:2 Solve file naming problem
#   Two related problems:
#   - Naming model /suppressing it. e.g.  class model
#   - removing path e.g.   import class model


#================================================================
#   Infrastructure
#================================================================

#TODO:2 add "single" info into the megamodel
#   => sc-composite2
#   See the TO DO single class model
#   See the TO DO in scenarios
#   Analysis needed
#   Not clear if multiple object model could be used
#   but it could be ok for scenario.
#   The poperty 'single' could be relative to a subgraph.
#   => megamodel.parser ?

#TODO:4 check how to restart/reset modelscritps in modelc nose tests
#   currently tests are run in an accumulated state
#   rather that a state from scratch
#   That means that the megamodel always accumulate information,
#   issue boxes and so on.
#   It would makes much more sense to start again the modelc.
#   Dunno how to do this with nose.
#   One option would be to have a "reset" feature on Megamodel

#TODO:3 add hierachical metrics

#TODO:2 add testing assert error message

#TODO:2 add some issue test coverage on framework
#   Something that gather all icode generated and associate them
#   with testcases.

#TODO:3 plantuml, check how to get errors from generation

#TODO:4- clean code with parent issue box
# The notion of parent between issue box between parents is flawed
# since we need to deal with a dag with shared parent and various
# source. The _doBindIssueBoxes has been commented but it
# might be good to do more cleaning.