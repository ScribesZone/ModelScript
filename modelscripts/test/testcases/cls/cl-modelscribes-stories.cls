    //@Issue cl.syn.Association.NoCompo 11
    //@Issue else *


class model ModelScribes

datatype Class_
datatype Association_
datatype TextBlock
datatype SimpleValue
datatype Metrics_

//---- metamodel objectModel ------------------------------------

package objects

class ObjectModel

class Object < ElementFromStep
// --> class_

class Link < ElementFromStep

class Slot < ElementFromStep
    attributes
        attribute_name:String
        //--> attributes
        simpleValue : SimpleValue

class ElementFromStep

composition HasObjects
    roles
        objectModel : ObjectModel[1]
        objects : Object[*]

composition HasLinks
    roles
        objectModel : ObjectModel[1]
        links : Link[*]

composition HasSlots
    roles
        object : Object[1]
        slots : Slot[*]

association IsSourceOf
    roles
        sourceObject : Object[1]
        targetLinks : Link[*]

association IsTargetOf
    roles
        targetObject : Object[1]
        sourceLinks : Link[*]

//---- metamodel stories ----------------------------------------

package stories

class Step
    attributes
        name : String

class CompositeStep < Step

class Story < CompositeStep

class VerbStep < CompositeStep
    attributes
        subjectName:String
        verbName:String

class TextStep < CompositeStep
    attributes
        textBlocK : TextBlock

package stories.operations

class OperationStep < Step

class UpdateOperationStep < OperationStep
    attributes
        isAction : Boolean

class ConsultOperationStep < OperationStep

class ObjectCreationStep < UpdateOperationStep
    attributes
        objectName:String
        class_:Class_

class ObjectDeletionStep < UpdateOperationStep
    attributes
        objectName : String

class SlotStep < UpdateOperationStep
    attributes
        objectName : String
        attributeName : String
        simpleValue: SimpleValue
        isUpdate:Boolean

class LinkCreationStep < UpdateOperationStep
    attributes
        sourceObjectName : String
        targetObjectName : String
        association : Association_

class LinkDeletionStep < UpdateOperationStep
    attributes
        sourceObjectName : String
        targetObjectName : String
        association : Association_

// class LinkObjectCreationStep < UpdateOperationStep
//v    attrib

class CheckStep < ConsultOperationStep
    attributes
        position : Integer


class ReadStep < ConsultOperationStep

association Contains
    roles
        parent : CompositeStep[0..1]
        steps : Step[*]


//---- metamodel stories.evaluations ------------------------------

package stories.evaluations

class StepEvaluation
    attributes
        name : String

class CompositeStepEvaluation < StepEvaluation

class StoryEvaluation < CompositeStepEvaluation

class CheckStepEvaluation < OperationStepEvaluation
    attributes
        metrics : Metrics_

association ResultsIn
    roles
        storyEvaluation : StoryEvaluation[0..1]
        finalState : ObjectModel[1]

association FrozesState
    roles
        checkStepEvaluation : CheckStepEvaluation[0..1]
        frozenState : ObjectModel[1]


association IsCheckedAt
    roles
        storyEvaluation : StoryEvaluation[1]
        checkEvaluations : CheckStepEvaluation[*]


class OperationStepEvaluation < StepEvaluation

association HasParentEvaluation
    roles
        stepEvaluations : StepEvaluation[*]
        parent : CompositeStepEvaluation[0..1]

association Evaluates
    roles
        stepEvaluations : StepEvaluation[*]
        step : Step[1]

association Accesses
    roles
        subject: StepEvaluation[1]
        accesses : Access[*]

association HasIssues
    roles
        issues : Issue[*]
        stepEvaluation : StepEvaluation[0..1]

association ComesFrom
    roles
        __element : ElementFromStep[*]
        step : Step[0..1]

//------ accesses ----

class Access

//------ Issue ----

class Issue

//---- metamodel classes ------------------------------------

package classes

class ClassModel

composition HasEnumeration
    roles
        model : ClassModel[1]
        enumerations : Enumeration[0..1]

composition HasDataType
    roles
        model : ClassModel[1]
        dataTypes: DataType[*]

composition HasClass
    roles
        model : ClassModel[1]
        classes : Class[*]

composition HasAssociation
    roles
        model : ClassModel[1]
        classes : Association[*]

composition HasPackage
    roles
        model : ClassModel[1]
        packages : Package[*]

class SimpleType
    attributes
        isOptional : Boolean
        isMultiple : Boolean

class Enumeration < SimpleType

composition HasLiteral
    roles
        enumeration : Enumeration[1]
        literals :EnumerationLiteral[*]

class EnumerationLiteral

class DataType < SimpleType

class Class
    attributes
        isAbstract : Boolean

association InheritsFrom
    roles
        subclasses : Class[0..*]
        superclasses : Class[0..*]

composition HasAttribute
    roles
        class : Class[1]
        attributes : Attribute[*]

class Attribute

association HasType
    roles
        __attributes : Attribute[*]
        type : SimpleType[1]

class Association

association HasRole
    roles
        association : Association[1]
        roles : Role[2..*]

composition HasRoleClass
    roles
        __roles : Role[*]
        type : Class[1]

class Role
    attributes
        label : String
        cardinalityMin : Integer
        cardinalityMax : Integer
        isOrdered : Boolean

class Package

