fixtool


* Server
  * Listens for requests from clients
    * JSON+TCP?
    * JSON+WS?
    * GPB+TCP?
    * ???
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

