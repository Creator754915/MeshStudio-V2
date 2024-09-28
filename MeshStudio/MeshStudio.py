from ursina import *


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

        self.iconTitle = Button(parent=camera.ui, icon=f"../../MeshStudio/icons/meshstudio_logo_big.png",
                                scale=0.2, color=color.rgba(0, 0, 0, 0), collider=None,
                                position=window.top - Vec2(0, 0.12))

        self.title = Button(parent=camera.ui, text="MeshStudio", color=color.rgba(0, 0, 0, 0),
                            text_size=Text.size * 100, position=window.top - Vec2(0.0, 0.26),
                            disabled=True, collider=None)
        self.launcher.append(self.title)

        self.versionText = Button(parent=camera.ui, text="Version Alpha 2.0.0",
                                  position=window.bottom_right - Vec2(0.12, -0.025),
                                  color=color.rgba(0, 0, 0, 0), collider=None)

        self.runBtn = Button(parent=camera.ui, text="Start New Project", scale=(0.25, 0.1), radius=0.1,
                             on_click=self.new_project,
                             y=0)
        self.launcher.append(self.runBtn)

        self.settingsBtn = Button(parent=camera.ui, text="Setting", scale=(0.25, 0.1), radius=0.1,
                                  y=-.15)
        self.launcher.append(self.settingsBtn)

        self.exitBtn = Button(parent=camera.ui, text="Exit", color=color.red.tint(-.3), scale=(0.25, 0.1), radius=0.1,
                              text_size=Text.size * 50,
                              y=-.3)
        self.launcher.append(self.exitBtn)

        #InstructionMenu(
        #    "MeshStudio is in beta, if you have issues, go to the github for repport the issues")

    def new_project(self):
        for i in range(5):
            destroy(self.launcher[i])


if __name__ == "__main__":
    app = Ursina(title="Launcher - MeshStudio", development_mode=False, show_ursina_splash=False)

    Launcher()

    app.run()
