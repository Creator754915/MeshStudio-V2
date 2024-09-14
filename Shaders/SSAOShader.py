from ursina import *
from ursina.shaders.screenspace_shaders.ssao import ssao_shader


class SSAOShader(Entity):
    def __init__(self, ClipPlaneNear=1):
        super().__init__(self, ClipPlaneNear=ClipPlaneNear)
        camera.shader = ssao_shader
        camera.clip_plane_near = ClipPlaneNear


if __name__ == "__main__":
    app = Ursina()

    ed = EditorCamera()

    SSAOShader(ClipPlaneNear=1)

    Entity(model='sphere', color=color.orange)
    Entity(model='cube', y=-1)
    Entity(model='plane', scale=100, y=-1)

    for i in range(20):
        e = Entity(model='cube', position=Vec3(random.random(), random.random(), random.random()) * 3,
                   rotation=Vec3(random.random(), random.random(), random.random()) * 360)

    app.run()
