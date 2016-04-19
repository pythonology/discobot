#!/usr/bin/env python3
from setuptools import setup, find_packages

import disco

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read()

setup(
    name='disco',
    version=disco.__version__,
    description=disco.__doc__.strip(),
    long_description=long_description,
    author=disco.__author__,
    maintainer=disco.__maintainer__,
    download_url='https://github.com/chandler14362/disco',
    packages=find_packages(),
    classifiers=[
        'Topic :: Communications :: Chat',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Environment :: No Input/Output (Daemon)',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5'
    ],
    license=disco.__license__,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'disco = disco.__main__:main',
        ],
    }
)
