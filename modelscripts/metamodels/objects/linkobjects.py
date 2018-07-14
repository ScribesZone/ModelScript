from modelscripts.metamodels.objects.objects import Object
from modelscripts.metamodels.objects.links import Link


class LinkObject(Object, Link):

    def __init__(self,
                 model, associationClass,
                 sourceObject, targetObject,
                 name,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        Object.__init__(
            self,
            model=model,
            name=name,
            class_=associationClass,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )

        Link.__init__(
            self,
            model=model,
            association=associationClass,
            sourceObject=sourceObject,
            targetObject=targetObject,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        # To be fully compatible with superclasses Object and Link
        # link objects have both an attribute class_ and association.
        # A third one is added here for convenience and proper naming.
        # All attributes contains the same reference to the association
        # class.
        self.associationClass=associationClass

        # just make sure that the name of this link object is set.
        # This avoid relying on the implementation of Link constructor.
        # This could be an issue otherwize since link have no name.
        self.name=name
        model._linkObjectNamed[self.name]=self
        print('TT'*10, 'adding object', model._linkObjectNamed)


    # def delete(self):
    #     #TODO:  implement delete operation on link objects
    #     raise NotImplementedError('Delete operation on link object is not implemented')

    def isPlainLink(self):
        return False

    def isPlainObject(self):
        return False