
import os
import unittest
from kivy3.loaders import WaveLoader

this_dir = os.path.abspath(os.path.dirname(__file__))

class WaveLoadertestCase(unittest.TestCase):
    
    def test_mesh_loader(self):
        loader = WaveLoader()
        obj_path = os.path.join(this_dir, 'testnurbs.obj')
        meshes = list(loader._load_meshes(obj_path, False))
        self.assertEqual(len(meshes), 4)
    
    def test_loader(self):
        loader = WaveLoader()
        obj_path = os.path.join(this_dir, 'testnurbs.obj')
        objects = loader.load(obj_path)
        self.assertEqual(len(objects), 4)


if __name__ == '__main__':
    unittest.main()