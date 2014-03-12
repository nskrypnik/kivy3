
import os
import kivy3
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy3 import Mesh, Material
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.extras.geometries import BoxGeometry


class SceneApp(App):

    def build(self):
        root = FloatLayout()

        self.renderer = Renderer()
        scene = Scene()
        geometry = BoxGeometry(0.5, 0.5, 0.5)
        material = Material(color=(0., 1., 0.))
        self.cube = Mesh(geometry, material)
        self.cube.pos.z = -2
        camera = PerspectiveCamera(75, 1, 1, 1000)

        scene.add(self.cube)
        self.renderer.render(scene, camera)

        root.add_widget(self.renderer)
        Clock.schedule_interval(self._rotate_cube, 1 / 20)

        return root

    def _rotate_cube(self, dt):
        self.cube.rotation.x += 1
        self.cube.rotation.y += 1
        self.cube.rotation.z += 1


if __name__ == '__main__':
    SceneApp().run()

