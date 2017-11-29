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
        self._destroyed = False

        msg = ClientCreateMessage(self._name)
        self._proxy.send_request(msg)
        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def destroy(self):
        assert not self._destroyed

        request = ClientDestroyMessage(self._name)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._proxy.remove_client(self._name)
        self._destroyed = True
        return

    def connect(self, host, port):
        assert not self._destroyed

        self._host = host
        self._port = port

        msg = ClientConnectMessage(self._name, self._host, self._port)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def disconnect(self):
        assert not self._destroyed

        self._proxy.send_request({"message": "client_disconnect"})
        return

    def receive_queue_length(self):
        assert not self._destroyed

        self._proxy.send_request({"message": "client_get_queue_length"})
        return 0

    def send_message(self, message):
        assert not self._destroyed

        return

    def is_connected(self):
        assert not self._destroyed

        request = ClientIsConnectedRequest(self._name)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        return response.connected


class ServerSession(object):
    def __init__(self, proxy, name: str):
        self._proxy = proxy
        self._name = name
        self._clients = {}
        self._ports = []
        self._destroyed = False

        msg = ServerCreateMessage(self._name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return

    def destroy(self):
        assert not self._destroyed

        for session in self._clients.values():
            session.destroy()
        self._clients = {}

        for port in self._ports[:]:
            self.unlisten(port)

        assert len(self._clients) == 0
        assert len(self._ports) == 0

        request = ServerDestroyMessage(self._name)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._proxy.remove_server(self._name)
        self._destroyed = True
        return

    def listen(self, port: int):
        assert not self._destroyed

        msg = ServerListenMessage(self._name, port)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._ports.append(port)
        return

    def unlisten(self, port: int):
        assert not self._destroyed

        request = ServerUnlistenMessage(self._name, port)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._ports.remove(port)
        return

    def pending_accept_count(self):
        assert not self._destroyed

        msg = ServerPendingAcceptCountRequest(self._name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)
        return response.count

    def accept(self, new_name: str):
        assert not self._destroyed

        msg = ServerAcceptMessage(self._name, new_name)
        self._proxy.send_request(msg)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        client = ServerClientSession(self, self._proxy, response.session_name)
        self._clients[response.session_name] = client
        return client


class ServerClientSession(object):
    def __init__(self, server, proxy, name):
        self._server = server
        self._proxy = proxy
        self._name = name
        self._connected = True
        return

    def destroy(self):
        if self._connected:
            self.disconnect()
        return

    def is_connected(self):
        request = ServerIsConnectedRequest(self._name)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        return response.connected

    def disconnect(self):
        request = ServerDisconnectMessage(self._name)
        self._proxy.send_request(request)

        response = self._proxy.await_response()
        if not response.result:
            raise RuntimeError(response.message)

        self._connected = False
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

            elif message_type == "client_destroyed":
                message = ClientDestroyedMessage.from_dict(d)

            elif message_type == "client_connected":
                message = ClientConnectedMessage.from_dict(d)

            elif message_type == "client_is_connected_response":
                message = ClientIsConnectedResponse.from_dict(d)

            elif message_type == "server_created":
                message = ServerCreatedMessage.from_dict(d)

            elif message_type == "server_destroyed":
                message = ServerDestroyedMessage.from_dict(d)

            elif message_type == "server_listened":
                message = ServerListenedMessage.from_dict(d)

            elif message_type == "server_unlistened":
                message = ServerUnlistenedMessage.from_dict(d)

            elif message_type == "server_pending_accept_response":
                message = ServerPendingAcceptCountResponse.from_dict(d)

            elif message_type == "server_accepted":
                message = ServerAcceptedMessage.from_dict(d)

            elif message_type == "server_is_connected_response":
                message = ServerIsConnectedResponse.from_dict(d)

            elif message_type == "server_disconnected":
                message = ServerDisconnectedMessage.from_dict(d)

            return message

    def remove_client(self, name):
        del self._clients[name]
        return

    def remove_server(self, name):
        del self._servers[name]
        return

