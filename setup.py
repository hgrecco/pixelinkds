#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

try:
    reload(sys).setdefaultencoding("UTF-8")
except:
    pass

try:
    from setuptools import setup
except ImportError:
    print('Please install or upgrade setuptools or pip to continue')
    sys.exit(1)

if sys.version_info < (3, 3):
   print('PixeLINKds requires Python 3.3+')
   sys.exit(1)

import codecs


def read(filename):
    return codecs.open(filename, encoding='utf-8').read()


long_description = '\n\n'.join([read('README'),
                                read('AUTHORS'),
                                read('CHANGES')])

__doc__ = long_description

setup(
    name='pixelinkds',
    version='0.1.dev0',
    description='PixeLINK Data Steam (PDS) Files in Python.',
    long_description=long_description,
    keywords='PixeLINK Data Stream PDS image movie',
    author='Hernan E. Grecco',
    author_email='hernan.grecco@gmail.com',
    url='https://github.com/hgrecco/pixelinkds',
    #test_suite='pint.testsuite.testsuite',
    zip_safe=True,
    packages=['pixelinkds'],
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ])
