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
Camera class
=============

This is the implementation of Camera abstraction, which represents
camera object in the 3D space
"""


__all__ = ('Camera', )

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ListProperty, ObjectProperty
from .math.vectors import Vector3


class Camera(EventDispatcher):

    position = ObjectProperty(Vector3(0, 0, 0))
    scale = NumericProperty(1.0)
    up = ObjectProperty(Vector3(0, 0, 0))

    def __init__(self):
        super(Camera, self).__init__()

    def on_position(self, instance, pos):
        """ Camera position was changed """

    def on_scale(self, instance, scale):
        """ Handler for change scale parameter event """

    def look_at(self):
        pass


class OrthographicCamera():

    pass


class PerspectiveCamera(Camera):

    def __init__(self, fov, aspect, near, far):

        super(PerspectiveCamera, self).__init__()
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far

        self.update_projection_matrix()

    def update_projection_matrix(self):
        pass
