************************************************
Discobot: a fully-featured music bot for Discord
************************************************
|release| |requirements| |license|

===========
Configuring
===========
Before you can run Discobot, you must first create a ``config.yaml`` file. Please refer to the `config.yaml.example <https://github.com/pythonology/discobot/blob/master/config.yaml.example>`_ file for reference.

**NOTE:** In order to run Discobot through Docker, you must leave the values of ``opus_library_path`` and ``redis`` as they are defined in the `config.yaml.example <https://github.com/pythonology/discobot/blob/master/config.yaml.example>`_ file.

=======
Running
=======
Discobot can easily be run through Docker:
::
    docker-compose up

==========
Change Log
==========
Please see the `CHANGELOG.rst <https://github.com/pythonology/discobot/blob/master/CHANGELOG.rst>`_ file.

=======
Licence
=======
Please see the `LICENSE <https://github.com/pythonology/discobot/blob/master/LICENSE>`_ file.

.. |release| image:: https://img.shields.io/github/release/pythonology/discobot.svg
    :target: https://github.com/pythonology/discobot/releases/latest
    :alt: Latest Release

.. |requirements| image:: https://img.shields.io/requires/github/pythonology/discobot.svg
    :target: https://requires.io/github/pythonology/discobot/requirements/?branch=master
    :alt: Requirements Status

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/pythonology/discobot/master/LICENSE
    :alt: License
