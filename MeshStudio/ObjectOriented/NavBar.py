from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenuButton, DropdownMenu


class NavBar(Entity):
    def __init__(self, color=color.gray, **kwargs):
        super().__init__(color=color, **kwargs)
        self.parent = camera.ui
        self.color = self.color.tint(-.05)

        DropdownMenu('File', buttons=(
            DropdownMenuButton('New Project'),
            DropdownMenuButton('Open'),
            DropdownMenuButton('Save', color=Color(0, 100, 0, .35)),
            DropdownMenu('Import Models', buttons=(
                DropdownMenuButton('OBJ files'),
                DropdownMenuButton('GLB files'),
                DropdownMenuButton('GLTF files')
            )),
            DropdownMenuButton('Exit', color=Color(75, 0, 0, .35), on_click=lambda: application.quit)
        ))
        self.pp = DropdownMenu('Preferences')
        self.pp.x = -window.aspect_ratio / 2 + .25
        self.changePX = False

    def update(self):
        if window.aspect_ratio >= 1.9374369323915237 and self.changePX == True:
            self.pp.x = -window.aspect_ratio / 2 + .25
            self.changePX = False
        elif window.aspect_ratio == 1.7777777777777777:
            self.pp.x = -window.aspect_ratio / 2 + .25
            self.changePX = True


if __name__ == "__main__":
    app = Ursina()
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    NavBar(color=color.red)

    EditorCamera()


    def update():
        print(window.aspect_ratio)


    app.run()
