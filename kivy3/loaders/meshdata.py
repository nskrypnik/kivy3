

class MeshData(object):
    """ This is more close to raw OpenGL mesh data and contains only
        vertices and indices may be used for  
    """
    
    def __init__(self, vertices=[], indices=[], vertex_format=None):
        self.vertex_format = vertex_format or [
            ('v_pos', 3, 'float'),
            ('v_normal', 3, 'float'),
            ('v_tc0', 2, 'float')]
        self.vertices = vertices
        self.indices = indices

        