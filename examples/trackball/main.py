
import os
import kivy3
from kivy.app import App
from kivy.clock import Clock
from kivy3 import Scene, Renderer, PerspectiveCamera
from kivy3.loaders import OBJLoader
from kivy.uix.floatlayout import FloatLayout


class ObjectTrackball(FloatLayout):

    def __init__(self, *args, **kw):
        super(ObjectTrackball, self).__init__(*args, **kw)
        self.obj3d = None
        self._touches = []

    def set_object(self, obj3d):
        self.obj3d = obj3d

    def define_rotate_angle(self, touch):
        x_angle = (touch.dx / self.width) * 360
        y_angle = -1 * (touch.dy / self.height) * 360
        return x_angle, y_angle

    def on_touch_down(self, touch):
        touch.grab(self)
        self._touches.append(touch)

    def on_touch_up(self, touch):
        touch.ungrab(self)
        self._touches.remove(touch)

    def on_touch_move(self, touch):
        if touch in self._touches and touch.grab_current == self:
            if len(self._touches) == 1:
                self.do_rotate(touch)
            elif len(self._touches) == 2:
                pass

    def do_rotate(self, touch):
        ax, ay = self.define_rotate_angle(touch)
        if self.obj3d:
            self.obj3d.rot.x += ay
            self.obj3d.rot.y += ax


class MainApp(App):

    def build(self):
        root = ObjectTrackball()
        self.renderer = Renderer()
        scene = Scene()
        camera = PerspectiveCamera(15, 1, 1, 1000)
        loader = OBJLoader()
        obj = loader.load("MQ-27.obj")
        self.obj3d = obj
        self.camera = camera

        scene.add(obj)

        self.renderer.render(scene, camera)

        # move camera to get chance see the object
        camera.pos.z += 1500

        root.add_widget(self.renderer)
        root.set_object(obj)
        self.renderer.bind(size=self._adjust_aspect)
        return root

    def _adjust_aspect(self, inst, val):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect


if __name__ == '__main__':
    MainApp().run()
