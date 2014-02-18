
import os
import kivy3
from kivy.app import App
from kivy.floatlayout import FloatLayout
from kivy3 import Scene, Renderer, PerspectiveCamera


class SceneApp(App):

    def build(self):
        root = FloatLayout()

        renderer = Renderer()
        scene = Scene()
        camera = PerspectiveCamera(75, 1, 1, 1000)

        renderer.render(scene, camera)

        root.add_widget(renderer)

if __name__ == '__main__':
    SceneApp().run()

