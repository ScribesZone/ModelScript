# coding=utf-8

import os

PLANTUML_JAR_FILE='plantuml.1.2018.2.jar'

class PlantUMLEngine(object):

    def __init__(self, checks=False, format='svg', outputDir='.'):
        self.plantumlJar=os.path.join(
            os.path.dirname(__file__),'res',PLANTUML_JAR_FILE)
        if checks:
            if not os.path.isfile(self.plantumlJar):
                raise EnvironmentError('cannot find %s'% self.plantumlJar)
            if os.system('java -version') != 0:
                raise EnvironmentError(
                    'java is required but it seems that it is not installed')
        self.defaultFormat=format
        self.defaultOutputDir=outputDir

    def generate(self, pumlFile, format=None, outputDir=None):
        format=self.defaultFormat if format is None else format
        outputDir=self.defaultOutputDir if outputDir is None else outputDir
        cmd='java -jar %s %s -t%s -o %s' % (
            self.plantumlJar,
            pumlFile,
            format,
            outputDir
        )
        errno=os.system(cmd)
        # TODO: check how to get errors from generation
        if errno != 0:
            RuntimeError('Error in plantuml generation')

if __name__ == "__main__":
    import sys
    engine=PlantUMLEngine()
    engine.generate(sys.argv[1])