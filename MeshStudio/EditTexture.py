from PIL import Image
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.prefabs.grid_editor import PixelEditor
from ursina.prefabs.file_browser import FileBrowser

from Prefabs.additive_function import MultiFunctionCaller

app = Ursina()
window.fullscreen = False
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = False

empty_texture = Texture(Image.new(mode='RGBA',
                                  size=(32, 32),
                                  color=(255, 255, 255, 255)))


def create_image():
    def hide_panel():
        destroy(wp)

    def create():
        PE.visible = True
        PE.enabled = True

        PE.texture = Texture(Image.new(mode='RGBA',
                                       size=(scaleInput.value, scaleInput.value),
                                       color=(255, 255, 255, 255)))

        hide_panel()

    scaleInput = Slider(8, 64, step=8)

    rgbInput = InputField(default_value='scale', limit_content_to='().,0123456789',
                          character_limit=20)

    PE.visible = False
    PE.enabled = False

    wp = WindowPanel(
        title="Create Image",
        content=(
            Text("Scale of Image"),
            scaleInput,
            Text("Color in RGBA"),
            rgbInput,
            Button(text="Create", color=color.azure, on_click=create),
            Button(text="Close", color=color.red, on_click=MultiFunctionCaller((PE.save(), hide_panel)))
        )
    )


def import_image():
    global empty_texture

    PE.visible = False
    PE.enabled = False

    fb = FileBrowser(file_types=['.png', '.jpg', '.jpeg'], enabled=True)

    def on_submit(paths):
        PE.visible = True
        PE.enabled = True
        print('--------', paths)
        for i in paths:
            print('---', i)
            texture1 = load_texture(i)
            PE.texture = load_texture(texture1)

    fb.on_submit = on_submit


def create_rectangle():
    print(1)


file = DropdownMenu('File', buttons=(
    DropdownMenuButton('New', on_click=lambda: print(1)),
    DropdownMenuButton('Open', on_click=lambda: print(1)),
    DropdownMenuButton('Save', color=color.rgb(0, 100, 0), on_click=lambda: print(1)),
    DropdownMenu('Import', buttons=(
        DropdownMenuButton('PNG', on_click=lambda: print(1)),
        DropdownMenuButton('JPG', on_click=lambda: print(1)),
        DropdownMenuButton('JPEG', on_click=lambda: print(1)),
    )),
    DropdownMenuButton('Preferences', on_click=lambda: print(1)),
    DropdownMenuButton('Exit', color=color.rgb(75, 0, 0), on_click=lambda: application.quit),
))

PE = PixelEditor(texture=empty_texture, brush_size=1, z=-2)

PE.help_text.visible = False

texture_scale = TextField(parent=camera.ui, ignore_paused=True, origin=(.5, .5), y=-0.5, x=-0.614,
                          z=-1)

create_rect = Button(parent=camera.ui, text="Create Rectangle", scale=(4 * 0.05, 0.05), radius=0.05,
                     position=(-0.625, -0.25),
                     on_click=create_rectangle)

create_image = Button(parent=camera.ui, text="Create Image", scale=(4 * 0.05, 0.05), radius=0.05,
                      position=(-0.625, -0.25 - (0.05 * 1.5)),
                      on_click=create_image)

create_image = Button(parent=camera.ui, text="Import Image", scale=(4 * 0.05, 0.05), radius=0.05,
                      position=(-0.625, -0.25 - (0.05 * 3)),
                      on_click=import_image)

exit_editor = Button(parent=camera.ui, text="EXIT", scale=(4 * 0.05, 0.05), radius=0.05,
                     position=(-0.625, -0.25 - (0.05 * 4.5)),
                     on_click=application.quit)

EditorCamera()

app.run()
