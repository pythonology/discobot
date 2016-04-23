************************************************
Discobot: a fully-featured music bot for Discord
************************************************
|license|

===========
Configuring
===========
Before you can run Discobot, you must first create a ``config.yaml`` file. Please refer to the `config.yaml.example <https://github.com/chandler14362/disco/blob/master/config.yaml.example>`_ file for reference.

**NOTE:** In order to run Discobot through Docker, you must leave the values of ``opus_library_path`` and ``redis`` as they are defined in the `config.yaml.example <https://github.com/chandler14362/disco/blob/master/config.yaml.example>`_ file.

=======
Running
=======
Discobot can easily be run through Docker:
::
    docker-compose up

==========
Change Log
==========
Please see the `CHANGELOG.rst <https://github.com/chandler14362/disco/blob/master/CHANGELOG.rst>`_ file.

=======
Licence
=======
Please see the `LICENSE <https://github.com/chandler14362/disco/blob/master/LICENSE>`_ file.

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/chandler14362/disco/master/LICENSE
    :alt: License
