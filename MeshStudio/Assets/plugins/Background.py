from ursina import *
from ursina.shaders import unlit_shader


class Background(Entity):

    def __init__(self, parent=camera.ui, name='sky', model='dome', texture='sky_default', **kwargs):
        super().__init__(parent=parent, name=name, model=model, texture=texture, shader=unlit_shader)
        self.texture = texture
        self.scale = (999, 999)
        self.world_position = (0, 0, 0)

        for key, value in kwargs.items():
            setattr(self, key, value)


if __name__ == '__main__':
    app = Ursina()

    Background(texture='sky_sunset')

    app.run()
