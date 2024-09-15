import json

from PIL import Image
from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenuButton, DropdownMenu
from ursina.prefabs.file_browser import FileBrowser
from ursina.prefabs.file_browser_save import FileBrowserSave
from ursina.prefabs.grid_editor import PixelEditor
from ursina.prefabs.video_recorder import VideoRecorderUI
from ursina.shaders import lit_with_shadows_shader

from ObjectOriented.WorldDirectionBox import DirectionBox
from ObjectOriented.WorldGrid import WorldGrid

# Pandas3D
from Physics.RigidBody import *

# from TexturesUI import TextureUI
from Assets.plugins.ClickPanel import ClickPanel
from Animation.timeline import Timeline

from Physics.sun import Sun
from Prefabs.memory_counter import MemoryCounter

# from github_request import GetLastestVersion


window.title = "MeshStudio"
window.icon = "./icons/meshstudio_logo.png"
app = Ursina(size=(720, 480))
window.fullscreen = False
window.borderless = False
window.exit_button.enabled = False
window.fps_counter.enabled = False

MemoryCounter()

editor_camera = EditorCamera()
editor_camera.rotation = Vec3(33, -45, 0)
editor_camera.position = Vec3(0, 0, 0)
editor_camera.enabled = False

sky = Sky(texture="sky_default")

project_name = 'Scene1'
name = 'Entity1'
cube_list = []
physic_nmb = []
save = False

timeline_speed = 1

debugNode = BulletDebugNode()
debugNode.showWireframe(False)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()

world = BulletWorld()
world.setGravity(Vec3(0, -9.81, 0))
world.setDebugNode(debugNP.node())

physic = False

ground = Entity(model='plane', color=Color(0, 0, 0, 0), y=0, scale=30, collider="box")
gr = Rigidbody(world=world, shape=BoxShape(size=(30, .05, 30)), entity=ground)

empty_texture = Texture(Image.new(mode='RGBA',
                                  size=(32, 32),
                                  color=(255, 255, 255, 255)))
pe = PixelEditor(texture=empty_texture, brush_size=1, z=-2, visible=False, enabled=False)
pe.help_text.visible = False

DirectionBox(parent=camera.ui, camera=editor_camera, enabled=True,
             render_queue=1,
             scale=0.018,
             position=Vec2(0.54, 0.425))


def hide_w():
    editor_camera.enabled = True
    destroy(wp)


def new_project():
    def hide_wwp():
        destroy(wwp)

    def clear_all():
        scene.clear(cube_list)

    if save is False:
        wwp = WindowPanel(
            title='WARNING',
            content=(
                Text('Are you sure to unsave your project ?'),
                Button(text='Yes', color=color.azure, on_click=clear_all),
                Button(text='Close', color=color.red, on_click=hide_wwp)
            ),
        )
        wwp.y = wwp.panel.scale_y / 2 * wwp.scale_y
    else:
        Func(scene.clear(cube_list))


def entity_cube(model_t):
    # global save

    # cube1 = Entity(parent=scene, model=model_t, name=f'Cube{len(cube_nmb)}', collider="box", postion=(0, 0, 0),
    #                color=rgb(r, g, b), texture='white_cube',
    #                lock=(0, 0, 0))

    # positionGizmo = PositionGizmo(cube1, 0, lambda: ...)
    # positionGizmo.SetUp()

    # positionGizmo.parent = cube1

    # Entity(parent=cube1, model='quad', color=color.orange, scale=(.05, .05))

    # save = False

    cube1 = MeshStudio.AddEntity(model=model_t, name=f"Entity{len(cube_list)}")

    cube_list.append(cube1)

    print(cube_list)


def add():
    def hide_wpo():
        destroy(wpo)

    def mesh_create():
        def hide_cm():
            destroy(cm)

        def create_mesh():
            global save
            try:
                verts = input1.text
                tris = input2.text
                uvs = input3.text
                norms = input4 * len(verts)

                # verts = ((0, 0, 0), (1, 0, 0), (.5, 1, 0), (-.5, 1, 0))
                # tris = (1, 2, 0, 2, 3, 0)
                # uvs = ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0, 1.0))
                # norms = ((0, 0, -1),) * len(verts)

                colors = (color.red, color.blue, color.lime, color.black)
                Entity(model=Mesh(vertices=verts, triangles=tris, uvs=uvs, normals=norms, colors=colors), scale=2)
                save = False
            except (IndexError, ValueError, AttributeError):
                print_warning("Error: Failed to create the Mesh")

        destroy(wpo)

        input1 = InputField(character_limit=50)
        input2 = InputField(character_limit=40)
        input3 = InputField(character_limit=40)
        input4 = InputField(character_limit=40)
        cm = WindowPanel(
            title='Mesh',
            content=(
                Text('Mesh Type:'),
                Text(text='Vertices:'),
                input1,
                Text(text='Triangles:'),
                input2,
                Text(text='UVS:'),
                input3,
                Text(text='Normals:'),
                input4,
                Button(text='Create', color=color.azure, on_click=create_mesh),
                Button(text='Close', color=color.red, on_click=hide_cm)
            ),
        )
        cm.y = cm.panel.scale_y / 2 * cm.scale_y

    wpo = WindowPanel(
        title='Model',
        content=(
            Text('Model Type:'),
            Button(text='Cube', color=color.azure, on_click=Func(entity_cube, "cube")),
            Button(text='Sphere', color=color.azure, on_click=Func(entity_cube, "sphere")),
            Button(text='Plane', color=color.azure, on_click=Func(entity_cube, "plane")),
            Button(text='Quad', color=color.azure, on_click=Func(entity_cube, "quad")),
            Button(text='Mesh', color=color.azure, on_click=mesh_create),
            Button(text='Close', color=color.red, on_click=hide_wpo)
        ),
    )

    wpo.y = wpo.panel.scale_y / 2 * wpo.scale_y

    print(cube_list)


def custom_effect(effect_name):
    global physic
    if effect_name == 'rigidbody':
        physic = True

        ground.visible = True

        def hide_wpf():
            destroy(wpf)

        def create_object(object_name):
            if object_name == "capsule":
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                capsule = Entity(model='sphere', texture='brick', y=5, scale=(1, 2, 1), color=Color(r, g, b, 1))
                Rigidbody(world=world, shape=CapsuleShape(height=2, radius=1), entity=capsule, mass=3)

                Entity(parent=capsule, model='quad', color=color.orange, scale=(.05, .05))

                physic_nmb.append(capsule)
                hide_wpf()

            elif object_name == "box":
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                box = Entity(model="cube", texture="brick", color=rgb(r, g, b), y=8, scale=(1, 1, 1))
                Rigidbody(world=world, shape=BoxShape(), entity=box, mass=1)

                Entity(parent=box, model='quad', color=color.orange, scale=(.05, .05))

                physic_nmb.append(box)
                hide_wpf()

            elif object_name == "sphere":
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)

                sphere = Entity(model='sphere', texture='brick', y=5, color=Color(r, g, b, 1))
                Rigidbody(world=world, shape=SphereShape(), entity=sphere, mass=5)

                Entity(parent=sphere, model='quad', color=color.orange, scale=(.05, .05))

                physic_nmb.append(sphere)
                hide_wpf()

        wpf = WindowPanel(
            title='RigidBody Type',
            content=(
                Text('Object Type:'),
                Button(text='Box', color=color.azure, on_click=Func(create_object, "box")),
                Button(text='Sphere', color=color.azure, on_click=Func(create_object, "sphere")),
                Button(text='Capsule', color=color.azure, on_click=Func(create_object, "capsule")),
                Button(text='Close', color=color.red, on_click=hide_wpf)
            ),
        )

        wpf.y = wpf.panel.scale_y / 2 * wpf.scale_y

    elif effect_name == 'wall':
        physic = True

        ground.visible = True

        for l in range(3):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            rgb_sphere = Entity(model="cube", texture="brick", color=rgb(r, g, b), x=l + 1, y=1, scale=(1, 1, 1))
            Rigidbody(world=world, shape=SphereShape(), entity=rgb_sphere, mass=5, friction=.7)

            Entity(parent=rgb_sphere, model='quad', color=color.orange, scale=(.05, .05))

            physic_nmb.append(rgb_sphere)

        for h in range(3):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            rgb_sphere = Entity(model="cube", texture="brick", color=rgb(r, g, b), y=h + 2, scale=(1, 1, 1))
            Rigidbody(world=world, shape=SphereShape(), entity=rgb_sphere, mass=5, friction=.7)

            Entity(parent=rgb_sphere, model='quad', color=color.orange, scale=(.05, .05))

            physic_nmb.append(rgb_sphere)

        for h in range(1, 3):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            rgb_sphere = Entity(model="cube", texture="brick", color=rgb(r, g, b), x=h + 1, y=5, scale=(1, 1, 1))
            Rigidbody(world=world, shape=SphereShape(), entity=rgb_sphere, mass=5, friction=.7)

            Entity(parent=rgb_sphere, model='quad', color=color.orange, scale=(.05, .05))

            physic_nmb.append(rgb_sphere)


def rename_object():
    def hide_wpr():
        destroy(wpr)

    object_name = InputField(text='Object1')

    def chg_name():
        for cube in cube_list:
            cube.name = object_name.text

    wpr = WindowPanel(
        title='Object Name',
        content=(
            Text('New Object Name:'),
            object_name,
            Button(text='Submit', color=color.azure, on_click=chg_name),
            Button(text='Close', color=color.red, on_click=hide_wpr)
        ),
    )

    wpr.y = wpr.panel.scale_y / 2 * wpr.scale_y


def remove_cube(*args):
    def all_cube():
        for cube1 in cube_list:
            cube1.DestroyGizmo()
            destroy(cube1)

    if cube_list:
        cube = cube_list.pop()
        destroy(cube)

    if args == 'all_cube':
        all_cube()


def change_color():
    if cube_list:
        cube_list[-1].color = color.random_color()
        print_on_screen("Enitity have been remove !")


def set_texture():
    def hide_tw():
        destroy(tw)

    def textures():
        if cube_list:
            cube = cube_list[:-1]
            cube.texture = texture_name.text

    texture_name = InputField(text='new_texture')

    tw = WindowPanel(
        title='Texture',
        content=(
            Text('Texture Path:'),
            texture_name,
            Button(text='Submit', color=color.azure, on_click=textures),
            Button(text='Close', color=color.red, on_click=hide_tw)
        ),
    )

    tw.y = tw.panel.scale_y / 2 * tw.scale_y


def open_sound_editor():
    print("Coming soon...")


def set_x():
    editor_camera.rotation = (0, 0, 0)


def set_y():
    editor_camera.rotation = (0, 90, 0)


def set_z():
    editor_camera.rotation = (90, 0, 0)


def render_image():
    # base = application.base

    # editor_camera.position = 0, 5, -24

    # base.screenshot(namePrefix=f"render_{project_name}.png", defaultFilename=0)
    # print_on_screen("Render finished !", scale=2, position=(-0.1, 0))
    # editor_camera.enabled = False

    editor_camera.world_position = (cameraEntity.x, cameraEntity.y, 0)
    editor_camera.rotation = (cameraEntity.rotation_z, 90, 0)


def render_video():
    vd_rec = VideoRecorderUI()
    vd_rec.visible = True


def open_model_obj():
    fb = FileBrowser(file_types='.obj', enabled=True)

    def on_submit(paths):
        for p in paths:
            print(p)
            model1 = load_model(p, use_deepcopy=True)

    fb.on_submit = on_submit


def open_model_gltf():
    fb = FileBrowser(file_types='.gltf', enabled=True)

    def on_submit(paths):
        for p in paths:
            print(p)
            model1 = load_model(p.name, use_deepcopy=True)

    fb.on_submit = on_submit


def rename_project():
    def hide_wpr():
        destroy(wpr)

    def rename_w():
        global project_name
        new_project_name = name_input.text
        if len(new_project_name) <= 9:
            project_name = new_project_name
        else:
            print_on_screen(text="Your name is too long", scale=2, position=(-0.2, 0, 0))

    name_input = InputField(name='name_field')

    wpr = WindowPanel(
        title='Rename Project',
        content=(
            Text('Name:'),
            name_input,
            Button(text='Submit', color=color.azure, on_click=rename_w),
            Button(text='Close', color=color.red, on_click=hide_wpr)
        ),
    )
    wpr.y = wpr.panel.scale_y / 2 * wpr.scale_y


def open_project():
    destroy(wp)
    fb = FileBrowser(file_types='.msstd', enabled=True, z=-5)

    def on_submit(paths):
        global project_name, editor_camera
        print('--------', paths)
        for p in paths:
            print('---', p)

            with open(f'{p}') as f:
                data = json.load(f)

            print(data)

            try:
                project_name = data['project']['name']

                editor_camera.rotation_x = data['project']['camera']['rotation']['x']
                editor_camera.rotation_y = data['project']['camera']['rotation']['y']
                editor_camera.rotation_z = data['project']['camera']['rotation']['z']

                print(data['project']['camera']['position']['x'])
                print(data['project']['models'])
            except json.decoder.JSONDecodeError:
                print_warning("Your project is corrupt !")
                print_on_screen("Your project is corrupt !", scale=2, position=(-0.3, 0))

    fb.on_submit = on_submit


def save_project():
    wps = FileBrowserSave(file_type='.msstd', z=-5)

    import json
    save_data = {
        "project": {
            "name": f'{project_name}',
            "camera": {
                "position": {
                    "x": editor_camera.x,
                    "y": editor_camera.y,
                    "z": editor_camera.z
                },
                "rotation": {
                    "x": 0,
                    "y": 0,
                    "z": 0
                }
            },
            "models": f'{cube_list}'
        }
    }
    wps.data = json.dumps(save_data)


def general_mode():
    axis_x.visible = True
    axis_y.visible = True
    axis_z.visible = True
    floor.visible = True
    footer.visible = True
    slider.visible = True
    right.visible = True


def texture_edit():
    def hide_pe():
        destroy(exit_button)
        pe.visible, pe.enabled = False, False

        empty_texture.save("new_texture.png")

        axis_x.visible = True
        axis_y.visible = True
        axis_z.visible = True
        floor.visible = True
        footer.visible = True
        slider.visible = True
        right.visible = True
        texture_scale.visible = True

    destroy(wp)
    empty_texture = Texture(Image.new(mode='RGBA',
                                      size=(32, 32),
                                      color=(255, 255, 255, 255)))

    texture_scale = TextField(parent=camera.ui, ignore_paused=True, origin=(.5, .5), y=-0.5, x=-0.614,
                              z=-1)

    pe.enabled = True
    pe.visible = True
    pe.texture = empty_texture

    axis_x.visible = False
    axis_y.visible = False
    axis_z.visible = False
    floor.visible = False
    footer.visible = False
    slider.visible = False
    right.visible = False
    texture_scale.visible = False

    exit_button = Button(parent=camera.ui, ignore_paused=True, origin=(.5, .5), y=0.5, x=0.614,
                         z=-1, scale=(.05, .025), color=color.red.tint(-.2), text='x',
                         on_click=hide_pe, name='exit_button')


def open_texture():
    bd = {}
    # TextureUI(bd)


def show_texture():
    def test(txt_arg: str):
        cube.texture = txt_arg
        sphere.texture = txt_arg

    button_dict = {}

    bl = ButtonList(button_dict, font='VeraMono.ttf', button_height=1.5, popup=True)

    bl.button_dict = {
        'noise': Func(test, 'noise'),
        'grass': Func(test, 'grass'),
        'vignette': Func(test, 'vignette'),
        'arrow_right': Func(test, 'arrow_right'),
        'test_tileset': Func(test, 'test_tileset'),
        'tilemap_test_level': Func(test, 'tilemap_test_level'),
        'shore': Func(test, 'shore'),
        'file_icon': Func(test, 'file_icon'),
        'sky_sunset': Func(test, 'sky_sunset'),
        'radial_gradient': Func(test, 'radial_gradient'),
        'circle': Func(test, 'circle'),
        'perlin_noise': Func(test, 'perlin_noise'),
        'brick': Func(test, 'brick'),
        'grass_tintable': Func(test, 'grass_tintable'),
        'circle_outlined': Func(test, 'circle_outlined'),
        'ursina_logo': Func(test, 'ursina_logo'),
        'arrow_down': Func(test, 'arrow_down'),
        'cog': Func(test, 'cog'),
        'vertical_gradient': Func(test, 'vertical_gradient'),
        'white_cube': Func(test, 'white_cube'),
        'horizontal_gradient': Func(test, 'horizontal_gradient'),
        'folder': Func(test, 'folder'),
        'rainbow': Func(test, 'rainbow'),
        'heightmap_1': Func(test, 'heightmap_1'),
        'sky_default': Func(test, 'sky_default'),
    }

    cube = Entity(parent=camera.ui, model="cube", scale=.22, x=-0.45, y=.13)
    sphere = Entity(parent=camera.ui, model="sphere", scale=.22, x=-0.45, y=-.13)

    Entity(model="quad", scale=(999, 999), color=color.black66, z=999)


def convert_code():
    with open('_convert_file.txt', 'w') as convert:
        clean_cube_nmb = str(cube_list).strip('[]') + '\n'
        convert.write(clean_cube_nmb)

    convert.close()


def edit_mode():
    def show_vert():
        axis_x.visible = False
        axis_y.visible = False
        axis_z.visible = False
        floor.visible = False
        footer.visible = False
        slider.visible = False
        right.visible = False

        m = load_model("Assets/models/cube.obj", use_deepcopy=True)
        for t in m.vertices:
            Draggable(parent=scene, model="cube", color=color.blue, scale=0.08, position=t)

    show_vert()


def physic_mode():
    global physic

    if physic is False:
        physic = True
        ground.visible = True
    elif physic is True:
        physic = False
        ground.visible = False
        destroy(physic_nmb)
        physic_nmb.clear()


plane = Entity(name="plane_shaders", model='plane', scale=50, color=color.gray, shader=lit_with_shadows_shader,
               visible=False)


def shaders_active():
    sun_l = None
    if plane.visible is False:
        axis_x.visible = False
        axis_y.visible = False
        axis_z.visible = False
        floor.visible = False
        footer.visible = False
        slider.visible = False
        right.visible = False

        EditorCamera()

        plane.visible = True

        sun_l = Sun(target=origin)
    else:
        axis_x.visible = True
        axis_y.visible = True
        axis_z.visible = True
        floor.visible = True
        footer.visible = True
        slider.visible = True
        right.visible = True

        plane.visible = False

        destroy(sun_l)


def preferences():
    def hide_wpr():
        destroy(wpr)

    def apply():
        try:
            if sky_input.value == 1:
                sky.texture = 'sky_sunset'
            else:
                sky.texture = 'sky_default'
        except Exception as e:
            print_warning(f"Error: {e}")

    project_input = InputField()
    plugin_input = InputField()
    sky_input = Slider(0, 1, step=1)

    wpr = WindowPanel(
        title='Preferences',
        content=(
            Text('Project Path'),
            project_input,
            Text('Import Plugin'),
            plugin_input,
            Text('Sky Texture Path'),
            sky_input,
            Button(text='Save', color=color.azure, on_click=apply()),
            Button(text='Close', color=color.red, on_click=hide_wpr)
        ),
    )

    wpr.y = wpr.panel.scale_y / 2 * wpr.scale_y


def timeline_options():
    def hide_wpt():
        destroy(wpt)

    def apply():
        global timeline_speed
        timeline_speed = speed_slider.value

        hide_wpt()

    step_slider = Slider(.4, 2, step=0.2, radius=0.05)
    speed_slider = Slider(0.5, 5, step=0.5, radius=0.05)

    destroy(wp)

    wpt = WindowPanel(
        title='Timeline Options',
        content=(
            Text('Timeline Step'),
            step_slider,
            Text('Animation Speed'),
            speed_slider,
            Button(text='Apply', color=color.azure, on_click=apply),
            Button(text='Close', color=color.red, on_click=hide_wpt)
        ),
    )

    wpt.y = wpt.panel.scale_y / 2 * wpt.scale_y


def physics_options():
    def hide_wpt():
        destroy(wpt)

    def apply():
        world.setGravity(Vec3(0, -gravity_slider.value, 0))

        hide_wpt()

    gravity_slider = Slider(0.1, 10, step=0.1, radius=0.05)

    destroy(wp)

    wpt = WindowPanel(
        title='Physics Options',
        content=(
            Text('Gravity'),
            gravity_slider,
            Button(text='Apply', color=color.azure, on_click=apply),
            Button(text='Close', color=color.red, on_click=hide_wpt)
        ),
    )

    wpt.y = wpt.panel.scale_y / 2 * wpt.scale_y


def QUIT():
    if save is False:
        WindowPanel(popup=True,
                    title="Do you want to unsaved your project ?",
                    scale=(.7, .08),
                    position=(0, .2, -1),
                    content=[
                        Button(text="No", color=color.azure, on_click=save_project),
                        Button(text="Yes", color=color.red.tint(-.2), on_click=application.quit)
                    ],
                    CalcAndAddTextLines=True, ToAddHeight=0
                    )


wp = WindowPanel(
    y=.3,
    lock=(1, 1, 1),
    title='Info Project',
    content=(
        Text('Name:'),
        Button(text='General', color=color.azure, on_click=hide_w),
        Button(text='Texture Edit', color=color.azure, on_click=texture_edit),
        Button(text='SFX', color=color.azure, on_click=open_sound_editor),
        Button(text='Open', color=color.azure, on_click=open_project),
        Button(text='Close', color=color.red, on_click=hide_w),
        Text(text="Version 1.5.5", size=Text.size / 1.5)
    )
)

file = DropdownMenu('File', buttons=(
    DropdownMenuButton('New', on_click=new_project),
    DropdownMenuButton('Open', on_click=open_project),
    DropdownMenuButton('Rename Project', on_click=rename_project),
    DropdownMenuButton('Save', color=color.rgb(0, 100, 0), on_click=save_project),
    DropdownMenu('Import', buttons=(
        DropdownMenuButton('OBJ', on_click=open_model_obj),
        DropdownMenuButton('GLTF', on_click=open_model_gltf),
    )),
    DropdownMenuButton('Preferences', on_click=preferences),
    DropdownMenuButton('Timeline Options', on_click=timeline_options),
    DropdownMenuButton('Physics Options', on_click=physics_options),
    DropdownMenuButton('Exit', color=color.rgb(75, 0, 0), on_click=QUIT),
))
edit_ui = DropdownMenu('Edit', buttons=(
    DropdownMenu('Add', buttons=(
        DropdownMenuButton('Cube', on_click=Func("AddEntity", model="cube")),
        DropdownMenuButton('Sphere', on_click=Func("AddEntity", model="sphere")),
        DropdownMenuButton('Plane', on_click=Func("", model="plane")),
        DropdownMenuButton('Quad', on_click=Func("AddEntity", model="quad")),
        DropdownMenuButton('Circle', on_click=Func("AddEntity", model="circle")),
        DropdownMenuButton('Mesh', on_click=Func("AddEntity", model="cube")),
    )),
    DropdownMenu('Quick Build', buttons=(
        DropdownMenuButton('Diamond', on_click=Func("AddEntity", model="diamond")),
        DropdownMenuButton('Icosphere', on_click=Func("AddEntity", model="icosphere")),
        DropdownMenuButton('Arrow', on_click=Func("AddEntity", model="arrow")),
    )),
    DropdownMenu('Quick Effects', buttons=(
        DropdownMenuButton('RigidBody', on_click=Func(custom_effect, "rigidbody")),
        DropdownMenuButton('Physics Wall', on_click=Func(custom_effect, "wall")),
        DropdownMenuButton('///'),
    )),
    DropdownMenuButton('Textures Folder', on_click=open_texture),
    DropdownMenuButton('Show All Textures', on_click=show_texture),
    DropdownMenuButton('Convert into code', on_click=convert_code)
))
render_ui = DropdownMenu('Render', buttons=(
    DropdownMenuButton('Render Image', on_click=render_image),
    DropdownMenuButton('Render Video', on_click=render_video)
))
mode_ui = DropdownMenu('Mode', buttons=(
    DropdownMenuButton('Object Mode', on_click=general_mode),
    DropdownMenuButton('Edit Mode', on_click=edit_mode),
    DropdownMenuButton('Physics Mode', on_click=physic_mode),
    DropdownMenuButton('Edit Texture', on_click=texture_edit),
))
shaders_ui = DropdownMenu('Shaders', buttons=(
    DropdownMenuButton('No Light', on_click=shaders_active),
    DropdownMenuButton('With Light', on_click=shaders_active)
))

edit_ui.x = window.top_left.x + .23
render_ui.x = window.top_left.x + .459
mode_ui.x = window.top_left.x + .688
shaders_ui.x = window.top_left.x + .918

footer = Entity(parent=camera.ui, scale=(1.95, 0.3), model=Quad(aspect=3, radius=0), color=color.black50, y=-0.4)
right = Entity(parent=camera.ui, scale=(0.3, 0.9), model=Quad(aspect=3, radius=0), color=color.black66,
               position=(0.75, 0.2))

# Help Keybind

Text(
    text=dedent('''
               shift + a:            object panel
               ctrl + o:             open project
               ctrl + s:             save project
               ctrl + t:             set texture
           '''),
    position=(-0.89, 0.39),
    scale=.75,
    visible=False
)

# Footer

WorldGrid()

axis_x = Entity(model='cube', scale=(0.015, 0.015, 100), color=color.red, rotation=(0, 90, 0))
axis_y = Entity(model='cube', scale=(0.015, 0.015, 100), color=color.green, rotation=(0, 0, 0))
axis_z = Entity(model='cube', scale=(0.015, 100, 0.015), color=color.blue, rotation=(0, 90, 0))

# axis_y = Entity(model=Mesh(vertices=[Vec3(0, 1000, 0), Vec3(0, -1000, 0)], mode='line', thickness=8),
#                 color=rgb(220, 0, 0))
# axis_x = Entity(model=Mesh(vertices=[Vec3(1000, 0, 0), Vec3(-1000, 0, 0)], mode='line', thickness=8),
#                 color=rgb(0, 220, 0))
# axis_z = Entity(model=Mesh(vertices=[Vec3(0, 0, 1000), Vec3(0, 0, -1000)], mode='line', thickness=8),
#                 color=rgb(0, 0, 220))

Button(parent=footer, text="Add", scale=(0.1, 0.2), radius=0, x=-0.4, y=0.25, on_click=add)
Button(parent=footer, text="Rename", scale=(0.1, 0.2), radius=0, x=-0.4, y=0, on_click=rename_object)
Button(parent=footer, text="Remove", scale=(0.1, 0.2), radius=0, x=-0.4, y=-0.25, on_click=remove_cube)

button_x = Button(parent=footer, text=f"Change Color", scale=(0.1, 0.2), radius=0, x=-0.27, y=0.25,
                  on_click=change_color)
button_y = Button(parent=footer, text=f"Change Name", scale=(0.1, 0.2), radius=0, x=-0.27, y=0)
button_z = Button(parent=footer, text=f"Delete All", scale=(0.1, 0.2), radius=0, x=-0.27, y=-0.25,
                  on_click=Func(remove_cube, 'all_cube'))

Button(parent=footer, text="X", scale=(0.1, 0.2), radius=0, x=-0.15, y=0.25, on_click=set_x)
Button(parent=footer, text="Y", scale=(0.1, 0.2), radius=0, x=-0.15, y=0, on_click=set_y)
Button(parent=footer, text="Z", scale=(0.1, 0.2), radius=0, x=-0.15, y=-0.25, on_click=set_z)

slider = Timeline(1, 359, text='Timeline', default=0, height=Text.size * 6, y=-0.4, step=1,
                  vertical=False, radius=0, list_to_anim=cube_list)

# Right

Text(parent=right, text='Project Info', scale=(3, 1.4), x=-0.33, y=0.33, z=-1)

project_text = Text(parent=right, text=f'Project Name: {project_name}', scale=(2.5, 1), x=-0.5, y=0.23, z=-1)

Text(parent=right, text='Camera Info', scale=(3, 1.5), x=-0.20, y=0.2, z=-1)
camera_text = Text(parent=right, text=f'Camera Position: {camera.position}', scale=(2.5, 1), x=-0.5, y=0.13, z=-1)
camera_rotation = Text(parent=right, text=f'Camera Position: {camera.rotation}', scale=(2.5, 1), x=-0.5, y=0.1, z=-1)

Text(parent=right, text='Object Info', scale=(3, 1.4), x=-0.20, y=0.04, z=-1)
cube_text = Text(parent=right, text=f'Object Name: None', scale=(2.5, 1), x=-0.5, y=-0.01, z=-1)
cube_position = Text(parent=right, text=f'Object Position: 0, 0, 0', scale=(2.5, 1), x=-0.5, y=-0.04, z=-1)
cube_rotation = Text(parent=right, text=f'Object Rotation: 0, 0, 0', scale=(2.5, 1), x=-0.5, y=-0.07, z=-1)
cube_scale = Text(parent=right, text=f'Object Scale: 0, 0, 0', scale=(2.5, 1), x=-0.5, y=-0.1, z=-1)
cube_texture = Text(parent=right, text=f'Object Texture: 0, 0, 0', scale=(2.5, 1), x=-0.5, y=-0.125, z=-1)

origin = Entity(model='sphere', color=color.orange, scale=0.02)

cameraEntity = Draggable(parent=scene, name="Camera", model="camera.obj", collider="mesh", scale=0.5,
                         rotation=(0, 0, 45),
                         position=(-8, 5, 0), color=color.black66)


def input(key):
    global save

    if held_keys['shift'] and key == "q":
        add()
    if held_keys['shift'] and key == "t":
        set_texture()
    if held_keys['control'] and key == "p":
        custom_effect("box")
    if held_keys['control'] and key == "s":
        save_project()
        save = True

    if held_keys['control'] and key == "o":
        open_project()
    if held_keys['control'] and key == "x":
        remove_cube()

    if held_keys['control'] and key == 'scroll up':
        pe.brush_size += 1
        print(pe.brush_size)

    if not pe.brush_size <= 1:
        if held_keys['control'] and key == 'scroll down':
            pe.brush_size -= 1
            print(pe.brush_size)

    if held_keys['space']:
        editor_camera.rotation_x = 27
        if slider.value == 359:
            print_on_screen("FINISH")
        else:
            slider.value += timeline_speed
            editor_camera.rotation_y += -timeline_speed

    if held_keys['right arrow']:
        for cube in cube_list:
            cube.rotation_y -= 1

    if held_keys['right arrow']:
        for cube in cube_list:
            cube.rotation_y += 0.5

    if held_keys['up arrow']:
        for cube in cube_list:
            cube.rotation_x -= 1

    if held_keys['down arrow']:
        for cube in cube_list:
            cube.rotation_x += 1


rot = False

rot_x = Entity(model=Circle(14, mode='line', thickness=8), scale=(1.5, 1.5, 1.5),
               color=color.red,
               position=(0, 0, 0),
               rotation=(0, 90, 0),
               visible=False)
rot_y = Entity(model=Circle(14, mode='line', thickness=8), scale=(1.5, 1.5, 1.5),
               color=color.green,
               position=(0, 0, 0),
               rotation=(0, 0, 0),
               visible=False)
rot_z = Entity(model=Circle(14, mode='line', thickness=8), scale=(1.5, 1.5, 1.5),
               color=color.blue,
               position=(0, 0, 0),
               rotation=(90, 0, 0),
               visible=False)

ClickPanel(key_control=True, key_bind="right mouse", button_text="Add", button2_text="Remove", button3_text="Rename",
           button4_text="Copy", button5_text="Paste", button6_text="Exit")


def update():
    global rot, physic

    if physic is True:
        world.doPhysics(time.dt)

    for cube in cube_list:
        if mouse.hovered_entity == cube:
            cube_text.text = f'Object Name: {cube.name}'
            cube_position.text = f'Object Position: {round(cube.x, 2)}, {round(cube.y, 2)}, {round(cube.z, 2)}'
            cube_rotation.text = f'Object Rotation: {round(cube.rotation_x, 2)}, {round(cube.rotation_y, 2)}, {round(cube.rotation_z, 2)} '
            cube_scale.text = f'Object Scale: {round(cube.scale_x, 2)}, {round(cube.scale_y, 2)}, {round(cube.scale_z, 2)}'
            cube_texture.text = f'Object Texture: {cube.texture}'

            # tooltip_test = Tooltip(
            #    f'''<scale:1.2><gray> {cube.name} <scale:1>
            #    Scale: {cube.scale}
            #    Position: {cube.position}
            # ''',
            #    background_color=color.black33,
            #    font='VeraMono.ttf',
            #    wordwrap=30,
            # )
            # cube.tooltip = tooltip_test

    for cube_physics in physic_nmb:
        if mouse.hovered_entity == cube_physics:
            print(cube_physics.name)
            cube_text.text = f'Object Name: {cube_physics.name}'
            cube_position.text = f'Object Position: {round(cube_physics.x, 2)}, {round(cube_physics.y, 2)}, {round(cube_physics.z, 2)}'
            cube_rotation.text = f'Object Rotation: {round(cube_physics.rotation_x, 2)}, {round(cube_physics.rotation_y, 2)}, {round(cube_physics.rotation_z, 2)} '
            cube_scale.text = f'Object Scale: {round(cube_physics.scale_x, 2)}, {round(cube_physics.scale_y, 2)}, {round(cube_physics.scale_z, 2)}'
            cube_texture.text = f'Object Texture: {cube_physics.texture}'

    if mouse.hovered_entity == cameraEntity:
        cube_text.text = f'Object Name: {cameraEntity.name}'
        cube_position.text = f'Object Position: {round(cameraEntity.x, 2)}, {round(cameraEntity.y, 2)}, {round(cameraEntity.z, 2)}'
        cube_rotation.text = f'Object Rotation: {round(cameraEntity.rotation_x, 2)}, {round(cameraEntity.rotation_y, 2)}, {round(cameraEntity.rotation_z, 2)} '
        cube_scale.text = f'Object Scale: {round(cameraEntity.scale_x, 2)}, {round(cameraEntity.scale_y, 2)}, {round(cameraEntity.scale_z, 2)}'
        cube_texture.text = f'Object Texture: {cameraEntity.texture}'

    if held_keys['s']:
        for cube in cube_list:
            if mouse.hovered_entity == cube:
                cube.scale = (mouse.x * 50, mouse.y * 10, mouse.x * 10)
        for cube_physics in physic_nmb:
            if mouse.hovered_entity == cube_physics:
                cube_physics.scale = (mouse.x * 50, mouse.y * 10, mouse.x * 10)

    if held_keys['r']:
        for cube in cube_list:
            if mouse.hovered_entity == cube and rot is False:
                rot_x.visible, rot_x.parent = True, cube
                rot_y.visible, rot_y.parent = True, cube
                rot_z.visible, rot_z.parent = True, cube
                rot = True

            else:
                rot_x.visible = False
                rot_y.visible = False
                rot_z.visible = False
                rot = False

    if cameraEntity.x > 0 and cameraEntity.y > 0:
        cameraEntity.rotation = (0, 180, 40)
    elif cameraEntity.x < 0 and cameraEntity.y > 0:
        cameraEntity.rotation = (0, 0, 40)
    elif cameraEntity.y < 0 and cameraEntity.x < 0:
        cameraEntity.rotation = (0, 0, -40)
    elif cameraEntity.y > 0 and cameraEntity.x < 0:
        cameraEntity.rotation = (0, 180, -40)

    project_text.text = f'Project Name: {project_name}'
    camera_text.text = f'Camera Position: {round(camera.x)}, {round(camera.y)}, {round(camera.z)}'
    camera_rotation.text = f'Camera Rotation: X: {round(editor_camera.rotation_x)} Y: {round(editor_camera.rotation_y)} Z: {round(editor_camera.rotation_z)} '


app.run()
