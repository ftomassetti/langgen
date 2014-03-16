from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import sandman

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='namegen',
    version=namegen.__version__,
    url='http://github.com/ftomassetti/namegen/',
    license='Apache Software License',
    author='Federico Tomassetti',
    tests_require=['nose'],
    install_requires=[
                    ],
    author_email='f.tomassetti@gmail.com',
    description='Languages and names generator',
    long_description=long_description,
    packages=['namegen'],
    include_package_data=True,
    platforms='any',
    test_suite='namegen.test.test_namegen',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
        ],
    extras_require={
        'testing': ['nose'],
    }
)