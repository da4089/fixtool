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

import socket
import struct

from fixtool.message import *


class ClientSession(object):
    def __init__(self, proxy, name: str):
        self._proxy = proxy
        self._name = name
        self._host = None
        self._port = None
        self._is_connected = False

        msg = ClientCreateMessage(self._name)
        self._proxy.send_request(msg)
        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def connect(self, host, port):
        self._host = host
        self._port = port

        msg = ClientConnectMessage(self._name, self._host, self._port)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._is_connected = True
        return

    def disconnect(self):
        self._proxy.send_request({"message": "client_disconnect"})
        return

    def receive_queue_length(self):
        self._proxy.send_request({"message": "client_get_queue_length"})
        return 0

    def get_message(self):
        if len(self._queue) < 1:
            return RuntimeError()

        msg = self._queue.pop(0)
        return msg

    def send_message(self, message):
        return

    def is_connected(self):
        return self._is_connected


class ServerSession(object):
    def __init__(self, proxy, name: str):
        self._proxy = proxy
        self._name = name
        self._clients = {}

        msg = ServerCreateMessage(self._name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def listen(self, port: int):
        msg = ServerListenMessage(self._name, port)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def pending_accept_count(self):
        msg = ServerPendingAcceptCountRequest(self._name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return response.count

    def accept(self, new_name: str):
        msg = ServerAcceptMessage(self._name, new_name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        client = ServerClientSession(self, response.session_name)
        self._clients[response.session_name] = client
        return client


class ServerClientSession(object):
    def __init__(self, server, name):
        self._server = server
        self._name = name
        self._is_connected = True
        return

    def is_connected(self):
        return self._is_connected

    def disconnect(self):
        self._is_connected = False
        return




class FixToolProxy(object):
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self._clients = {}
        self._servers = {}

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._socket.setblocking(True)

        self._buffer = b''
        return

    def create_client(self, name: str):
        """Create a FIX client."""
        client = ClientSession(self, name)
        self._clients[name] = client
        return client

    def create_server(self, name: str):
        """Create a FIX server."""
        server = ServerSession(self, name)
        self._servers[name] = server
        return server

    def send_request(self, message):
        payload = message.to_json().encode('UTF-8')
        payload_length = len(payload)
        header = struct.pack(">L", payload_length)
        self._socket.sendall(header + payload)
        return

    def await_response(self):
        while True:
            buf = self._socket.recv(65536)
            if len(buf) == 0:
                # Disconnected.
                return None

            self._buffer += buf
            if len(self._buffer) <= 4:
                continue

            message_length = struct.unpack(">L", self._buffer[:4])[0]
            self._buffer = self._buffer[4:]
            if len(self._buffer) < message_length:
                continue

            message_buf = self._buffer[:message_length]
            self._buffer = self._buffer[message_length:]

            d = json.loads(message_buf)
            message = None
            message_type = d.get("type")
            if message_type == "client_created":
                message = ClientCreatedMessage.from_dict(d)

            elif message_type == "client_connected":
                message = ClientConnectedMessage.from_dict(d)

            elif message_type == "server_created":
                message = ServerCreatedMessage.from_dict(d)

            elif message_type == "server_listened":
                message = ServerListenedMessage.from_dict(d)

            elif message_type == "server_pending_accept_response":
                message = ServerPendingAcceptCountResponse.from_dict(d)

            elif message_type == "server_accepted":
                message = ServerAcceptedMessage.from_dict(d)

            return message
