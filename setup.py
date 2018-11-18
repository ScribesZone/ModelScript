# coding=utf-8
#
# inspired from http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
from __future__ import print_function
import setuptools
# from setuptools.command.test import test as TestCommand
import io
import os
import sys
import re

name = 'modelscript'

here = os.path.abspath(os.path.dirname(__file__))

def read(file):
    encoding = 'utf-8'
    buf = []
    with io.open(file, encoding=encoding) as f:
            buf.append(f.read())
    return '\n'.join(buf)

def getLongDescription():
    """
    get long description from README.rst
    :return:
    """
    return read('README.rst')

def getVersion():
    """
    get the version by extracting :version: label from CHANGES.txt
    :return:
    """
    version_file = read('CHANGES.rst')
    version_match = re.search(r"^:version: *([^\s]+)",
                                  version_file, re.M)
#    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
#                              version_file, re.M)
    if version_match:

        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def getRequirements():
    """
    get the requirements from 'requirements.txt'
    :return:
    """
    from pip.req import parse_requirements
    #install_requirements = parse_requirements('requirements.txt')
    #requirements = [str(ir.req) for ir in install_requirements]
    return [] #  requirements

setuptools.setup(
    name = name,
    version=getVersion(),
    url='https://github.com/ScribesZone/modelscript/',
    license='MIT',
    author='escribis',
    author_email='someone@somewhere.org',  #TODO: add proper email
    description='A Textual Modeling Environment for learning purposes.',
    long_description=getLongDescription(),
    long_description_content_type='text/x-rst',
    keywords = 'model uml modeling dsl metamodel',

    platforms='any',
    classifiers=[
        'Programming Language::Python:: 2.7',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Natural Language :: French',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    python_requires='>=2.7',
    #------ packages-----------------------------------------------------------
    #
    packages=setuptools.find_packages(),
    # packages=[
    #     'modelscript',
    #     ],

    install_requires=getRequirements(),
    # extras_require={
    #    'testing': ['pytest'],
    # }
    # include_package_data=True,


    #------ tests -------------------------------------------------------------
    test_suite='nose.collector'
)
