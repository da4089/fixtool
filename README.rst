
=======
fixtool
=======

|  |Build Status|  |Docs|  |Code Health|  |Coverage|  |PyPI|  |Python|

Introduction
============

fixtool


* Server
  * Listens for requests from clients
    * TCP + 32-bit length + JSON
  * Establishes FIX sessions
    * Client (initiator)
    * Server (responder)
  * All subsequent behaviour is driven by client program
    * Much like robot-nps, without the RobotFramework.
* Python client
  * Intended to integrate with unittest, tox, etc.
  * Standard OO API library
* Java client
  * Designed for writing tests using standard Java unit test framework
* DotNET client
  * Designed for writing tests using standard (?) .NET unit test framework
* CLI client
  * Can be driven from shell, for scripting tests in bash, etc.


Contributing
============

Comments, suggestions, bug reports, bug fixes -- all contributions to
this project are welcomed.  See the project's `GitHub
<https://github.com/da4089/fixtool>`_ page for access to the latest
source code, and please open an `issue
<https://github.com/da4089/fixtool/issues>`_ for comments,
suggestions, and bugs.



.. |Build Status| image:: https://travis-ci.org/da4089/fixtool.svg?branch=master
    :target: https://travis-ci.org/da4089/fixtool
    :alt: Build status
.. |Docs| image:: https://readthedocs.org/projects/fixtool/badge/?version=latest
    :target: http://fixtool.readthedocs.io/en/latest/
    :alt: Docs
.. |Code Health| image:: https://landscape.io/github/da4089/fixtool/master/landscape.svg?style=flat
    :target: https://landscape.io/github/da4089/fixtool/master
    :alt: Code Health
.. |Coverage| image:: https://coveralls.io/repos/github/da4089/fixtool/badge.svg?branch=master
    :target: https://coveralls.io/github/da4089/fixtool?branch=master
    :alt: Coverage
.. |PyPI| image:: https://img.shields.io/pypi/v/fixtool.svg
    :target: https://pypi.python.org/pypi/fixtool
    :alt: PyPI
.. |Python| image:: https://img.shields.io/pypi/pyversions/fixtool.svg
    :target: https://pypi.python.org/pypi/fixtool
    :alt: Python
