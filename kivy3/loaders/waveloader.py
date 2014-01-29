
from .meshdata import MeshData
from kivy3 import Object3D


class WaveObject(object):
    """ This class contains top level mesh object information like vertices,
        normals, texcoords and faces
    """
    
    def __init__(self, loader, name=''):
        self.name = name
        self.faces = []
        self.loader = loader
    
    def to_mesh_data(self, vertex_format=None):
        
        mesh = MeshData(vertex_format=vertex_format)
        idx = 0
        for f in self.faces:
            verts =  f[0]
            norms = f[1]
            tcs = f[2]
            for i in range(3):
                #get normal components
                n = (0.0, 0.0, 0.0)
                if norms[i] != -1:
                    n = self.loader.normals[norms[i]-1]

                #get texture coordinate components
                t = (0.0, 0.0)
                if tcs[i] != -1:
                    t = self.loader.texcoords[tcs[i]-1]

                #get vertex components
                v = self.loader.vertices[verts[i]-1]

                data = [v[0], v[1], v[2], n[0], n[1], n[2], t[0], 1 - t[1]]
                mesh.vertices.extend(data)

            tri = [idx, idx+1, idx+2]
            mesh.indices.extend(tri)
            idx += 3
        return mesh


class WaveLoader:
    
    def __init__(self):
        pass
    
    def _load_meshes(self, filename, swapyz):
        
        wvobj = WaveObject(self)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        faces_section = False
        
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            if line.startswith('s'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'o' or values[0] == 'g':
                wvobj.name = values[1]
            if values[0] == 'v':
                if faces_section:
                    # here we yield new mesh object
                    faces_section = False
                    yield wvobj
                    wvobj = WaveObject(self)
                v = map(float, values[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = map(float, values[1:4])
                if swapyz:
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
        
    def _convert_to_objects(self, wave_objects):
        objects = []
        for wvobj in wave_objects:
            obj = Object3D(mesh=wvobj.to_mesh_data())
            objects.append(obj)
        return objects

    def load(self, filename, swapyz=False):
        
        wave_objects = []
        
        for wvobj in self._load_meshes(filename, swapyz):
            wave_objects.append(wvobj)
            
        return self._convert_to_objects(wave_objects)

    
def MTL(filename):
    contents = {}
    mtl = None
    return
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError, "mtl file doesn't start with newmtl stmt"
        mtl[values[0]] = values[1:]
    return contents