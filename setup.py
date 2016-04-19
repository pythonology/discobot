#!/usr/bin/env python3
from setuptools import setup, find_packages

import discobot

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    install_requires = []
    dependency_links = []
    for line in f.read().splitlines():
        if line.startswith('git+'):
            dependency_links.append(line)
        else:
            install_requires.append(line)

setup(
    name='DiscoBot',
    version=discobot.__version__,
    description=discobot.__doc__.strip(),
    long_description=long_description,
    author=discobot.__author__,
    maintainer=discobot.__maintainer__,
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
    license=discobot.__license__,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'discobot = discobot.__main__:main',
        ],
    },
    dependency_links=dependency_links
)
