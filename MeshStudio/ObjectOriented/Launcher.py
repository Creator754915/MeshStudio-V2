from ursina import *

from MeshStudio.ObjectOriented.CoreFiles.InstructionMenu import InstructionMenu
from MeshStudio.ObjectOriented.NewProjectUI import NewProjectUI


class Launcher():
    def __init__(self):
        super().__init__()
        self.launcher = []
        window.borderless = False
        window.fullscreen = False
        window.exit_button.enabled = False
        window.fps_counter.enabled = False

        self.background = Sky(texture='sky_sunset')
        self.launcher.append(self.background)

        self.title = Text(parent=camera.ui, text="MeshStudio", size=1.2, position=window.top - Vec2(0.08, 0.25))
        self.launcher.append(self.title)

        self.runBtn = Button(parent=camera.ui, text="Start New Project", scale=(0.25, 0.1), radius=0.1,
                             on_click=self.new_project,
                             y=0)
        self.launcher.append(self.runBtn)

        self.settingsBtn = Button(parent=camera.ui, text="Setting", scale=(0.25, 0.1), radius=0.1,
                                  y=-.15)
        self.launcher.append(self.settingsBtn)

        self.exitBtn = Button(parent=camera.ui, text="Exit", color=color.red.tint(-.3), scale=(0.25, 0.1), radius=0.1,
                              y=-.3)
        self.launcher.append(self.exitBtn)

        InstructionMenu(
            "MeshStudio is in beta, if you have issues, go to the github for repport the issues")

    def new_project(self):
        for i in range(5):
            destroy(self.launcher[i])
        NewProjectUI()


if __name__ == "__main__":
    app = Ursina(title="Launcher - MeshStudio")

    Launcher()

    app.run()

