from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from modelscripts.metamodels.classes.associations import opposite
from modelscripts.metamodels.objects import PackagableElement, Entity
from modelscripts.base.exceptions import (
    UnexpectedCase,
    MethodToBeDefined)
class Link(PackagableElement, Entity):
    __metaclass__ = ABCMeta

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[Package], Optional['Step'],Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        PackagableElement.__init__(
            self,
            model=model,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        Entity.__init__(self)


        self.association=association
        #type: association

        self.sourceObject = sourceObject
        # type: Object

        self.targetObject = targetObject
        # type: Object

        # Singleton-like link roles to allow direct comparison
        # of link role instances. (see linkRole method)
        self._linkRole=OrderedDict()
        self._linkRole['source']=LinkRole(self, 'source')
        self._linkRole['target']=LinkRole(self, 'target')

    @abstractmethod
    def isPlainLink(self):
        # just used to prevent creating object of this class
        # (ABCMeta is not enough)
        raise MethodToBeDefined( #raise:OK
            'method isPlainLink() is not defined.'
        )

    def object(self, position):
        #type: () -> RolePosition
        if position=='source':
            return self.sourceObject
        elif position=='target':
            return self.targetObject
        else:
            raise UnexpectedCase( #raise:OK
                'role position "%s" is not implemented' % position)

    def linkRole(self, position):
        return self._linkRole[position]

    def __str__(self):
        return '(%s,%s,%s)' % (
            self.sourceObject.name,
            self.association.name,
            self.targetObject.name
        )


class LinkRole(object):

    def __init__(self, link, position):
        self.link=link
        self.position=position

    @property
    def object(self):
        return self.link.object(self.position)

    @property
    def association(self):
        return self.link.association

    @property
    def role(self):
        return self.link.association.role(self.position)

    @property
    def roleType(self):
        return self.role.type

    @property
    def objectType(self):
        return self.object.class_

    @property
    def opposite(self):
        return self.link.linkRole(opposite(self.position))

    def __str__(self):
        if self.position=='source':
            return '([[%s]],%s,%s)' % (
                self.link.sourceObject.name,
                self.association.name,
                self.link.targetObject.name
            )
        elif self.position=='target':
            return '(%s,%s,[[%s]])' % (
                self.link.sourceObject.name,
                self.association.name,
                self.link.targetObject.name
            )
        else:
            raise UnexpectedCase( #raise:OK
                'Unexpected position: %s' % self.position)


class PlainLink(Link):

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[Package], Optional['Step'], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(PlainLink, self).__init__(
            model=model,
            association=association,
            sourceObject=sourceObject,
            targetObject=targetObject,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        model._plainLinks.append(self)


    def isPlainLink(self):
        return True

    # def delete(self):
    #     self.state.links=[l for l in self.state.links if l != self]