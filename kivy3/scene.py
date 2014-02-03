
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
from kivy.resources import resource_find
from kivy.graphics.opengl import glEnable, glDisable, GL_DEPTH_TEST
from kivy.graphics.fbo import Fbo
from kivy.graphics.transformation import Matrix
from kivy.graphics import Callback, PushMatrix, PopMatrix, \
                          Rectangle, Canvas, UpdateNormalMatrix



from .camera import Camera


class Renderer(Fbo):

    def __init__(self, *args, **kw):
        kw.setdefault('with_depthbuffer', True)
        kw.setdefault('compute_normal_mat', True)
        
        super(Renderer, self).__init__(*args, **kw)
        
        self.cb_before = Callback(self.setup_gl_context)
        self.push_matrix = PushMatrix()
        self.update_matrix = UpdateNormalMatrix() 
        self.pop_matrix = PopMatrix()
        self.cb_after = Callback(self.reset_gl_context)
    
    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        self.clear_buffer()

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
        
    def load_objects(self, objects):
        self.clear()
        self.add(self.cb_before)
        self.add(self.push_matrix)
        self.add(self.update_matrix)
        for obj in objects:
            for i in obj.as_instructions():
                self.add(i)
        self.add(self.pop_matrix)
        self.add(self.cb_after)
    
    def update_glsl(self, *largs):
        asp = self.size[0] / float(self.size[1])
        proj = Matrix().view_clip(-asp*0.1, asp*0.1, -1*0.1, 1*0.1, 1*0.1, 100, 1)
        #proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self['projection_mat'] = proj


class Scene(Widget):
    """ Core class which allows you to use 3D graphics in
    Kivy application.
    
    Parameters:
        camera_cls: Camera by default, but you may use your own class
        clear_color: to make transparent background set value to (0., 0., 0., 0.)
        shader_file: path to your shader file
    """
    
    def __init__(self, camera_cls=Camera, renderer_cls=Renderer, **kw):
        
        self.objects = []
        self.viewport = None # scene viewport
        self.canvas = Canvas()
        
        # get clear color 
        self.clear_color = kw.pop('clear_color', (0., 0., 0., 0.))
        self.shader_file = kw.pop('shader_file', resource_find('default.glsl'))
         
        super(Scene, self).__init__(**kw)
        self.camera = camera_cls(self)
        
        # create FBO where all drawing is going
        with self.canvas:
            self.renderer = renderer_cls(size=self.size, clear_color=self.clear_color)
            self.viewport = Rectangle(size=self.size, pos=self.pos)

        self.renderer.shader.source = self.shader_file
    
    def add(self, *objs):
        """ Add objects to 3D scene """
        for obj in objs:
            self._add_obj(obj)
        self.reload_scene()
    
    def _add_obj(self, obj):
        self.objects.append(obj)
        
    def reload_scene(self):
        self.renderer.load_objects(self.objects)
        
    def on_size(self, instance, value):
        self.renderer.size = value
        self.viewport.texture = self.renderer.texture
        self.viewport.size = value
        self.renderer.update_glsl()
        
    def on_texture(self, instance, value):
        self.viewport.texture = value
    
 