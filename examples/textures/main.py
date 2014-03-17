
import os
import kivy3
from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer(shader_file="simple.glsl")
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)
        loader = OBJMTLLoader()
        obj = loader.load("orion.obj", "orion.mtl")

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -4.

        self.renderer.render(scene, camera)

        root.add_widget(self.renderer)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    MainApp().run()
