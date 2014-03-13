"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Loader class
=============

Base loader class which should be used by all other loaders implementations
"""


class Loader(object):

    def __init__(self, **kw):
        self._on_load_start = kw.pop("on_load_start", None)
        self._on_load_progress = kw.pop("on_load_progress", None)
        self._on_load_complete = kw.pop("on_load_complete", None)

    @property
    def on_load_start(self):
        return self._on_load_start

    @on_load_start.setter
    def set_on_load_start(self, v):
        if callable(v):
            self._on_load_start = v
        else:
            raise Exception("on_load_start should be callable")

    @property
    def on_load_progress(self):
        return self._on_load_progress

    @on_load_progress.setter
    def set_on_load_progress(self, v):
        if callable(v):
            self._on_load_progress = v
        else:
            raise Exception("on_load_progress should be callable")

    @property
    def on_load_complete(self):
        return self._on_load_complete

    @on_load_progress.setter
    def set_on_load_complete(self, v):
        if callable(v):
            self._on_load_complete = v
        else:
            raise Exception("on_load_complete should be callable")

