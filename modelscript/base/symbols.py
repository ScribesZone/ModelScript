# coding=utf-8
"""Symbol related helpers.

This include for instance functions that check if a symbol is in CamlCase,
snake_case and soon."""

import re

__all__ = (
    'Symbol',
    'isVerb'
)

class Symbol(object):
    CamlCase = r'^_?[A-Z][A-Za-z0-9]*_?'
    camlCase = r'_?[a-z][A-Za-z0-9]*_?'
    SNAKE_CASE = r'_?[A-Z][A-Z_]*_?'
    snake_case = r'_?[a-z][a-_]*_?'

    @classmethod
    def is_CamlCase(cls, word):
        assert word is not None
        return re.match(r'%s$' % cls.CamlCase, word, re.U)

    @classmethod
    def is_camlCase(cls, word):
        assert word is not None
        return re.match(r'%s$' % cls.camlCase, word, re.U)

    @classmethod
    def is_SNAKE_CASE(cls, word):
        assert word is not None
        return re.match(r'%s$' % cls.SNAKE_CASE, word, re.U)

    @classmethod
    def is_snake_case(cls, word):
        assert word is not None
        return re.match(r'%s$' % cls.snake_case, word, re.U)

def isVerb(word, lang='fr'):
    for terminaison in ['er', 'ir', 'oir', 're']:
        if word.endswith(terminaison):
            return True
    else:
        return False

