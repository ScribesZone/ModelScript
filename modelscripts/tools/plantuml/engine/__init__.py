# coding=utf-8

import os

__all__=(
    'PlantUMLEngine',
    'PlantUMLError',
    'PlantUMLInstallationError',
    'PlantUMLExecutionError'
)

PLANTUML_JAR_FILE='plantuml.1.2018.2.jar'

class PlantUMLError(Exception):
    pass


class PlantUMLInstallationError(PlantUMLError):
    pass


class PlantUMLExecutionError(PlantUMLError):
    pass


class PlantUMLEngine(object):

    def __init__(self, checks=False, format='svg', outputDir='.'):
        self.plantumlJar=os.path.join(
            os.path.dirname(__file__),'res',PLANTUML_JAR_FILE)
        if checks:
            if not os.path.isfile(self.plantumlJar):
                raise PlantUMLInstallationError( #raise:TODO:3
                    'cannot find %s'% self.plantumlJar)
            if os.system('java -version') != 0:
                raise PlantUMLInstallationError( #raise:TODO:3
                    'java is required but it seems that it is not installed')
        self.defaultFormat=format
        self.defaultOutputDir=outputDir

    def generate(self, pumlFile, format=None, finalOutputDir=None):

        def rename_output_file(outputdir, format, file):
            """
            Rename something like
                /outputdir/file.png
            into
                /outputdir/file.puml.png
            """
            print('FF'*10, 'file', outputdir)
            print('FF'*10, 'ouputdir', outputdir)

            abs_outputdir=os.path.abspath(
                os.path.join(
                    os.path.dirname(file),
                    outputdir))
            print('FF'*10, 'abs_outputdir', outputdir)
            base_file=os.path.splitext(
                os.path.basename(file))[0]
            generated_file_name=os.path.join(
                abs_outputdir,
                base_file+'.'+format)
            new_file_name=os.path.join(
                abs_outputdir,
                base_file+'.puml.'+ format
            )
            print('FF'*10, generated_file_name)
            assert os.path.isfile(generated_file_name)
            os.rename(generated_file_name, new_file_name)

        format=self.defaultFormat if format is None else format
        outputDir=(
            self.defaultOutputDir if finalOutputDir is None
            else finalOutputDir)

        cmd='java -jar %s %s -t%s -o %s' % (
            self.plantumlJar,
            pumlFile,
            format,
            outputDir
        )
        errno=os.system(cmd)
        print('FF' * 10, 'outputDir',outputDir)

        # TODO:3 check how to get errors from generation
        if errno != 0:
            PlantUMLExecutionError( #raise:TODO:3
                'Error in plantuml generation')
        rename_output_file(outputDir, format, pumlFile)


if __name__ == "__main__":
    import sys
    engine=PlantUMLEngine()
    engine.generate(sys.argv[1])