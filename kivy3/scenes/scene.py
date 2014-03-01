
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

from kivy.graphics import Callback, UpdateNormalMatrix
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy3 import Object3D


class Scene(Object3D):

    def as_instructions(self):
        if not self._instructions.children:
            super(Scene, self).as_instructions()
            self._instructions.insert(0, Callback(self.setup_gl_context))
            self._nstructions.add(Callback(self.reset_gl_context))
        return self._instructions

    def custom_instructions(self):
        return [UpdateNormalMatrix(), ]

    def setup_gl_context(self, *args):
        #clear_buffer
        glEnable(GL_DEPTH_TEST)
        self.fbo.clear_buffer()
        #glDepthMask(GL_FALSE);

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
