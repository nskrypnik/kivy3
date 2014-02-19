
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

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.fbo import Fbo
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics import Callback, PushMatrix, PopMatrix, \
                          Rectangle, Canvas, UpdateNormalMatrix


class Renderer(Widget):

    def __init__(self):
        self.canvas = Canvas()
        with self.canvas:
            self._viewport = Rectangle(size=self.size, pos=self.pos)
        self.camera = None
        self.scene = None
        self._create_fbo()

    def _create_fbo(self):
        self.fbo = Fbo(with_depthbuffer=True, compute_normal_mat=True)
        with self.fbo:
            Callback(self._setup_gl_context())
            PushMatrix()
            UpdateNormalMatrix()
            # instructions set for all instructions
            self._instructions = InstructionGroup()
            PopMatrix()
            Callback(self._reset_gl_context())

    def _setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        self.clear_buffer()

    def _reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def render(self, scene, camera):
        pass

    def on_size(self, instance, value):
        self.fbo.size = value
        self.viewport.texture = self.renderer.texture
        self.viewport.size = value
        self.fbo.update_glsl()

    def on_texture(self, instance, value):
        self.viewport.texture = value
