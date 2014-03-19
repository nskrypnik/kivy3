
import os
import kivy3
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file="../textures/simple.glsl")
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)
        loader = OBJMTLLoader()
        obj = loader.load("../textures/orion.obj", "../textures/orion.mtl")
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -6.

        self.renderer.render(scene, camera)
        self.orion = scene.children[0]

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self,  keyboard, keycode, text, modifiers):
        print keycode


if __name__ == '__main__':
    MainApp().run()
