from modelscripts.metamodels.classes.classes import Class
from modelscripts.metamodels.classes.associations import Association



class AssociationClass(Class, Association):
    """
    Association classes.
    """
    def __init__(self,
                 name, model, isAbstract=False, superclasses=(),
                 package=None,
                 lineNo=None, description=None, astNode=None):
        # Use multi-inheritance to initialize the association class
        Class.__init__(self,
                       name=name,
                       model=model,
                       isAbstract=isAbstract,
                       superclasses=superclasses,
                       package=package,
                       lineNo=lineNo,
                       description=description,
                       astNode=astNode)
        Association.__init__(self,
                             name=name,
                             model=model,
                             kind='associationclass',
                             package=package,
                             lineNo=lineNo,
                             description=description, astNode=astNode)
        self.model._associationClassNamed[name] = self

    def isPlainAssociation(self):
        return False

    def isPlainClass(self):
        return False