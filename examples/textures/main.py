
import os
import kivy3
from kivy.app import App
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJMTLLoader
from kivy.uix.floatlayout import FloatLayout


class MainApp(App):

    def build(self):
        root = FloatLayout()
        self.renderer = Renderer()
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)
        loader = OBJMTLLoader()
        obj = loader.load("orion.obj", "orion.mtl")

        scene.add(*obj.children)
        for obj in scene.children:
            obj.pos.z = -10.
            obj.rotation.z = 90

        #scene.children[0].material.color = .7, .7, .0
        #scene.children[0].material.diffuse = .7, .7, .0
        #scene.children[0].material.specular = .35, .35, .35

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
