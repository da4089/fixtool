#! /usr/bin/env python3
##################################################################
# fixtool
# Copyright (C) 2017-2018, David Arnold.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
##################################################################

import logging
import os
from .proxy import FixToolProxy


def spawn_agent():
    """Create a new agent, and associated proxy.

    :returns: Reference to proxy, or None on error."""

    # Spawned agents are spawned from the calling process, and usually
    # dedicated to it.  It's possible to contact a spawned agent from
    # an independent process, but that's not the intended use case.
    #
    # When the agent starts, it is allocated an ephemeral port number.
    # That port number is reported on stdout from the process, and
    # can be read by the proxy which subsequently connects to it on
    # that port.
    #
    # The agent can be explicitly shutdown at any time by the proxy,
    # but will also be implicitly killed if the proxy instance is
    # deleted.

    agent = os.popen('fixtool-agent start')
    s = agent.read()
    try:
        port = int(s)
    except ValueError:
        logging.error("Unable to read port number from agent output")
        return

    p = FixToolProxy("localhost", port)
    return p
