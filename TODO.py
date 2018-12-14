# coding=utf-8

#================================================================
#   General
#================================================================

#TODO:1 deployment: check how to deploy modelscript
#   should it be with ScribesInfra ?
#   a python package ?
#   check if it works at uni

#TODO:1 create cl1/ob1/sc1 scripts

#TODO:1 add an option to just launch syntax parsing
#   This should go to megamodels/sources.py
#   Add attribute in Megamodel for the type of models
#   (1) syntax, (2) dependencies, (3) full

#TODO:3 add a warning in modelc for useless directory
#   If a directory is on the command line
#   and it does contains any model files then issue a warning


#TODO:2 Deal with Unexpected exception
#   when in source "except FatalError" -> FatalError exception
#   globally as well
#   generate a file with diagnosis ?
#   To be tested

#TODO:2 review print statement
#   remove space in command line output

#TODO:2 add a parameter in modelc to select issue level
#   the default should be ignoring hint.info (i.e. for info check)

#TODO:2 allow model to have no name
#   if the model comes from a source then it will take the name of the file
#   otherwise it will be set according to the type of the model.
#   For instances "classes" for class model. See in megamodel.

#TODO:3 check issue reporting in Printers
#   see us-import03 04
#   removing the "parent" from issue boxes
#   cause problems for understanding Printer display
#   Only "serious issue(s)" is displayed in the child context

#TODO:3 the list of source in testFinalMegamodel is not accurate
#   see the end of the tests
#   This problem might have been solved with sourceList algorithm


#TODO:3 restore/finalize modela
#   check how to configure it at uni

#TODO:3 fix strange printing for models

#TODO:3 metamodel uniquness in graph should be implemented
#   see test imp-2-oksep01.cls
#   check how a dag based uniqueness can be implemented
#   uniqueness attrib has been added to class Metamodel
#   FYI import is done in class SourceImport
#   a method allUsedMetamodels  has been added
#   all metamodel.uniqueness has to be changed

#TODO:3 fix bug "modelc imports/imp-2-oksep01.obs"
#   fix bug "modelc imports/imp-2-oksep01.obs"
#   see modelc test
#   Two different glossaries are included in the same
#   graph. This should be an error but not error is raised.

#TODO:4 check what happen with cyclic import structure
#   at the moment this case is not relevant since
#   the metamodel types make it impossible

#TODO:3 Replace comment # to //
#   At the same time, deal with end of line //
#   This imply changing all tests cases and test driiver with #something
#   This will be nicer for # as protected in clas model
#   Could be used as well for # as foreign key in relation


#================================================================
#   Glossary Model
#================================================================

#TODO:1 add acronym, expansion, abbreviation

#TODO:1 rename label/translation to representation
#   this could be
#
#        representation: "Bibliotheque"
#   or
#        representations
#            fr: "Bibliotheque"
#            en: "Library"
#

#TODO:3 add default text language
#
#   glossary model X
#       | This glossary define ...
#       default language: fr
#
#   This requires changing the megamodel part to add the
#   attribute "default language" after the definition of "glossary model".


#TODO:2 replace `ok`? by `ok?`
#   This solution is better. Needs should be taken to add ? after letters.
#

#TODO:2 check best way to use coloring for `ok?` and `ok!`
#   Using glossary is much better when using GEdit integration
#   since `ok`!  and `ko`? are displayed. Otherwise in colored
#   terminal.

#TODO:3 add TextBlock/TextReference metrics in all model
# this could help testing that all testBlock have been processed
# and that how many references have been resolved or not.
# This should be available in all modules and therefore based on
# a generic way of registering TextBlock

#TODO:4 add some memoization or store some stuff

#================================================================
#   Class model
#================================================================

#FIXME:1 Duplicated issue box
# see for instance us-actor02.uss
# the number of issue box is strange
# the child/parent relationship is strange

#TODO:2 add inheritance of oppositeRoles/playedRoles
#   => add_inherited_attached_roles

#TODO:2 add/test link-object
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
#   Add optional attributes
#       syntax is OK
#       fillModel is OK
#       metamodel is OK

# TODO:3 restore the ability to call USE
#   this could be
#   1. for the user interface (drawing diagrams, OCL queries)
#   2. for the CLI (OCL queries)
#   3. as a compiler (not useful with new syntax)
# See modelscript.tools.use.interfaces

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

#TODO:2 add "can be used to / peut etre utilisé pour"
#TODO:2 usecase: check what works or not

#TODO:2 add import of participant model with actors imported
#   Add first the dependency in metamodel to participant model
#   Then add error "actor" already imported in participant model
#   Then add search of actor in participant/local model

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
#   Participant Model
#================================================================

# STATUS
    # The parser seems to be OK and synchronized with Sybille wishes.
    # No metamodel, no checking of any sort apart from syntax errors.
    # Should be enough anyway.

#TODO:3 add actors/persona in metamodel to be reused from usecase

#TODO:3 migrate Usecase actor to participant metamodel
#   One option is to have declaration only in participant model
#   or better (may be) to have both (useful?)

#TODO:3 xheck if "communication plan" would make sense
#   https://opentextbc.ca/projectmanagement/chapter/chapter-15-communication-planning-project-management/
#   https://www.teamgantt.com/blog/project-management-communication-plan


#================================================================
#   Task Model
#================================================================

#TODO:3 make sure KMade import is ok

#================================================================
#   AUI Model
#================================================================

#TODO:3 Add Concept reference
#   This could be a real concepts (Class/Assoc/Att/Role=
#   or an arbitrary id, just in case

#TODO:3 Add link/back link/label
#   Check what shoulf be in the language

#TODO:3 Add "transformation" / "rules"
#   it should be possible to explain from where the space comes
#   from. See the "relation" model for examples of transformation
#   Here space comes from tasks rather than concepts.

#TODO:3 Check what works

#================================================================
#   Relational class model / relation model
#================================================================


#TODO:2 add new notations (see todo in re-main)
#TODO:3 generate a ER diagram form model

#TODO:3 metamodel to be continued / add semantics
#   a few elements (relations, columns) seems to exist
#   but their content have to be checked.
#   In particular type, constraints
#   This should enable res/TO DO tests

#================================================================
#   Quality Model
#================================================================

#TODO:2  design a simple qa/qc model
#   => voir le model
#   with rule, enforce rule
#   control in quality control (qc) model

#TODO:3 add norm for python versionning
#   see https://www.python.org/dev/peps/pep-0440/
#   https://packaging.python.org/guides/distributing-packages-using-setuptools/#choosing-a-versioning-scheme

#================================================================
#   Project Model
#================================================================

#TODO:2  design a simple project model

#TODO:3 communication plan in project model ?
#   see TO DO in participant model
#   check if should go to participant model or project

#================================================================
#  Time Tracking Model
#================================================================

#TODO:2  design a simple Time Tracking model

#================================================================
#  Issue Model
#================================================================

#TODO:2  create issue model from CyberBibliotheque

#================================================================
#   Misc
#================================================================


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