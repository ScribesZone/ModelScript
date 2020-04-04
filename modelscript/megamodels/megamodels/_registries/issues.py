# coding=utf-8
"""issue box registry.
This module provides a unique mixin _IssueBoxRegistry to be
included in the Megamodel class.
"""

__all__=(
    '_IssueBoxRegistry'
)

class _IssueBoxRegistry(object):
    """Part of the megamodel dealing with issueBoxes """

    _issueBoxes = []

    @classmethod
    def registerIssueBox(cls, issueBox):
        cls._issueBoxes.append(issueBox)

    @classmethod
    def issueBoxes(cls):
        return cls._issueBoxes

    @classmethod
    def rootIssueBoxes(cls):
        return [
            ib for ib in cls._issueBoxes
            if len(ib.parents)
        ]