# coding=utf-8

from modelscribes.base.preprocessors import (
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

        self.addTransfo(RegexpTransfo(
            '^ *! *check *',
            'check -v -d -a' ))

        # Remove the megammodel statement (import, model)
        # These statements are removed during
        # preprocessing since they are not useful after.
        self.addTransfo(RegexpTransfo(
            '^ *(scenario|import|object)', # remove mega
            '' ))

        self.addTransfo(PrefixToCommentTransfo((
            'actor',
            'uci',
            'usecase',
            'end',
            'enduci',
            'context',
            'endcontext')))
