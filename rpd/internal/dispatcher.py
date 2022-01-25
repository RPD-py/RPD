# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""
Dispatches raw OpCode events to Event classes.
"""

import logging

from rpd.state import ConnectionState

_log = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self):
        self.listeners = {}
        self.state = ConnectionState()

    def dispatch(self, op: int, *args) -> None:
        """Dispatch an OpCode event."""
        _log.debug("Dispatching Op: %s", op)

        for listener in self.listeners[op]:
            self.state.loop.create_task(listener(*args))
