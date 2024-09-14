from ursina import *
from ursina.shaders.screenspace_shaders.camera_vertical_blur import camera_vertical_blur_shader


class BLURShader(Entity):
    def __init__(self, Intensity=0.05, BlackBG=True):
        super().__init__(self, Intensity=Intensity, BlackBG=BlackBG)
        camera.shader = camera_vertical_blur_shader
        camera.set_shader_input("blur_size", Intensity)

        if BlackBG is True:
            window.color = color._16
        else:
            window.color = color.dark_gray


if __name__ == "__main__":
    app = Ursina()

    Entity(model='sphere', color=color.orange)
    Entity(model='cube', y=-1)

    BLURShader(0.4, False)

    EditorCamera()

    app.run()
