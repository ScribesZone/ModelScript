# coding=utf-8
"""
This utility module is used to split a line in
multiple segments.
A segment is either regular piece of text or a reference.
The module is only used by the text parser.
"""
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, List, Optional, Tuple
import re

class Segment(object):

    def __init__(self, string, pos):
        self.string=string
        self.pos=pos

class StringSegment(Segment):
    pass

class ReferenceSegment(Segment):

    @property
    def body(self):
        # remove the quote `abc`
        return self.string[1:-1]



def segmentsAndErrors(line):
    # type: (Text) -> Tuple[List[Segment],List[int]]
    regexp=re.compile(r'`\w+`', re.UNICODE)

    def nextSearch(s, start):
        # type: (Text, int)->(Text, Optional[Text], int, int)
        # Return
        # - the string before the match
        # - the string matched or None
        # - the index of the first character of the match or None
        # - the index of the character just after the match or the len of s
        m = regexp.search(s, start)
        if m:
            return(
                s[start:m.start()],
                m.group(0)[1:-1],
                m.start(),
                m.end()
            )
        else:
            return(
                s[start:],
                None,
                None,
                len(s)
            )

    def segment_list(line):
        # type: (Text) ->  List[Segment]
        # Return a list with successive segments
        segments=[] # type:
        nextstart=0
        while True:
            start= nextstart
            (before, token, pos, nextstart) = nextSearch(line, nextstart)
            segments.append(StringSegment(before, start) )
            if token is not None:
                segments.append(
                    ReferenceSegment(token, pos))
            else:
                segments.append(None)
            if nextstart >= len(line):
                break
        # remove last element since it is always None
        # since there the algorithm always ebd with None
        if segments[-1] is None:
            return segments[:-1]
        else:
            return segments


    segments= segment_list(line)
    # now check
    error_positions=[]
    for seg in segments:
        if isinstance(seg, StringSegment):
            pass  # TODO: implement the list of error positions

    return (segments, error_positions)

