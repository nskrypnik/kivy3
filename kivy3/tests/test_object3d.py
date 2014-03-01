
import unittest
from kivy3 import Object3D


class Object3DTest(unittest.TestCase):

    def test_creation(self):
        obj = Object3D()

    def test_position(self):
        obj = Object3D()
        obj.pos.x = 10
        self.assertEqual(obj._position[0], 10)
        obj.position.y = 8
        self.assertEqual(obj._position[1], 8)
        obj.pos.z = 3 
        self.assertEqual(obj._position[2], 3)


if __name__ == "__main__":
    unittest.main() 