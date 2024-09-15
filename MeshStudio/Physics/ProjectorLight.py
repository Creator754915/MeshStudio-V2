from ursina import *
from ursina.shaders.projector_shader import projector_shader


class ProjectorLight(Entity):
    def __init__(self, parent=scene, model=None, unlit=True, ProjectorTexture='vignette',
                 FogDensity=(10, 250), speed=5):
        super().__init__(parent=parent, model=model, unlit=unlit, ProjectorTexture=ProjectorTexture,
                         FogDensity=FogDensity, speed=speed)
        scene.fog_density = FogDensity
        self.projector_texture = load_texture(self.ProjectorTexture, application.internal_textures_folder)

        Entity(parent=self, model="sphere", scale=(.5, .5, .5), y=2)
        Entity(parent=self, model="cube", scale=(0.1, 2, 0.1), y=1)

    def SetUp(self):
        self.projector_shader.default_input['projector_texture'] = self.projector_texture

    def update(self):
        for EntityToAffect in scene.entities:
            if hasattr(EntityToAffect, 'shader') and EntityToAffect.shader == projector_shader:
                EntityToAffect.set_shader_input('projector_uv_offset',
                                                light.world_position.xz * projector_shader.default_input[
                                                    'projector_uv_scale'])

        self.x += (held_keys['d'] - held_keys['a']) * time.dt * self.speed
        self.z += (held_keys['w'] - held_keys['s']) * time.dt * self.speed


if __name__ == "__main__":
    app = Ursina()

    Entity.default_shader = projector_shader

    editor_camera = EditorCamera(rotation_x=30)
    light = ProjectorLight()
    ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4, 4))

    random.seed(0)
    for i in range(16):
        Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1, 2),
               x=random.uniform(-8, 8),
               z=random.uniform(-8, 8) + 8,
               collider='box',
               scale_y=random.uniform(2, 3),
               color=color.hsv(0, 0, random.uniform(.9, 1))
               )

    app.run()
