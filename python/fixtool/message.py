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

import json

__all__ = ["ShutdownMessage",
           "ClientCreateMessage",
           "ClientCreatedMessage",
           "ClientConnectMessage",
           "ClientConnectedMessage",
           "ServerCreateMessage",
           "ServerCreatedMessage",
           "ServerListenMessage",
           "ServerListenedMessage",
           "ServerUnlistenMessage",
           "ServerUnlistenedMessage",
           "ServerPendingAcceptCountRequest",
           "ServerPendingAcceptCountResponse",
           "ServerAcceptMessage",
           "ServerAcceptedMessage",
           "ClientIsConnectedRequest",
           "ClientIsConnectedResponse",
           "ServerIsConnectedRequest",
           "ServerIsConnectedResponse",
           "ServerDisconnectMessage",
           "ServerDisconnectedMessage",
           "ClientDestroyMessage",
           "ClientDestroyedMessage",
           "ServerDestroyMessage",
           "ServerDestroyedMessage",
           "ServerSendMessage",
           "ServerSentMessage",
           "ServerReceiveCountRequest",
           "ServerReceiveCountResponse",
           "ServerReceiveMessage",
           "ServerReceivedMessage"]


class ShutdownMessage:
    def __init__(self):
        self.type = "shutdown"
        return

    def to_json(self):
        return json.dumps({"type": self.type})

    @staticmethod
    def from_dict(d):
        assert d.get("type") == "shutdown"
        return ShutdownMessage()


class ClientCreateMessage:
    def __init__(self, name: str):
        self.type = "client_create"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ClientCreateMessage(d.get("name"))


class ClientCreatedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "client_created"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ClientCreatedMessage(d.get("name"),
                                    d.get("result"),
                                    d.get("message"))


class ClientConnectMessage:
    def __init__(self, name: str, host: str, port: int):
        self.type = "client_connect"
        self.name = name
        self.host = host
        self.port = port
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "host": self.host,
                           "port": self.port})

    @staticmethod
    def from_dict(d):
        return ClientConnectMessage(d.get("name"),
                                    d.get("host"),
                                    d.get("port"))


class ClientConnectedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "client_created"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ClientCreatedMessage(d.get("name"),
                                    d.get("result"),
                                    d.get("message"))


class ServerCreateMessage:
    def __init__(self, name: str):
        self.type = "server_create"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerCreateMessage(d.get("name"))


class ServerCreatedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_created"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerCreatedMessage(d.get("name"),
                                    d.get("result"),
                                    d.get("message"))


class ServerListenMessage:
    def __init__(self, name: str, port: int):
        self.type = "server_listen"
        self.name = name
        self.port = port
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "port": self.port})

    @staticmethod
    def from_dict(d):
        return ServerListenMessage(d.get("name"),
                                   d.get("port"))


class ServerListenedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_listened"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerListenedMessage(d.get("name"),
                                     d.get("result"),
                                     d.get("message"))


class ServerUnlistenMessage:
    def __init__(self, name: str, port: int):
        self.type = "server_unlisten"
        self.name = name
        self.port = port
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "port": self.port})

    @staticmethod
    def from_dict(d):
        return ServerUnlistenMessage(d.get("name"),
                                     d.get("port"))


class ServerUnlistenedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_unlistened"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerUnlistenedMessage(d.get("name"),
                                       d.get("result"),
                                       d.get("message"))


class ServerPendingAcceptCountRequest:
    def __init__(self, name: str):
        self.type = "server_pending_accept_request"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerPendingAcceptCountRequest(d.get("name"))


class ServerPendingAcceptCountResponse:
    def __init__(self, name: str, result: bool, message: str, count: int):
        self.type = "server_pending_accept_response"
        self.name = name
        self.result = result
        self.message = message
        self.count = count
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "count": self.count})

    @staticmethod
    def from_dict(d):
        return ServerPendingAcceptCountResponse(d.get("name"),
                                                d.get("result"),
                                                d.get("message"),
                                                d.get("count"))


class ServerAcceptMessage:
    def __init__(self, name: str, session_name: str):
        self.type = "server_accept"
        self.name = name
        self.session_name = session_name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "session_name": self.session_name})

    @staticmethod
    def from_dict(d):
        return ServerAcceptMessage(d.get("name"),
                                   d.get("session_name"))


class ServerAcceptedMessage:
    def __init__(self, name: str, result: bool, message: str,
                 session_name: str):
        self.type = "server_accepted"
        self.name = name
        self.result = result
        self.message = message
        self.session_name = session_name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "session_name": self.session_name})

    @staticmethod
    def from_dict(d):
        return ServerAcceptedMessage(d.get("name"),
                                     d.get("result"),
                                     d.get("message"),
                                     d.get("session_name"))


class ClientIsConnectedRequest:
    def __init__(self, name: str):
        self.type = "client_is_connected_request"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ClientIsConnectedRequest(d.get("name"))


class ClientIsConnectedResponse:
    def __init__(self, name: str, result: bool, message: str, connected: bool):
        self.type = "client_is_connected_response"
        self.name = name
        self.result = result
        self.message = message
        self.connected = connected
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "connected": self.connected})

    @staticmethod
    def from_dict(d):
        return ClientIsConnectedResponse(d.get("name"),
                                         d.get("result"),
                                         d.get("message"),
                                         d.get("connected"))


class ServerIsConnectedRequest:
    def __init__(self, name: str):
        self.type = "server_is_connected_request"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerIsConnectedRequest(d.get("name"))


class ServerIsConnectedResponse:
    def __init__(self, name: str, result: bool, message: str, connected: bool):
        self.type = "server_is_connected_response"
        self.name = name
        self.result = result
        self.message = message
        self.connected = connected
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "connected": self.connected})

    @staticmethod
    def from_dict(d):
        return ServerIsConnectedResponse(d.get("name"),
                                         d.get("result"),
                                         d.get("message"),
                                         d.get("connected"))


class ServerDisconnectMessage:
    def __init__(self, name: str):
        self.type = "server_disconnect"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerDisconnectMessage(d.get("name"))


class ServerDisconnectedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_disconnected"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerDisconnectedMessage(d.get("name"),
                                         d.get("result"),
                                         d.get("message"))


class ClientDestroyMessage:
    def __init__(self, name: str):
        self.type = "client_destroy"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ClientDestroyMessage(d.get("name"))


class ClientDestroyedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "client_destroyed"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ClientDestroyedMessage(d.get("name"),
                                      d.get("result"),
                                      d.get("message"))


class ServerDestroyMessage:
    def __init__(self, name: str):
        self.type = "server_destroy"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerDestroyMessage(d.get("name"))


class ServerDestroyedMessage:
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_destroyed"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerDestroyedMessage(d.get("name"),
                                      d.get("result"),
                                      d.get("message"))


class ServerSendMessage:
    """Request message be sent from server to client."""
    def __init__(self, name: str, payload: bytes):
        self.type = "server_send"
        self.name = name
        self.payload = payload
        return

    def to_json(self):
        #FIXME: going to have issues here with 3.5 and non-unicode payloads
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "payload": self.payload})

    @staticmethod
    def from_dict(d):
        return ServerSendMessage(d.get("name"),
                                 d.get("payload"))


class ServerSentMessage:
    """Acknowledge message was sent from server to client."""
    def __init__(self, name: str, result: bool, message: str):
        self.type = "server_sent"
        self.name = name
        self.result = result
        self.message = message
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message})

    @staticmethod
    def from_dict(d):
        return ServerSentMessage(d.get("name"),
                                 d.get("result"),
                                 d.get("message"))


class ServerReceiveCountRequest:
    """Request count of server's received messages."""

    def __init__(self, name: str):
        self.type = "server_receive_count_request"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerReceiveCountRequest(d.get("name"))


class ServerReceiveCountResponse:
    """Return count of server's received messages."""

    def __init__(self, name: str, result: bool, message: str, count: int):
        self.type = "server_receive_count_response"
        self.name = name
        self.result = result
        self.message = message
        self.count = count
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "count": self.count})

    @staticmethod
    def from_dict(d):
        return ServerReceiveCountResponse(d.get("name"),
                                          d.get("result"),
                                          d.get("message"),
                                          g.get("count"))


class ServerReceiveMessage:
    """Request message received by server."""

    def __init__(self, name: str):
        self.type = "server_receive"
        self.name = name
        return

    def to_json(self):
        return json.dumps({"type": self.type,
                           "name": self.name})

    @staticmethod
    def from_dict(d):
        return ServerReceiveMessage(d.get("name"))


class ServerReceivedMessage:
    """Deliver message received by server to controler."""

    def __init__(self, name: str, result: bool, message: str, payload: bytes):
        self.type = "server_received"
        self.name = name
        self.result = result
        self.message = message
        self.payload = payload
        return

    def to_json(self):
        #FIXME: going to have issues here with 3.5 and non-unicode payloads
        return json.dumps({"type": self.type,
                           "name": self.name,
                           "result": self.result,
                           "message": self.message,
                           "payload": self.payload})

    @staticmethod
    def from_dict(d):
        return ServerReceivedMessage(d.get("name"),
                                     d.get("result"),
                                     d.get("message"),
                                     d.get("payload"))

