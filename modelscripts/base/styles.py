from modelscripts.locallibs.termcolor import colored


class Style(object):
    def __init__(self, c=None, b=None, a=None):
        self.color = c
        self.background = b
        self.attributes = a

    def do(self, text, styled=True):
        if styled:
            return colored(text,
                           color=self.color,
                           on_color=self.background,
                           attrs=self.attributes)
        else:
            return text


class Styles(object):
    bigIssue=Style('red', a=['bold'])
    smallIssue=Style('magenta', a=['bold'])
    bigIssueSummary=Style('red', a=['reversed','bold'])
    smallIssueSummary=Style('magenta', a=['reversed','bold'])

    keyword=Style('blue')
    comment=Style('white')
    highlight=Style('red')
    annotate=Style('yellow')
    s2=Style('green')
    bold=Style(a=['bold'])
    no=Style()
    ko=Style('red')
    ok=Style('green')
    # underline, bold, reverse