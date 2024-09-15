from panda3d.core import LineSegs
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
from ursina.shaders import unlit_shader

from MeshStudio.Assets.plugins.CheckBox import CheckBox
from ursina.prefabs.file_browser_save import FileBrowserSave
from ursina.prefabs.first_person_controller import FirstPersonController
from PIL import Image
import numpy as np
from perlin_noise import PerlinNoise

app = Ursina(title='Texture Node Editor', borderless=False, fullscreen=False, development_mode=False, vsync=True)

test = Vec4(0, 0, 0, 0.72)


class Line2D(Entity):
    def __init__(self, parent=scene, start=Vec2(0, 0), end=Vec2(2, 0), line_color=Color(1, 1, 1, 1),
                 thickness=1.0, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent
        self.start = start
        self.end = end
        self.line_color = line_color
        self.thickness = thickness
        self.create_line()

    def create_line(self):
        line = LineSegs()
        line.setThickness(self.thickness)
        line.setColor(self.line_color[0], self.line_color[1], self.line_color[2], self.line_color[3])
        line.moveTo(self.start[0], self.start[1], 0)
        line.drawTo(self.end[0], self.end[1], 0)

        line_node = line.create()
        line_node_path = NodePath(line_node)
        self.model = line_node_path
        self.model.setTwoSided(True)

    def update_start_position(self, new_start):
        self.start = new_start
        self.create_line()

    def update_end_position(self, new_end):
        self.end = new_end
        self.create_line()


class ModelNode(Draggable):
    def __init__(self, text='', position=(0, 0), scale=(.3, .3, .3), color=Color(0, 0, 0, 0.72)):
        super().__init__(
            model=Quad(scale=(1, 1.6, 0.3)),
            text=text,
            text_origin=(0, .4),
            position=position,
            scale=scale,
            radius=0.05,
            color=color,
            highlight_color=color,
            texture="white_cube")

        self.modelText = Text(text='Model Node', position=(-.43, .58, -.01), scale=3.25, parent=self)

        self.modelText = Text(text='Model', position=(-.43, .58, -.01), scale=3.25, parent=self)
        self.path = InputField(default_value='path', limit_content_to='_./abcdefghijklmnopqrstuvwxyz',
                               character_limit=13, position=(0, .4, -.01), scale=(.9, .15), parent=self)
        self.scaleText = Text(text='Scale', position=(-.43, .2, -.01), scale=3.25, parent=self)
        self.scaleInput = InputField(default_value='scale', limit_content_to='().,0123456789',
                                     character_limit=13, position=(0, .03, -.01), scale=(.9, .15), parent=self)
        self.scale_attachment = Button(model='circle', position=(.5, 0.03, -.01), scale=.07, parent=self)
        self.scale_attachment.on_click = lambda: print("IN DEV")

        self.positionText = Text(text='Position', position=(-.43, -0.1, -.01), scale=3.25, parent=self)
        self.positionInput = InputField(default_value='position', limit_content_to='().,0123456789',
                                        character_limit=13, position=(0, -0.28, -.01), scale=(.9, .15), parent=self)
        self.position_attachment = Button(model='circle', position=(.5, -0.28, -.01), scale=.07, parent=self)
        self.position_attachment.on_click = lambda: print("IN DEV")

        self.shadows = Entity(position=(-.03, -.7, -.01), parent=self)
        self.shadowsText = Text(text='shadows', position=(-.4, .035), scale=3, parent=self.shadows)
        self.shadowsBox = CheckBox(scale=.08, parent=self.shadows)

    def make(self):
        self.m = Entity(model=self.path.text)

    def undo(self):
        destroy(self.m, delay=0)


class PositionNode(Draggable):
    def __init__(self, text='Position Node', position=(0, 0), scale=(.35, .3), color=Color(0, 0, 0, 0.72)):
        super().__init__(text=text, text_origin=(0, .4), position=position, scale=scale,
                         radius=0.05, color=color,
                         highlight_color=color)

        self.attachment = Button(model='circle', position=(-.5, 0, -.01), scale=.07, parent=self)


class ScaleNode(Draggable):
    def __init__(self, text='Scale Object', position=(0, 0), scale=(.35, .3), color=Color(0, 0, 0, 0.72)):
        super().__init__(text=text, text_origin=(0, .4), position=position, scale=scale,
                         radius=0.05, color=color,
                         highlight_color=color)

        self.texture_attachment = Button(model='circle', position=(-.5, -0.1, -.015), scale=.07, parent=self)

        self.slider_x = Slider(0, 100, step=1, position=(-0.475, .2, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)
        self.slider_y = Slider(0, 100, step=1, position=(-0.475, .1, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)
        self.slider_z = Slider(0, 100, step=1, position=(-0.475, 0, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)

        self.value_text = Text(align="left", position=(-0.3, -.18, -.01), size=.1, parent=self)

    def make(self):
        print(self.color)

    def UpdateColor(self):
        self.value_text.text = (
            self.slider_x.value, self.slider_y.value, self.slider_z.value
        )

    def undo(self):
        destroy(self, delay=0)


class ColorNode(Draggable):
    def __init__(self, text='RGB Color', position=(0, 0), scale=(.35, .3), color=Color(0, 0, 0, 0.72)):
        super().__init__(text=text, text_origin=(0, .4), position=position, scale=scale,
                         radius=0.05, color=color,
                         highlight_color=color)

        self.sky_color = Entity(scale=9900, shader=unlit_shader)

        self.texture_attachment = Button(model='circle', position=(-.5, 0, -.015), scale=.07, parent=self)

        self.slider_r = Slider(0, 255, position=(-0.475, .2, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)
        self.slider_g = Slider(0, 255, position=(-0.475, .1, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)
        self.slider_b = Slider(0, 255, position=(-0.475, 0, -.01), scale=(1.9, 2), parent=self,
                               dynamic=True,
                               on_value_changed=self.UpdateColor)

        self.value_text = Text(align="left", position=(-0.44, -.1, -.01), size=.065, parent=self)

        self.preview = Entity(model="cube", position=(-0, -.35, -.01), scale=(0.55, 0.22), parent=self)

    def make(self):
        print(self.color)
        self.sky_color.color = color.rgba(self.color[0], self.color[1], self.color[2], self.color[3])
        self.sky_color.world_position = camera.world_position

    def UpdateColor(self):
        self.value_text.text = (
            round(self.slider_r.value, 2), round(self.slider_g.value, 2), round(self.slider_b.value, 2), 0.72)
        self.preview.color = color.rgba(self.slider_r.value, self.slider_g.value, self.slider_b.value, 255)

    def undo(self):
        destroy(self, delay=0)


class DirectionalLightNode(Draggable):
    def __init__(self, text='Directional Light', position=(0, 0), scale=.3, color=Color(0, 0, 0, 0.72)):
        super().__init__(
            text=text,
            text_origin=(0, .4),
            position=position,
            scale=scale,
            radius=0.05,
            color=color,
            highlight_color=color)

        self.texture_attachment = Button(model='circle', position=(-.5, 0, -.01), scale=.07, parent=self)

        self.shadows = Entity(position=(-.03, .15, -.01), parent=self)
        self.shadowsText = Text(text='shadows', position=(-.4, .035), scale=3, parent=self.shadows)
        self.shadowsBox = CheckBox(scale=.08, parent=self.shadows)

        self.resolutionText = Text(text='shadows resolution', position=(-.4, -.052), scale=3, parent=self.shadows)

        self.MapResolutionSlider = Slider(32, 2048, default=256, step=32, position=(-0.475, -.1), scale=(1.9, 2),
                                          parent=self,
                                          dynamic=True)

    def make(self):
        self.sun = DirectionalLight(shadows=self.shadowsBox.state)
        self.sun.look_at(Vec3(1, -1, -1))
        self.sun.shadow_map_resolution = Vec2(self.MapResolutionSlider.value, self.MapResolutionSlider.value)

    def undo(self):
        destroy(self.sun, delay=0)


class PerlinNoiseNode(Draggable):
    def __init__(self, text='Perlin Noise', position=(0, 0), scale=.3, color=Color(0, 0, 0, 0.75), **kwargs):
        super().__init__(text=text,
                         text_origin=(0, .4),
                         position=position,
                         scale=scale,
                         radius=.05,
                         color=color,
                         highlight_color=color)

        octaves_slider = Slider(parent=self, step=1, min=1, max=20, scale=(2, 2), y=.2, x=-.5)

        seed_slider = Slider(parent=self, step=1, min=1, max=1000000, scale=(2, 2), y=.1, x=-.5)

        scale_texture_input = InputField(parent=self, scale=(.8, 0.18), y=-0.1)

        generate_button = Button(parent=self, text="Generate", scale=(.8, .25), y=-.35)

    def create(self):
        noise = PerlinNoise(octaves=self.octaves_slider.value, seed=self.octaves_slider.value)
        xpix, ypix = 100, 100
        pic = [[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

        image = Image.fromarray(np.array(pic) * 255, 'L')
        image.save('output.png')


class CameraNode(Draggable):
    def __init__(self, text='Camera Type Name', position=(0, 0), scale=.3, color=Color(0, 0, 0, 0.75), **kwargs):
        super().__init__(
            text=text,
            text_origin=(0, .4),
            position=position,
            scale=scale,
            radius=.05,
            color=color,
            highlight_color=color)

        self.camera = Entity(position=(-.03, .15, -.01), scale=(0.3, 0.05), parent=self)

        Entity(parent=self, model="plane", position=(0, 0, 1), rotation=(0, 0, 0), scale=(0.3, 0.05),
               color=Color(255, 0, 0, 0.90))

        # self.cameraText = Text(text='Camera Type Name', position=(-.43, .04, -.01), scale=3.25, parent=self)
        Text(text="Editor Camera", position=(-0.25, .2, -.02), scale=3, parent=self)
        self.ec_checkbox = CheckBox(position=(0, .08, -.02), scale=.08, parent=self)

        Text(text="First Camera", position=(-0.25, 0, -.02), scale=3, parent=self)
        self.fpc_checkbox = CheckBox(position=(0, -.14, -.02), scale=.08, parent=self)

    def make(self):
        if self.ec_checkbox.state is True:
            EditorCamera()
        elif self.fpc_checkbox is True:
            FirstPersonController()
        else:
            camera.position = (0, 0, 0)
            camera.rotation = (0, 0, 0)

    def undo(self):
        destroy(self, delay=0)


nodes = []


def createNode(node):
    newNode = node()
    nodes.append(newNode)


def save_project():
    wp = FileBrowserSave(file_type='.json', z=-5)

    import json
    save_data = {
        "nodes": {
            "node1": {
                "model": nodes
            }
        }
    }

    print(nodes)
    wp.data = json.dumps(save_data)


def convert():
    try:
        print(nodes)
        print(scene.entity)
    except Exception as e:
        print_warning(f"Error: {e}")


DropdownMenu(text='File', buttons=(
    DropdownMenuButton(text='New'),
    DropdownMenuButton(text='Open'),
    DropdownMenuButton(text='Save', on_click=save_project),
    DropdownMenu(text='Options', buttons=(
        DropdownMenuButton(text='Option a'),
        DropdownMenuButton(text='Option b'),
    )),
    DropdownMenuButton(text='Convert', color=color.rgb(0, 100, 0), on_click=convert),
    DropdownMenuButton(text='Exit', color=color.rgb(75, 0, 0), on_click=application.quit),
))

# Add
addMenu = DropdownMenu(text='Add', buttons=(
    DropdownMenuButton(text='Model', on_click=Func(createNode, ModelNode)),
    DropdownMenu(text='Attributes', buttons=(
        DropdownMenuButton(text='Position Attribute', on_click=Func(createNode, PositionNode)),
        DropdownMenuButton(text='Scale Attribute', on_click=Func(createNode, ScaleNode)),

    )),
    DropdownMenuButton(text='Light', on_click=Func(createNode, DirectionalLightNode)),
    DropdownMenuButton(text='Color', on_click=Func(createNode, ColorNode)),
    DropdownMenuButton(text='Texture Noise', on_click=Func(createNode, PerlinNoiseNode)),
    DropdownMenuButton(text='Camera', on_click=Func(createNode, CameraNode)),
))

addMenu.x = window.top_left.x + .23


def run():
    camera.ui.disable()
    backButton.visible = True
    for i in range(len(nodes)):
        nodes[i].make()


def back():
    camera.ui.enable()
    backButton.visible = False


def input(key):
    if held_keys['control'] and key == "e":
        try:
            camera.ui.enable()
            for i in range(len(nodes)):
                nodes[i].undo()
        except AttributeError:
            print_on_screen(text=f"Please use a CAMERA !", position=(-.1, 0), scale=2)

    if held_keys['control'] and key == "w":
        try:
            if nodes:
                cube = nodes.pop()
                destroy(cube)

                print_on_screen(text=f"{cube} was deleted !", position=(-.1, 0), scale=2)
        except AssertionError:
            print_on_screen(text="Try Again !", position=(-.1, 0), scale=2)

    if held_keys['control'] and key == 'scroll up':
        for node in nodes:
            if node.scale < 0.89:
                node.scale = node.scale * 1.2

    if held_keys['control'] and key == 'scroll down':
        for node in nodes:
            if node.scale > 0.12:
                node.scale = node.scale / 1.2

    if held_keys['delete']:
        if nodes:
            node = nodes.pop()
            destroy(node)

    print(key)


# grid = Entity(model=Grid(50, 50), rotation=(0, 0, 0), scale=(50, 50), position=(0, 0, 20))

runButton = Button(model='circle', icon='../icons/run.png', position=window.top_right + (-.025, -.025), scale=.03,
                   color=color.black10,
                   on_click=run)

backButton = Button(parent=scene, model='circle', icon='../icons/run.png', position=window.top_right + (-.025, -.025),
                    scale=1,
                    rotation=(0, 0, 180),
                    color=color.black10,
                    visible=False,
                    on_click=back)

n1 = ScaleNode()
n2 = PositionNode()
n3 = ModelNode()

nodeConnector = Line2D(parent=camera.ui, start=Vec2(.3, 0), end=Vec2(5, 0), line_color=Color(1, 1, 1, 1),
                       thickness=10.0)

nodeConnector2 = Line2D(parent=camera.ui, start=Vec2(.3, 0), end=Vec2(5, 0), line_color=Color(1, 1, 1, 1),
                        thickness=10.0)


def update():
    nodeConnector.update_start_position(Vec2(n3.position.x + n3.scale_x / 2, n3.position.y - 0.08))
    nodeConnector.update_end_position(Vec2(n2.position.x - n2.scale_x / 2, n2.position.y))
    nodeConnector2.update_start_position(Vec2(n3.position.x + n3.scale_x / 2, n3.position.y + 0.01))
    nodeConnector2.update_end_position(Vec2(n1.position.x - n2.scale_x / 2, n1.position.y - 0.027))


app.run()
