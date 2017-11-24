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

"""Background agent that manages the fixtool sessions."""

# The client to agent protocol uses TCP, with a simple 32-bit big-endian
# length frame, and then JSON to encode messages.
#
# Any number of fixtool clients can connect to the agent simultaneously.
# This is no significant security implemented.
#
# Initially, at least, the agent will be invisible.  It might make sense
# to add a web UI later, as an alternative controller (via WebSockets).
#
# Requests:
# - login
# - ping
# - logout
# - restart
# - shutdown
# - status

# - create_client
# - connect_client
# - disconnect_client

# - create_server
# - listen_for_connections
# - check_for_connections
# - accept_connection
# - disconnect_connection

# - send_message
# - check_for_messages
# - wait_for_message


import asyncio
import fixtool
import logging
import os
import simplefix
import signal
import socket
import struct
import sys
import ujson


class Server:
    def __init__(self):
        """Constructor."""
        self._begin_string = b''
        self._comp_id = b''
        self._auto_heartbeat = True
        self._auto_sequence = True
        self._raw = False
        self._next_send_sequence = 0
        self._last_seen_sequence = 0

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(False)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

        self._pending_sessions = []
        self._accepted_sessions = {}
        return

    def is_raw(self):
        """Is this server configured in 'raw' mode?"""
        return self._raw

    def listen(self, port):
        """Listen for client connections.

        :param port: TCP port number to listen on."""
        self._socket.bind(('', port))
        self._socket.listen(5)

        asyncio.get_event_loop().add_reader(self._socket, self.acceptable)
        return

    def acceptable(self):
        """Handle readable event on listening socket."""
        sock, _ = asyncio.get_event_loop().sock_accept(self._socket)
        session = ServerSession(self, sock)
        self._pending_sessions.append(session)
        return

    def pending_client_count(self):
        """Return number of pending client sessions."""
        return len(self._pending_sessions)

    def accept_client_session(self, name:str):
        """Accept a pending client session.

        :param name: Name for client session."""

        if self.pending_client_count() < 1:
            return None

        client = self._pending_sessions.pop(0)
        self._accepted_sessions[name] = client
        return client


class ServerSession:
    def __init__(self, server:Server, sock:socket.socket):
        """Constructor.

        :param server: Server instance that owns this session.
        :param sock: ephemeral sock for this session."""
        self._server = server
        self._socket = sock
        self._parser = simplefix.FixParser()
        self._is_closed = False
        self._queue = []

        asyncio.get_event_loop().add_reader(sock, self.readable)
        return

    def readable(self):
        """Handle readable event on session's socket."""
        buf = self._socket.recv(65536)
        if len(buf) == 0:
            self._is_closed = True
            return

        self._parser.append_buffer(buf)
        msg = self._parser.get_message()
        while msg is not None:
            self._queue.append(msg)
            msg = self._parser.get_message()
        return

    def is_closed(self):
        """Return True if session is closed."""
        return self._is_closed

    def close(self):
        """Close this session."""
        self._is_closed = True
        self._socket.close()
        return

    def receive_queue_length(self):
        """Return the number of messages on the received message queue."""
        return len(self._queue)

    def get_message(self):
        """Return the first message from the received message queue."""
        if self.receive_queue_length() < 1:
            return None
        return self._queue.pop(0)

    def send_message(self, message:simplefix.FixMessage):
        """Send a message to the connected client."""
        buffer = message.encode()
        self._socket.sendall(buffer)
        asyncio.get_event_loop().sock_sendall(buffer)
        return


class ControlSession:
    def __init__(self, sock):
        self._socket = sock
        self._buffer = b''
        return

    def append_bytes(self, buffer:bytes):
        self._buffer += buffer
        if len(self._buffer) <= 4:
            # No payload yet
            return

        message_length = struct.unpack(b'>L', self._buffer[:4])[0]
        if len(buffer) < message_length:
            # Not received full message yet
            return

        payload = self._buffer[4:message_length]
        self._buffer = self._buffer[message_length:]

        return payload

    def close(self):
        self._socket.close()
        return


class FixToolAgent(object):
    """ """

    def __init__(self):
        """Constructor."""
        self._port = 11011
        self._socket = None
        self._loop = None

        self._control_sessions = {}
        self._clients = {}
        self._servers = {}

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setblocking(False)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(('0.0.0.0', self._port))
        self._socket.listen(5)

        self._loop = asyncio.get_event_loop()
        self._loop.add_reader(self._socket, self.accept)
        return

    def run(self):
        """Enter mainloop."""
        self._loop.run_forever()
        return

    def stop(self):
        """Exit mainloop."""
        self._loop.stop()
        return

    def accept(self):
        """Accept a new control client connection."""
        sock, _ = self._socket.accept()
        self._loop.add_reader(sock, self.readable, sock)
        self._control_sessions[sock] = ControlSession(sock)
        return

    def readable(self, sock):
        """Handle readable event on a control client socket."""
        control_session = self._control_sessions[sock]
        buf = sock.recv(65536)
        if len(buf) == 0:
            del self._control_sessions[sock]
            control_session.close()
            return

        payload = control_session.append_bytes(buf)
        while payload is not None:
            message = ujson.loads(payload)
            self.handle_request(control_session, message)
            payload = None  # FIXME: deal with multiple messages
        return

    def handle_request(self, client, message):
        """Process a received message."""

        # FIXME: framing?  streaming JSON?
        # FIXME: define protocol
        print(message)

        message_type = message["message"]
        if message_type == "client_create":
            return

        elif message_type == "server_create":
            return self.handle_server_create(client, message)

        elif message_type == "server_listen":
            return

        elif message_type == "server_accept":
            return

        elif message_type == "server_queue_length":
            return

        elif message_type == "server_get_message":
            return

        elif message_type == "server_send_message":
            return

        else:
            return


    def handle_client_create(self):
        return

    def handle_server_create(self, client, message):
        name = message["name"]
        if name in self._servers:
            self.send_error(message, "Server '%s' already exists" % name)
            return

        return

    def send_error(self, request, error):
        self.send_response(request,
                           {"message": "",
                            "result": False,
                            "error": error})
        return

    def send_response(self, request, response):
        return



def main():
    """Main function for agent."""

    # FIXME: use logging, but write to stdout for systemd.
    # FIXME: use similar requests as rnps FIX module?
    # FIXME: use asyncio?  cjson over TCP?
    # FIXME: use type annotations?

    # FIXME: replace all this pidfile malarky with a shutdown to a port number
    pid_file_name = "/tmp/%s-fixtool-agent.pid" % os.environ.get("LOGNAME")

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "shutdown":
            pid_file = open(pid_file_name)
            pid = int(pid_file.readline())
            os.kill(pid, signal.SIGINT)
            sys.exit(0)

    pid_file = open(pid_file_name, "wb")
    pid_file.write(b"%u\n" % os.getpid())
    pid_file.close()

    try:
        agent = FixToolAgent()
        agent.run()
    finally:
        os.remove(pid_file_name)

    return


if __name__ == "__main__":
    main()


##################################################################
