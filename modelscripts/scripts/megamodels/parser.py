# coding=utf-8


from typing import Text, Optional, List
import re
import io

class Import(object):
    def __init__(self, words, path):
        #type: (List[Text], Optional[Text])
        self.words=words #rtpe
        self.path=path

def matchImportExpr(line, prefixRegexp=r' *(--)? *@'):
    #type: (Text) -> Optional[List[Text],Optional[Text]]
    re_import=(
        prefixRegexp
        +'import +(?P<kind>[\w ]+)'
        +r' *model( +(?P<path>[\w\./]+)?)? *$')

    m = re.match(re_import, line)
    if m:
        words=m.group('kind').split()
        path=m.group('path')
        return Import(words,path)
    else:
        return None



def extractImports(fileName):

    def read_file():
        with io.open(fileName,
                     'rU',
                     encoding='utf8') as f:
            lines = list(
                line.rstrip() for line in f.readlines())
        return lines

    _=[]
    for line in read_file():
        imp=matchImportExpr(line)
        if imp is not None:
            _.append(imp)
    return _