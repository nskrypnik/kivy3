"""
The MIT License (MIT)

Copyright (c) 2014 Niko Skrypnik

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

import os
import kivy3
from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer()

        scene = Scene()
        # load obj file
        loader = OBJLoader()
        obj = loader.load("monkey.obj")
        scene.add(*obj.children)
        camera = PerspectiveCamera(90, 0.3, 1, 1000)

        self.renderer.render(scene, camera)
        root.add_widget(self.renderer)
        Clock.schedule_interval(self._update_obj, 1./20)
        return root

    def _update_obj(self, dt):
        obj = self.scene.children[0]
        if obj.pos.z > -3:
            obj.pos.z -= 0.1


if __name__ == '__main__':
    MainApp().run()
