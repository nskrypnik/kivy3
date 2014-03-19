
import os
import kivy3
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy3 import Scene, Renderer, PerspectiveCamera, Vector3
from kivy3.loaders import OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout


class MainApp(App):

    def build(self):
        self.look_at = Vector3(0, 0, -1)
        root = FloatLayout()
        self.renderer = Renderer(shader_file="../textures/simple.glsl")
        scene = Scene()
        self.camera = PerspectiveCamera(15, 1, 1, 1000)
        loader = OBJMTLLoader()
        obj = loader.load("../textures/orion.obj", "../textures/orion.mtl")
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -6.

        self.renderer.render(scene, self.camera)
        self.orion = scene.children[0]

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        Clock.schedule_interval(self._rotate_obj, 1 / 20)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self,  keyboard, keycode, text, modifiers):
        if  keycode[1] == 'w':
            self.camera.pos.z += 0.02
        elif keycode[1] == 's':
            self.camera.pos.z -= 0.02
        elif keycode[1] == 'a':
            self.camera.pos.x -= 0.02
        elif keycode[1] == 'd':
            self.camera.pos.x += 0.02

        elif keycode[1] == 'up':
            self.look_at.y += 0.02
        elif keycode[1] == 'down':
            self.look_at.y -= 0.02
        elif keycode[1] == 'right':
            self.look_at.x += 0.02
        elif keycode[1] == 'left':
            self.look_at.x -= 0.02

        print keycode, self.look_at
        self.camera.look_at(self.look_at)

    def _rotate_obj(self, dt):
        self.orion.rot.x += 2
        self.orion.rot.z += 2


if __name__ == '__main__':
    MainApp().run()
