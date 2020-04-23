# coding=utf-8
"""Parser for ClassScript"""

from typing import cast, Union
import os

from modelscript.base.grammars import (
    ASTNodeSourceIssue)
from modelscript.base.issues import (
    Levels)
from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.metamodels.demo import (
    DemoModel,
    Class,
    Reference,
    METAMODEL)
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscript.megamodels.models import (
    Placeholder)


__all__=(
    'ClassModelSource'
)


DEBUG = 0


ISSUES = {
    'CLASS_NAME_TWICE': 'cl.syn.ClassName.Twice',
    'REFERENCE_NAME_TWICE': 'cl.syn.ReferenceName.Twice',
    'REFERENCE_NO_CLASS': 'cl.res.Reference.NoClass',
    'SUPERCLASS_NO_CLASS': 'cl.res.Superclass.NoClass'

}


def icode(ilabel):
    return ISSUES[ilabel]


class DemoModelSource(ASTBasedModelSourceFile):
    """Source file representing a demo model.
    This class mostly contains the parser that convert the
    source lines into a model conforming to the demo metamodel.
    """

    def __init__(self, fileName: str) -> None:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        super(DemoModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

        # Here can be initialized parser-time variables

    @property
    def demoModel(self) -> DemoModel:
        # This method is useful for type checking. The return value
        # il a ClassModel not just a Model
        m = cast(DemoModel, self.model)
        return m

    @property
    def metamodel(self) -> Metamodel:
        return METAMODEL

    # ----------------------------------------------------------------
    #                          fillModel
    # ----------------------------------------------------------------

    def fillModel(self):
        """Convert syntactical elements (TextXNodes) into semantical ones,
        that is model elements. This method, "fillModel" is the first pass
        of the process. During this pass some elements may be left be
        unresolved. These elements are typically store as string in place
        of model elements). The second pass ("resolve") will eventually
        replace these string by the corresponding model elements."""

        def define_class(ast_class: 'TextXNode') -> bool:
            """A a new class to the model.

            This can raise some errors (e.g. class already defined)
            Otherwise the class is created. Embedded components (here
            references) are defined as well by calling the corresponding
            methods (here define_references).

            Args:
                ast_class: the node in the AST corresponding to the class.
            """

            class_name = ast_class.name
            if class_name in self.demoModel.classNames:
                # ---- class already defined ------------------
                ASTNodeSourceIssue(
                    code=icode('CLASS_NAME_TWICE'),
                    astNode=ast_class,
                    level=Levels.Error,
                    message=(
                            'Class "%s" is already defined' % (
                                class_name,
                            )))
            else:
                # ---- create class class ------------------
                c = Class(
                    name=ast_class.name,
                    model=self.demoModel,
                    astNode=ast_class,
                    isAbstract=ast_class.isAbstract)

                # ---- Process the class documentation -----
                c.description = astTextBlockToTextBlock(
                    container=c,
                    astTextBlock=ast_class.textBlock)

                # ---- Process the superclasses _____
                for ast_superclass in ast_class.superclasses:
                    define_superclass(c, ast_class, ast_superclass)

                # ---- Process the references references -----
                for ast_ref in ast_class.references:
                    define_reference(c, ast_ref)

        def define_superclass(class_: Class,
                              astClass: 'TextXNode',
                              superclassName : str) -> None:
            """Add the name of a superclass (a Placeholder actually,
            to the list of superclasses."""
            class_.superclasses.append(
                Placeholder(
                    placeholderValue=superclassName,
                    astNode=astClass,
                    category='Class'),
            )


        def define_reference(class_: Class, ast_ref: 'TextXNode') -> None:
            """ Add a reference to a given class.
            The reference is not fully resolved. The target of the
            reference may be unknown in this pass. Just store a string
            in place of the target class. This string will be replaced
            by the actual Class in the "resolve" pass.

            Args:
                class_: The class containing the reference. This is
                    a model element ; a semantical element, not syntactical
                    one.
                ast_ref: The AST element corresponding to the reference.
                    This is a syntactical element.
            """
            ref_name = ast_ref.name
            if ref_name in class_.referenceNames:
                # ---- Raise a error if the reference name is already used
                ASTNodeSourceIssue(
                    code=icode('REFERENCE_NAME_TWICE'),
                    astNode=ast_ref,
                    level=Levels.Error,
                    message=(
                            'Reference "%s" is already '
                            'defined in class %s.'
                            % (ref_name, class_.name
                               )))
            else:
                # ---- Create the reference ----
                r = Reference(
                    name=ref_name,
                    class_=class_,
                    isMultiple=ast_ref.multiplicity == 'many',
                    target=Placeholder(
                        placeholderValue=ast_ref.target,
                        astNode=ast_ref,
                        category='ClassRef'),
                    astNode=ast_ref
                )

                # ---- Process the reference documentation ----
                r.description=astTextBlockToTextBlock(
                    container=class_,
                    astTextBlock=ast_ref.textBlock)


        for declaration in self.ast.model.declarations:
            type_ = declaration.__class__.__name__
            if type_ == 'Class':
                define_class(declaration)
            else:
                raise UnexpectedCase(  # raise:OK
                    'declaration of %s not implemented' % type_)
        pass

    # ----------------------------------------------------------------
    #                          Resolution
    # ----------------------------------------------------------------

    def resolve(self) -> None:
        """This method corresponds to the second phase of the process
        of model creation.
        During this process the symbol resolution is performed, that is
        all strings that stands for a model element are replaced by
        a reference to this element."""

        def resolve_class_content(class_: Class):
            """Resolves all symbols left in the class.
            In practice this means the target of each references
            contained in the class."""

            def resolve_superclasses():
                """Replace class name placeholder by the actual classes."""
                actual_superclasses = []
                for superclass_placeholder in class_.superclasses:
                    name = superclass_placeholder.placeholderValue
                    actual_class = self.demoModel.class_(name)
                    if actual_class is None:
                        ASTNodeSourceIssue(
                            code=icode('SUPERCLASS_NO_CLASS'),
                            astNode=class_.astNode,
                            level=Levels.Error,
                            message=(
                                'Class "%s" does not exist. '
                                "Can't be the superclass of %s."
                                % (name, class_.name)))
                    else:
                        actual_superclasses.append(actual_class)
                class_.superclasses = actual_superclasses

            def resolve_references():
                """Resolves all the placeholders contained in references.
                reference. In practice these are the targets of the
                references.
                """
                for ref in class_.references:
                    target_class_name = ref.target.placeholderValue
                    target_class = self.demoModel.class_(target_class_name)
                    if target_class is None:
                        # the reference has an error. Remove it from the
                        # model. This allows to keep the model clean
                        # with only valid model elements.
                        del class_._referenceNamed[ref.name]
                        ASTNodeSourceIssue(
                            code=icode('REFERENCE_NO_CLASS'),
                            astNode=ref.target.astNode,
                            level=Levels.Error,
                            message=(
                                'The class "%s" mentioned in '
                                'reference "%s" does not exist.'
                                % (target_class_name, ref.name)))
                    else:
                        ref.target = target_class

            resolve_references()
            resolve_superclasses()

        super(DemoModelSource, self).resolve()

        for c in self.demoModel.classes:
            resolve_class_content(c)


METAMODEL.registerSource(DemoModelSource)
