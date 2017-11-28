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

import json


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
    def __init__(self, name: str, result: bool, message: str, session_name: str):
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
