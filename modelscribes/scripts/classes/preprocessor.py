# coding=utf-8

from modelscribes.base.preprocessors import (
    Preprocessor,
    RegexpTransfo,
    PrefixToCommentTransfo
)

class ClsToUsePreprocessor(Preprocessor):
    def __init__(self):
        super(ClsToUsePreprocessor, self).__init__(
            sourceText='class model',
            targetText='.use class model',
            targetExtension='.use'
        )
        self.addTransfo(RegexpTransfo(
            '^ *class +model (?P<rest>.*)',
            'model {rest}'))

        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)\|(?P<rest>.*)',
            '{before}--|{rest}'))

        self.addTransfo(PrefixToCommentTransfo((
            'package',)))

        #---- datatype ----------------------------------------
        # implementation is more complex:
        # the **preprocessor** should replace the type of attribute
        # by the substitution type. a blank line should
        # be generated here and the type registered.
        self.addTransfo(PrefixToCommentTransfo((
            'datatype',)))


        #---- derived attribute --------------------------------
        #
        self.addTransfo(RegexpTransfo(
            '(?P<before> *)(?P<derived>/ *)(?P<attr>[#~+-]? *\w+ *: *\w+)(?P<rest>.*)',
            '{before}{attr}{rest} --@derived'))
        # / removed now ----------------------------------------


        #---- attribute visibility -----------------------------
        #  +-~# -> @visibility=+-~#
        self.addTransfo((RegexpTransfo(
            '(?P<before> *)(?P<visibility>[#~+-] *)(?P<attr>\w+ *: *\w+)(?P<rest>.*)',
            '{before}{attr}{rest} --@visibility={visibility}')))
        # attribute visibility removed now ---------------------


        #---- optional attribute -------------------------------
        # [0..1] -> @optional
        self.addTransfo(RegexpTransfo(
            '(?P<before> *)(?P<attr>\w+ *: *\w+) *(?P<card>\[ *0 *\.\. *1 *])(?P<rest>.*)',
            '{before}{attr}{rest} --@optional'))
        # [0..1] removed now -----------------------------------


        #---- tagged attribute ---------------------------------
        # {...} -> @optional
        self.addTransfo(RegexpTransfo(
            '(?P<before> *)(?P<attr>\w+ *: *\w+) *(?P<tags>( *\{[^}]*\})+)(?P<rest>.*)',
            #TODO: add a parameter in RegexpTransfo to process groups in the middle
            '{before}{attr}{rest} --@tags={tags}'))
        # {...} removed now -----------------------------------


        # self.addTransfo(RegexpTransfo(
        #     '(?P<before> *)datatype(?P<name> *\w+)(?P<rest>.*)',
        #     '{before}class{name}{rest} --@optional'))

        #  *(?P<derived>/)? *\w+ *: *(?P<type>\w+) *(?P<card>\[ *0 *\.\. *1 *])?