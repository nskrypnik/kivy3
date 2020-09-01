from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import (
    NumericProperty,
    ReferenceListProperty
)

# Map for light attributes to shader
# uniform variables
LIGHT_TO_SHADER_MAP = {
    "pos": "light_pos",
    "intensity": "light_intensity",
}


class LightError(Exception):
    pass


class Light(EventDispatcher):

    # ensure floats everywhere,
    # otherwise it breaks stuff
    pos_x = NumericProperty(0.0)
    pos_y = NumericProperty(0.0)
    pos_z = NumericProperty(0.0)
    pos = ReferenceListProperty(pos_x, pos_y, pos_z)
    intensity = NumericProperty(1000.0)

    def __init__(self, renderer=None, intensity=None,
                 pos=None, origin=None, **kwargs):
        if not renderer:
            raise LightError("Renderer is not defined!")
        super(Light, self).__init__(**kwargs)
        self.renderer = renderer
        self.on_pos(self, pos if pos else self.pos)
        self.on_intensity(self, intensity if intensity else self.intensity)

    def on_pos(self, instance, value):
        self._update_fbo(
            'pos',
            (float(value[0]),
             float(value[1]),
             float(value[2]))
        )

    def on_intensity(self, instance, value):
        self._update_fbo('intensity', float(value))

    def _update_fbo(self, key, value):
        if key in LIGHT_TO_SHADER_MAP:
            uniform_var = LIGHT_TO_SHADER_MAP[key]
            self.renderer.fbo[uniform_var] = value
