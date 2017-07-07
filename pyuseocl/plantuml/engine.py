import os

class PlantUMLEngine(object):

    def __init__(self, checks=False, format='svg', outputDir='.'):
        self.plantumlJar=os.path.join(os.path.dirname(__file__),'res','plantuml.jar')
        if checks:
            if not os.path.isfile(self.plantumlJar):
                raise EnvironmentError('cannot find '% self.plantumlJar)
            if os.system('java -version') != 0:
                raise EnvironmentError('java is required but it seems that it is not installed')
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
        # TODO: check how to get errors.
        if errno != 0:
            RuntimeError('Error in plantuml generation')