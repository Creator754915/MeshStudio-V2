from ursina import *
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader


class PIXELShader(Entity):
    def __init__(self, ClipPlaneFarSetter=1):
        super().__init__(ClipPlaneFarSetter=ClipPlaneFarSetter)
        camera.shader = pixelation_shader
        camera.clip_plane_far_setter = ClipPlaneFarSetter


if __name__ == "__main__":
    app = Ursina()

    Entity(model='sphere', color=color.orange)
    Entity(model='cube', y=-1)

    PIXELShader()

    EditorCamera()

    app.run()