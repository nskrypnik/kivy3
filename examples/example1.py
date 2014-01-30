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
from kivy3 import Scene
from kivy3.loaders import WaveLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Translate 

class MainApp(App):
    
    def build(self):
        root = FloatLayout()
        scene = Scene(shader_file="simple.glsl")
        # load obj file
        loader = WaveLoader()
        obj_path = os.path.join(os.path.dirname(kivy3.__file__), "tests/testnurbs.obj")
        objects = loader.load(obj_path)
        scene.add(*objects)
        scene.renderer.before.add(Translate(0, 0, -5))
        root.add_widget(scene)
        return root


if __name__ == '__main__':
    MainApp().run()
