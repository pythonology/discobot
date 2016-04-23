************************************************
Discobot: a fully-featured music bot for Discord
************************************************
|pypi| |python| |license|

===========
Configuring
===========
Before you can run Discobot, you must first create a ``config.yaml`` file. Please refer to the `config.yaml.example <https://github.com/chandler14362/disco/blob/master/config.yaml.example>`_ file for reference.

**NOTE:** If you are going to be running Discobot through Docker, you must leave the values of ``opus_library_path`` and ``redis`` as they are defined in the `config.yaml.example <https://github.com/chandler14362/disco/blob/master/config.yaml.example>`_ file.

=======
Running
=======
There are two ways in which you can run Discobot.

Docker
------
This method is recommended, as it is the quickest, easiest, and most flexible.
::
    docker-compose up

pip
---
This method requires you to first install the following dependencies:

* FFmpeg
* Redis

Now, you may install Discobot through **pip**...
::
    pip install Discobot

...and run it using:
::
    discobot

==========
Change Log
==========
Please see the `CHANGELOG.rst <https://github.com/chandler14362/disco/blob/master/CHANGELOG.rst>`_ file.

=======
Licence
=======
Please see the `LICENSE <https://github.com/chandler14362/disco/blob/master/LICENSE>`_ file.

.. |pypi| image:: https://img.shields.io/pypi/v/Discobot.svg?label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/Discobot
    :alt: Latest version released on PyPi

.. |python| image:: https://img.shields.io/pypi/pyversions/Discobot.svg
    :target: https://pypi.python.org/pypi/Discobot/
    :alt: Supported Python versions

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/chandler14362/disco/master/LICENSE
    :alt: License
