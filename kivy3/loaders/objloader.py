"""
The MIT License (MIT)

Copyright (c) 2013 Niko Skrypnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Loaders for Wavefront format .obj files
=============

"""

from .loader import Loader
from kivy3 import Object3D, Mesh, Material
from kivy3.core.geometry import Geometry
from kivy3.core.face3 import Face3


class WaveObject(object):
    """ This class contains top level mesh object information like vertices,
        normals, texcoords and faces
    """

    def __init__(self, loader, name=''):
        self.name = name
        self.faces = []
        self.loader = loader

    def convert_to_mesh(self, vertex_format=None):
        """Converts data gotten from the .obj definition
        file and create Kivy3 Mesh object which may be used
        for drawing object in the scene
        """

        geometry = Geometry()
        material = Material()
        idx = 0
        for f in self.faces:
            verts = f[0]
            norms = f[1]
            tcs = f[2]
            face3 = Face3(0, 0, 0)
            for i, e in enumerate(['a', 'b', 'c']):
                #get normal components
                n = (0.0, 0.0, 0.0)
                if norms[i] != -1:
                    n = self.loader.normals[norms[i] - 1]
                face3.vertex_normals.append(n)

                #get texture coordinate components
                t = (0.0, 0.0)
                if tcs[i] != -1:
                    t = self.loader.texcoords[tcs[i] - 1]
                # TODO: figure out with texcoords

                #get vertex components
                v = self.loader.vertices[verts[i] - 1]
                if not v in geometry.vertices:
                    geometry.vertices.append(v)
                v_index = geometry.vertices.index(v)
                setattr(face3, e, v_index)
            geometry.faces.append(face3)

        mesh = Mesh(geometry, material)

        return mesh


class OBJLoader(Loader):

    def __init__(self):
        pass

    def _load_meshes(self):

        wvobj = WaveObject(self)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        faces_section = False

        for line in open(self.source, "r"):
            if line.startswith('#'):
                continue
            if line.startswith('s'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'o' or values[0] == 'g':
                wvobj.name = values[1]
            if values[0] == 'v':
                if faces_section:
                    # here we yield new mesh object
                    faces_section = False
                    yield wvobj
                    wvobj = WaveObject(self)
                v = map(float, values[1:4])
                if self.swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if self.swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] == 'f':
                if not faces_section:
                    faces_section = True
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(-1)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(-1)
                wvobj.faces.append((face, norms, texcoords))
        yield wvobj

    def load(self, source, **kw):
        self.swapyz = kw.pop("swapyz", False)
        return super(OBJLoader, self).load(source, **kw)

    def parse(self):

        obj = Object3D()

        for wvobj in self._load_meshes():
            obj.add(wvobj.convert_to_mesh())

        return obj


def MTL(filename):
    contents = {}
    mtl = None
    return
    for line in open(filename, "r"):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        mtl[values[0]] = values[1:]
    return contents
