#! /usr/bin/env python3
##################################################################
# fixtool
# Copyright (C) 2017, David Arnold.
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

import asyncio
import fixtool
import socket


class ClientSession(object):
    def __init__(self, proxy):
        self._proxy = proxy
        self._host = None
        self._port = None
        self._client_id = None

        self._proxy.send_request({"message": "create_client"})
        return

    def connect(self, host, port):
        self._host = host
        self._port = port

        self._proxy.send_request({"message": "connect_client"})
        return

    def disconnect(self):
        self._proxy.send_request({"message": "disconnect_client"})
        return

    def receive_queue_length(self):
        self._proxy.send_request({"message": "get_client_queue_length"})
        return 0

    def get_message(self):
        if len(self._queue) < 1:
            return RuntimeError()

        msg = self._queue.pop(0)
        return msg

    def send_message(self, message):
        return


class ServerSession(object):
    def __init__(self, proxy):
        self._proxy = proxy
        self._queue = []
        return

    def listen(self, port):
        return

    def pending_client_count(self):
        return len(self._queue)

    def get_message(self):
        if len(self._queue) < 1:
            raise RuntimeError()

        msg = self._queue.pop(0)
        return msg


class ServerSessionClient(object):
    def __init__(self, server):
        self._server = server
        return


class Responder(object):
    def __init__(self):
        return



class FixToolProxy(object):
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._clients = []
        self._servers = []

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.setblocking(False)

        return

    def create_client(self):
        """Create a FIX client."""
        client = ClientSession(self)
        self._clients.append(client)
        return client

    def create_server(self):
        """Create a FIX server."""
        server = ServerSession(self)
        self._servers.append(server)
        return server

    def send_request(self, message):
        return

    def wait_for_response(self):
        return

