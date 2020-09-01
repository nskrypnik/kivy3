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
Camera module
=============

In this module base camera class is implemented.
"""


__all__ = ('Camera', )

import math

from kivy.properties import NumericProperty, ListProperty, ObjectProperty, \
    AliasProperty
from kivy.graphics.transformation import Matrix
from ..math.vectors import Vector3
from ..core.object3d import Object3D
from math import radians


class Camera(Object3D):
    """
    Base camera class
    """

    scale = NumericProperty(1.0)
    _right = ObjectProperty(Vector3(1, 0, 0))
    _up = ObjectProperty(Vector3(0, 1, 0))
    _back = ObjectProperty(Vector3(0, 0, 1))
    up = ObjectProperty(Vector3(0, 1, 0))

    def __init__(self):
        super(Camera, self).__init__()
        self.projection_matrix = Matrix()
        self.modelview_matrix = Matrix()
        self.model_matrix = Matrix()
        self.viewport_matrix = (0, 0, 0, 0)
        self.renderer = None  # renderer camera is bound to
        self._look_at = None
        self.look_at(Vector3(0, 0, -1))

    def _set_position(self, val):
        super(Camera, self).on_pos_changed(val)
        self.look_at(self._look_at)
        self.update()

    def on_pos_changed(self, coord, v):
        """ Camera position was changed """
        self.look_at(self._look_at)
        self.update()

    def on_up(self, instance, up):
        """ Camera up vector was changed """
        pass

    def on_scale(self, instance, scale):
        """ Handler for change scale parameter event """

    def look_at(self, *v):
        if len(v) == 1:
            v = v[0]
        m = Matrix()
        pos = self._position
        m = m.look_at(pos[0], pos[1], pos[2], v[0], v[1], v[2],
                      self.up[0], self.up[1], self.up[2])
        m = m.rotate(radians(self.rot.x), 1.0, 0.0, 0.0)
        m = m.rotate(radians(self.rot.y), 0.0, 1.0, 0.0)
        m = m.rotate(radians(self.rot.z), 0.0, 0.0, 1.0)
        self.modelview_matrix = m

        # set camera vectors from view matrix
        self._right = Vector3(m[0], m[1], m[2])
        self._up = Vector3(m[4], m[5], m[6])
        self._back = Vector3(m[8], m[9], m[10])
        self._look_at = v
        self.update()

    def bind_to(self, renderer):
        """ Bind this camera to renderer """
        self.renderer = renderer

    def update(self):
        if self.renderer:
            self.viewport_matrix = (
                self.renderer._viewport.pos[0],
                self.renderer._viewport.pos[1],
                self.renderer._viewport.size[0],
                self.renderer._viewport.size[1]
            )
            model_matrix = self.modelview_matrix.multiply(
                self.renderer.fbo['view_mat'].inverse())
            self.model_matrix = model_matrix
            self.renderer._update_matrices()

    def update_projection_matrix(self):
        """ This function should be overridden in the subclasses
        """
