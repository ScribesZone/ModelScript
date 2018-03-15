# coding=utf-8

from modelscripts.base.preprocessors import (
    Preprocessor,
    RegexpTransfo,
    PrefixToCommentTransfo
)

__all__=(
    'ScsToSoilPreprocessor',
)


class ScsToSoilPreprocessor(Preprocessor):
    def __init__(self):
        super(ScsToSoilPreprocessor, self).__init__(
            sourceText='scenario model',
            targetText='.soil scenario model',
            targetExtension='.soil'
        )

        #---- scenario begin ----------------------------
        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)scenario +begin *$',
            '{before}--@scenariobegin'))

        #---- scenario end ----------------------------
        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)scenario +end *$',
            '{before}check -v -d -a'))

        #---- block ends ---------------------------------
        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)end *$',
            '{before}check -a -d -v'))


        #---- description lines --------------------------
        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)\|(?P<rest>.*)',
            '{before}--|{rest}'))

        self.addTransfo(RegexpTransfo(
            '^ *\? *check *',
            'check -v -a -d' ))

        #---- assert queries -----------------------------
        self.addTransfo(RegexpTransfo(
            '^(?P<before> *)assert *(?P<expr>.*)',
            '{before}?? {expr} --@assertquery'))

        #---- megastatements -----------------------------
        # Remove the megammodel statement (import, model)
        # These statements are removed during
        # preprocessing since they are not useful after.
        self.addTransfo(RegexpTransfo(
            '^ *(scenario|import|object)', # remove mega
            '' ))


        # self.addTransfo(RegexpTransfo(
        #     '^(?P<before> *)enduci(?P<rest>.*)',
        #     '{before}check -v -d -a --@enduci{rest}'))
        #
        # self.addTransfo(RegexpTransfo(
        #     '^(?P<before> *)endcontext(?P<rest>.*)',
        #     '{before}check -v -d -a --@endcontext{rest}'))

        self.addTransfo(PrefixToCommentTransfo((
            'actori',
            'systemi',
            'usecasei',
            'context')))
