# coding=utf-8


from modelscripts.metamodels import (
    scenarios
)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts import (
    F, E, W, I, H,
    checkAllAssertionsForDirectory,
    checkValidIssues
)

EXPECTED_ISSUES={


    'cl01.scs':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    'cl20.scs':         {F: 0, E: 3, W: 0, I: 0, H: 0},
    'cl21.scs':         {F: 0, E: 3, W: 0, I: 0, H: 0},

    'pe10.scs':         {F: 0, E: 1, W: 0, I: 0, H: 0},

    'us10.scs':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    'us28.scs':         {F: 0, E: 0, W: 0, I: 0, H: 0},
    'us90.scs':         {F: 0, E: 0, W: 0, I: 1, H: 0},

    'empty01.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},
    'empty02.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},

    'no01.scs':         {F: 0, E: 0, W: 0, I: 1, H: 0},
    'no02.scs':         {F: 0, E: 0, W: 0, I: 3, H: 0},

    'ko01.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko02.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko03.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko04.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko05.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko06.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},

    'kosyntax1.scs':    {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax2.scs':    {F: 0, E: 2, W: 0, I: 0, H: 0},
    'kosyntax3.scs':    {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax4.scs':    {F: 1, E: 0, W: 0, I: 0, H: 0},
    'kosyntax7.scs':    {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax8.scs':    {F: 0, E: 2, W: 0, I: 0, H: 0},
    'kosyntax9.scs':    {F: 1, E: 0, W: 0, I: 0, H: 0},
    'kosyntax10.scs':   {F: 1, E: 0, W: 0, I: 0, H: 0},
    'kosyntax11.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax12.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax13.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax14.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax15.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kosyntax16.scs':   {F: 0, E: 4, W: 0, I: 0, H: 0},
    'kosyntax17.scs':   {F: 0, E: 6, W: 0, I: 0, H: 0},
    'kosyntax18.scs':   {F: 0, E: 5, W: 0, I: 0, H: 0},
    'kosyntax19.scs':   {F: 0, E: 4, W: 0, I: 0, H: 0},
    'kosyntax20.scs':   {F: 0, E: 1, W: 0, I: 0, H: 0},

    'koinv01.scs':      {F: 0, E: 1, W: 0, I: 0, H: 0},
    'koinv02.scs':      {F: 0, E: 2, W: 0, I: 0, H: 0},
    'koinv03.scs':      {F: 0, E: 4, W: 0, I: 0, H: 0},
    'koinv04.scs':      {F: 0, E: 12, W: 0, I: 0, H: 0},

    'kocard01.scs':     {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kocard02.scs':     {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kocard03.scs':     {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kocard04.scs':     {F: 0, E: 1, W: 0, I: 0, H: 0},
    'kocard05.scs':     {F: 0, E: 2, W: 0, I: 0, H: 0},
    'kocard06.scs':     {F: 0, E: 5, W: 0, I: 0, H: 0},

    'koquery01.scs':    {F: 0, E: 4, W: 0, I: 0, H: 0},
    'koquery02.scs':    {F: 0, E: 1, W: 0, I: 1, H: 0},
    'koquery03.scs':    {F: 0, E: 0, W: 0, I: 2, H: 0},
    'koquery06.scs':    {F: 0, E: 5, W: 0, I: 0, H: 0},
    'koquery90.scs':    {F: 0, E: 1, W: 0, I: 0, H: 0},

    'query02.scs':      {F: 0, E: 0, W: 0, I: 3, H: 0},
    'query03.scs':      {F: 0, E: 0, W: 0, I: 1, H: 0},
    'query04.scs':      {F: 0, E: 0, W: 0, I: 4, H: 0},
    'query05.scs':      {F: 0, E: 0, W: 0, I: 1, H: 0},
    'query06.scs':      {F: 0, E: 5, W: 0, I: 2, H: 0},

    'kosem1.scs':       {F: 0, E: 2, W: 0, I: 0, H: 0},
    'kosem2.scs':       {F: 1, E: 0, W: 1, I: 0, H: 0},


}


def testGenerator_Issues():
    res = checkAllAssertionsForDirectory(
        'scs',
        ['.scs'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        if file.endswith('.scs'):
            yield (
                checkValidIssues,
                file,
                scenarios.METAMODEL,
                ex)

def testFinalMegamodel():
    MegamodelPrinter().display()

