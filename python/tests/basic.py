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

import fixtool
import unittest


class BasicTests(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_connect_disconnect(self):
        proxy = fixtool.FixToolProxy("localhost", 11011)
        client = proxy.create_client("c1")
        server = proxy.create_server("s1")
        server.listen(12000)
        self.assertEqual(0, server.pending_accept_count())
        client.connect("localhost", 12000)
        self.assertEqual(1, server.pending_accept_count())
        server_session = server.accept("ss1")
        self.assertTrue(server_session.is_connected())
        self.assertTrue(client.is_connected())

        server_session.disconnect()
        self.assertFalse(server_session.is_connected())


        self.assertFalse(client.is_connected())
        return

