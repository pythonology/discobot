#!/usr/bin/env python3
import re

from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

    # install_requires cannot contain VCS links, which we use to get
    # discord.py>=0.10.0. Once this version becomes available on PyPi,
    # we can remove the following lines.
    for install_require in install_requires[:]:
        if install_require.startswith('git+'):
            install_requires.remove(install_require)

with open('discobot/__init__.py') as f:
    data = f.read()
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        data, re.MULTILINE).group(1)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]',
                       data, re.MULTILINE).group(1)
    maintainer = re.search(r'^__maintainer__\s*=\s*[\'"]([^\'"]*)[\'"]',
                           data, re.MULTILINE).group(1)
    license = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        data, re.MULTILINE).group(1)

setup(
    name='Discobot',
    version=version,
    description='A fully-featured music bot for Discord.',
    long_description=long_description,
    author=author,
    maintainer=maintainer,
    url='https://github.com/chandler14362/disco',
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
    license=license,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'discobot = discobot.__main__:main'
        ]
    }
)
