from ursina import *


class TextureUI(Entity):
    def __init__(self):
        super(TextureUI, self).__init__()
        self.entities = True

        self.button_dict = {
            'noise': Func(self.look_texture, 'noise'),
            'grass': Func(self.look_texture, 'grass'),
            'vignette': Func(self.look_texture, 'vignette'),
            'arrow_right': Func(self.look_texture, 'arrow_right'),
            'test_tileset': Func(self.look_texture, 'test_tileset'),
            'tilemap_test_level': Func(self.look_texture, 'tilemap_test_level'),
            'shore': Func(self.look_texture, 'shore'),
            'file_icon': Func(self.look_texture, 'file_icon'),
            'sky_sunset': Func(self.look_texture, 'sky_sunset'),
            'radial_gradient': Func(self.look_texture, 'radial_gradient'),
            'circle': Func(self.look_texture, 'circle'),
            'perlin_noise': Func(self.look_texture, 'perlin_noise'),
            'brick': Func(self.look_texture, 'brick'),
            'grass_tintable': Func(self.look_texture, 'grass_tintable'),
            'circle_outlined': Func(self.look_texture, 'circle_outlined'),
            'ursina_logo': Func(self.look_texture, 'ursina_logo'),
            'arrow_down': Func(self.look_texture, 'arrow_down'),
            'cog': Func(self.look_texture, 'cog'),
            'vertical_gradient': Func(self.look_texture, 'vertical_gradient'),
            'white_cube': Func(self.look_texture, 'white_cube'),
            'horizontal_gradient': Func(self.look_texture, 'horizontal_gradient'),
            'folder': Func(self.look_texture, 'folder'),
            'rainbow': Func(self.look_texture, 'rainbow'),
            'heightmap_1': Func(self.look_texture, 'heightmap_1'),
            'sky_default': Func(self.look_texture, 'sky_default'),
        }

        self.button = ButtonList(button_dict=self.button_dict, font='VeraMono.ttf', button_height=1.5, popup=True)

        self.cube = Entity(parent=camera.ui, model="cube", scale=.15, x=-.45, y=.15)
        self.sphere = Entity(parent=camera.ui, model="sphere", scale=.15, x=-.45, y=-.15)

        self.bg = Entity(parent=camera.ui, model="quad", scale=(999, 999), color=color.black66, z=5)

    def look_texture(self, txt_arg: str):
        self.cube.texture = txt_arg
        self.sphere.texture = txt_arg

    def update(self):
        if self.entities:
            self.cube.rotation_y += 1
            self.cube.rotation_x += 1
            self.sphere.rotation_y += 1
            self.sphere.rotation_x += 1

    def input(self, key):
        if key == "escape":
            self.entities = False
            destroy(self.button)
            destroy(self.cube)
            destroy(self.sphere)
            destroy(self.bg)


if __name__ == "__main__":
    app = Ursina(size=(720, 480))
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False

    TextureUI()

    app.run()
