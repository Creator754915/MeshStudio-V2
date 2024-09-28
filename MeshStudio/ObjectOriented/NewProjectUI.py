from PIL import Image
from ursina import *
from ursina.lights import DirectionalLight
from MeshStudio.Assets.plugins.CheckBox import CheckBox
from ursina.shaders import lit_with_shadows_shader
import psutil

from MeshStudio.MainFiles.SceneEditor import SceneEditor


class NewProjectUI(Entity):
    def __init__(self, parent=camera.ui):
        super().__init__(parent=parent)
        self.background = Sky(texture='sky_default')

        self.LeftPart = Entity(parent=camera.ui, model="quad", scale=(1.5, 999), color=color.black50,
                               position=window.left, z=998)

        self.RightPart = Entity(parent=camera.ui, model="quad", scale=(1.5, 999), color=color.black50,
                                position=window.right, z=998)

        self.TotalPhysicalsRAM = psutil.virtual_memory().total / 10 ** 6

        self.GetMaxRAMUsable = round(self.TotalPhysicalsRAM * .4)  # Max RAM Usable it's 40% of Total RAM

        self.GetMinRAMUsable = round(self.TotalPhysicalsRAM * .02)  # Min RAM Usable it's 2% of Total RAM

        print(f"Max RAM: {self.GetMaxRAMUsable}\nMin RAM: {self.GetMinRAMUsable}")

        # Global Settings

        Text(text="Name of the project: ", scale=1.5, position=(window.left + (0, 0.45)))

        self.ProjectName = InputField(default_value="My Project", max_lines=1, character_limit=16,
                                      position=(window.left + (0.25, 0.35)))

        Text(text="Description of the project: ", scale=1.5, position=(window.left + (0, 0.3)))

        self.ProjectDescription = InputField(default_value="Description", max_lines=4, radius=0.05, character_limit=100,
                                             position=(window.left + (0.25, 0.15)))

        Text(text="Max RAM use: ", scale=1.5, position=(window.left + (0, 0)))

        self.RamUsed = Slider(self.GetMinRAMUsable, self.GetMaxRAMUsable, step=1,
                              default=round(self.GetMaxRAMUsable * .25),
                              radius=Text.size / 2, height=Text.size * 2,
                              position=(window.left + (0.025, -0.1)))

        self.RAMInfo = Text(text="Max RAM use: ",
                            scale=1.2, position=(window.left + (0.025, -.15)))

        # Physics Settings

        Text(text="Enabled Physics: ", scale=1.5, position=(.2, .45))

        self.PhysicsCheckbox = CheckBox(scale=.05, position=(.5, .435), start_value=True)

        Text(text="Gravity instance: ", scale=1.5, position=(.2, .35))

        self.GravityInstanceSlider = Slider(0.1, 20, step=0.01, default=9.81,
                                            radius=Text.size / 5, height=Text.size * 1.4,
                                            position=(0.22, 0.26))

        Text(text="Enabled Light: ", scale=1.5, position=(.2, .2))

        self.LightCheckbox = CheckBox(scale=.05, position=(.5, .185), start_value=True)

        Text(text="Shadows Resolution: ", scale=1.5, position=(.2, .1))

        self.ShadowsResolutionSlider = Slider(32, 4096, step=32, default=2048,
                                              radius=Text.size / 5, height=Text.size * 1.4,
                                              position=(0.22, 0.01))

        self.ShadowResolutionText = Text(text="256x256", scale=1.2, position=(.21, -.02))

        Text(text="Preview Shadows ", scale=1, position=(-.1, .47))

        self.CreateProjectButton = Button(text="Create project", radius=0, color=color.blue, scale=(.438, .1),
                                          text_size=Text.size * 50,
                                          position=(0, -.45),
                                          on_click=self.CreateProject)

        self.TextureEntity = Entity(parent=camera.ui, model="cube", texture='brick', scale=0.2, position=(.31, -.16))
        self.TextureEntity.texture_scale = Vec2(self.ShadowsResolutionSlider.value, self.ShadowsResolutionSlider.value)
        self.ShadowsResolutionSlider.on_value_changed = self.ChangeTexture()

        self.light = DirectionalLight(shadows=True)
        self.light.look_at(Vec3(1, -1, 1))
        self.light.shadow_map_resolution = Vec2(2048, 2048)

        Entity(model='plane', scale=2, color=color.gray, shader=lit_with_shadows_shader)
        Entity(model='cube', y=.5, scale=.5, shader=lit_with_shadows_shader, color=color.gray)

        EditorCamera(zoom_speed=1, rotation_speed=0, move_speed=0, pan_speed=(0, 0),
                     rotation=Vec3(36, 136, 0))

    def ChangeTexture(self):
        self.ShadowResolutionText.text = f'{self.ShadowsResolutionSlider.value}x{self.ShadowsResolutionSlider.value}'
        self.TextureEntity.texture_scale = Vec2(self.ShadowsResolutionSlider.value, self.ShadowsResolutionSlider.value)

    def update(self):
        if self.PhysicsCheckbox.state is True:
            self.GravityInstanceSlider.enabled = True
        else:
            self.GravityInstanceSlider.enabled = False

        self.RAMInfo.text = f"Total RAM: {self.TotalPhysicalsRAM} Mo\nMax RAM: {self.GetMaxRAMUsable} Mo\nMin RAM: {self.GetMinRAMUsable} Mo\nRAM Will Usder: {self.RamUsed.value} Mo"
        self.ShadowResolutionText.text = f"{self.ShadowsResolutionSlider.value}x{self.ShadowsResolutionSlider.value} PIXELS"

    def CreateProject(self):
        destroy(self.light)
        for i in scene.entities:
            destroy(i)


if __name__ == "__main__":
    app = Ursina(title="Create Project - MeshStudio")
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    NewProjectUI()

    app.run()
