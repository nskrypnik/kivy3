import os
import unittest
from kivy3 import Scene
from kivy3.loaders import WaveLoader

this_dir = os.path.abspath(os.path.dirname(__file__))

class SceneTestCase(unittest.TestCase):
    
    def test_load_scene(self):
        scene = Scene()
        loader = WaveLoader()
        obj_path = os.path.join(this_dir, 'testnurbs.obj')
        objects = loader.load(obj_path)
        scene.add(*objects)
        self.assertEqual(len(scene.objects), 4)


if __name__ == '__main__':
    unittest.main()
