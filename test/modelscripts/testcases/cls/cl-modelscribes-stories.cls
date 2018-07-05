class model ModelScribes


#---- metamodel stories ---------------------------------------------------

class Step
    attributes
        name : String

class CompositeStep < Step

class Story < CompositeStep

class VerbStep < CompositeStep

class TextStep < CompositeStep

class OperationStep < Step

class UpdateStep < OperationStep
    attributes
        isAction : Boolean

class ConsultStep < OperationStep

class ObjectCreationStep < UpdateStep

class ObjectDeletionStep < UpdateStep

class SlotStep < UpdateStep

class LinkCreationStep < UpdateStep

class LinkDeletionStep < UpdateStep

class LinkObjectCreationStep < UpdateStep

class CheckStep < ConsultStep

class ReadStep < ConsultStep

association Contains
    roles
        parent : CompositeStep[0..1]
        steps : Step[*]


#---- metamodel stories.evaluations ---------------------------------------

class StepEvaluation

class CompositeStepEvaluation < StepEvaluation

class StoryEvaluation < CompositeStepEvaluation

class OperationStepEvaluation < StepEvaluation

association Evaluates
    roles
        stepEvaluations : StepEvaluation[*]
        step : Step[1]

association Access
    roles
        stepEvaluations : Access[*]
        subject: StepEvaluation

association HasIssue
    roles
        stepEvaluation : StepEvaluation[0..1]
        issues : Issue[*]


#------ accesses ----

class Access

#------ Issue ----

class Issue