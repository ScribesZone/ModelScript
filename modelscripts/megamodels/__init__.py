from abc import ABCMeta, abstractproperty

from typing import Text, Optional, Callable, List

from modelscripts.base.issues import WithIssueList
from modelscripts.base.sources import SourceElement, SourceFile

class Model(SourceElement, WithIssueList):
    __metaclass__ = ABCMeta

    model_registry=[]

    def __init__(self,
                 source=None,
                 name=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        #type: (Optional[SourceFile], Optional[Text], Optional[Text], Optional[int], Optional[Text], Optional[Text]) -> None
        SourceElement.__init__(self,
            name=name, code=code, lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)
        self.source=source  #type: Optional[SourceFile]
        WithIssueList.__init__(
            self,
            parent=(None if source is None else source.issueBox))
        # if self.source is not None:
        #     parentBox=self.source.issueBox
        # else:
        #     parentBox=None
        # self.issueBox=IssueBox(parent=parentBox) #type: IssueBox

        Megamodel.registerModel(self, self.metamodel)


    @abstractproperty
    def metamodel(self):
        pass

Cls=Callable
OptCls=Optional[Cls]

class Metamodel(object):  # TODO should be model instead of object
    def __init__(self,
                 id,
                 label,
                 extension,
                 modelClass,
                 sourceClass=None,
                 modelPrinterClass=None,
                 sourcePrinterClass=None,
                 diagramPrinterClass=None,
                 ):
        #type: (Text, Text, Text, Cls, OptCls, OptCls, OptCls, OptCls) -> None
        self.id=id
        self.label=label
        self.extension=extension,
        self.modelClass=modelClass
        self.sourceClass=sourceClass
        self.modelPrinterClass=modelPrinterClass
        self.sourcePrinterClass=sourcePrinterClass
        self.diagramPrinterClass=diagramPrinterClass
        Megamodel.registerMetamodel(self)

    def registerSource(self, cls):
        # TODO: check that cls is a subclass
        self.sourceClass=cls

    def registerModelPrinter(self, cls):
        # TODO: check that cls is a subclass
        self.modelPrinterClass=cls

    def registerSourcePrinter(self, cls):
        # TODO: check that cls is a subclass
        self.sourcePrinterClass=cls

    def registerDiagramPrinter(self, cls):
        # TODO: check that cls is a subclass
        self.diagramPrinterClass=cls

class Megamodel(object):

    _metamodelById={}
    #type: (Text) -> Metamodel

    _metamodelByLabel={}
    #type: (Text) -> Metamodel

    _metamodelByExtension={}
    #type: (Text) -> Metamodel

    _modelsByMetamodel={}
    #type: (Metamodel) -> List[Model]

    @classmethod
    def registerMetamodel(cls, metamodel):
        #type: (Metamodel) -> None
        Megamodel._metamodelById[metamodel.id]=metamodel
        Megamodel._metamodelByLabel[metamodel.label]=metamodel
        Megamodel._metamodelByExtension[metamodel.extension]=metamodel

    @classmethod
    def registerModel(cls, model, metamodel):
        #type: (Model) -> None
        if metamodel not in Megamodel._modelsByMetamodel:
            Megamodel._modelsByMetamodel[metamodel]=[]
        Megamodel._modelsByMetamodel[metamodel].append(model)

    @classmethod
    def metamodels(cls):
        #type: () -> List[Metamodel]
        return cls._metamodelById.values()

    @classmethod
    def metamodel(cls, id=None, label=None, ext=None):
        #type: () -> Optional[Metamodel]
        assert id is not None or label is not None or ext is not None
        if id is not None:
            return (
                None if id not in cls._metamodelById
                else cls._metamodelById[id])
        if label is not None:
            return (
                None if id not in cls._metamodelByLabel
                else cls._metamodelByLabel[label])
        if ext is not None:
            return (
                None if id not in cls._metamodelByExtension
                else cls._metamodelByExtension[ext])

    @classmethod
    def models(cls, metamodel=None):
        #type: () -> List[Model]
        if metamodel is None:
            return cls._modelsByMetamodel.values()
        else:
            return cls._modelsByMetamodel[metamodel]








class ModelDependency(object):
    def __init__(self,
                 sourceModel, targetModel,
                 sourceElement=None):
        self.sourceModel=sourceModel
        self.targetModel=targetModel
        self.sourceElement=sourceElement


# TODO: move this elsewhere
# class Importer(object):
#     @classmethod
#     def getFileName(cls, label, extension):
#         return label
#
#     @classmethod
#     def getClassModelSource(cls, issueBox, label):
#         filename = cls.getFileName(
#             label,
#             extension='.clm')
#         return ClassModelSource(filename)
#
#     @classmethod
#     def getUsecaseModelSource(cls, issueBox, label):
#         filename = cls.getFileName(
#             label,
#             extension='.ucm')
#         return UsecaseModelSource(filename)
#
#     @classmethod
#     def getScenarioModelSource(cls, issueBox, label):
#         filename = cls.getFileName(
#             label,
#             extension='.scm')
#         return ScenarioEvaluationModelSource(filename)
#
#     @classmethod
#     def getModelSource(cls, issueBox, kind, label):
#         if kind == '.clm':
#             return cls.getClassModelSource(issueBox, label)
#         elif kind == '.ucm':
#             return cls.getUsecaseModelSource(issueBox, label)
#         elif kind == '.scm':
#             return cls.getScenarioModelSource(issueBox, label)
#         else:
#             raise NotImplementedError('model %s are not implemented' % kind)
