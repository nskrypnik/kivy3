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
Object3D class
=============


"""

from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import Scale, Rotate, PushMatrix, PopMatrix, Translate, \
                          Mesh
from kivy.event import EventDispatcher

class Object3D(EventDispatcher):
    
    pos = ListProperty([0, 0, 0])
    angle_x = NumericProperty(0.0)
    angle_y = NumericProperty(0.0)
    angle_z = NumericProperty(0.0)
    scale = NumericProperty(1.0)
    
    def __init__(self, **kw):
        
        super(Object3D, self).__init__(**kw)
        self.name = kw.pop('name', '')
        self._pop_matrix = PopMatrix()
        self._push_matrix = PushMatrix()
        self._translate = Translate(*self.pos)        
        self._scale = Scale(self.scale)
        self._rotate_x = Rotate(self.angle_x, 1, 0, 0)
        self._rotate_y = Rotate(self.angle_y, 0, 1, 0)
        self._rotate_z = Rotate(self.angle_y, 0, 0, 1)
        
        mesh_data = kw.pop('mesh', None)
        if mesh_data:
            self.set_mesh(mesh_data)
        else:
            self.mesh = None
        
        self._instructions = None
        
    def on_pos(self, val):
        self._translate.xyz = val
    
    def on_angle_x(self, inst, val):
        self._rotate_x.angle = val
    
    def on_angle_y(self, inst, val):
        self._rotate_y.angle = val

    def on_angle_z(self, inst, val):
        self._rotate_z.angle = val
    
    def on_scale(self, val):
        self._scale.xyz = (val, val, val)
                
    def set_mesh(self, mesh):
        if isinstance(mesh, Mesh):
            self.mesh = mesh
        else:
            # normally it should be RawMeshData
            self.mesh = Mesh(
                vertices=mesh.vertices,
                indices=mesh.indices,
                fmt=mesh.vertex_format,
                mode='triangles',
                #texture=texture,
            )
    
    def as_instructions(self):
        """ Get instructions set for renderer """
        if not self._instructions:
            self._instructions = [self._push_matrix, self._translate, self._rotate_x,
                                  self._rotate_y, self._rotate_z, self.scale, self.mesh]
        return self._instructions

