import json
from ursina import *


class KeyframesManager:
    def __init__(self):
        self.data = {'frame': {}}
        self.load_keyframes()

    def load_keyframes(self):
        try:
            with open('keyframes.json', 'r') as json_file:
                self.data = json.load(json_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.save_keyframes()  # Créer un fichier avec des données par défaut

    def save_keyframes(self):
        with open('keyframes.json', 'w') as json_file:
            json.dump(self.data, json_file, indent=3, default=self.default_encoder)

    def default_encoder(self, obj):
        if isinstance(obj, Vec3):
            return obj.x, obj.y, obj.z
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

    def add_key(self, list_to_add, key_number):
        if str(key_number) in self.data['frame']:
            self.data['frame'][str(key_number)] = list_to_add
            self.save_keyframes()
        else:
            self.data['frame'][str(key_number)] = list_to_add
            self.save_keyframes()

    def remove_key(self, key_number):
        if str(key_number) in self.data['frame']:
            del self.data['frame'][str(key_number)]
            self.save_keyframes()
        else:
            print(f"Keyframe {key_number} does not exist.")

    def update_keyframe(self, key_number, list_to_update):
        if str(key_number) in self.data['frame']:
            self.data['frame'][str(key_number)] = list_to_update
            self.save_keyframes()
        else:
            print(f"Keyframe {key_number} does not exist.")


class Timeline(Entity):
    def __init__(self, min=0, max=100, default=None, width=.525, height=Text.size, text='', dynamic=False,
                 bar_color=color.black66, list_to_anim=list, **kwargs):
        super().__init__(add_to_scene_entities=False)  # add later, when __init__ is done
        if list_to_anim is None:
            list_to_anim = []
        self.parent = camera.ui
        self.vertical = False
        self.min = min
        self.max = max
        self.width = width
        self.list_to_anim = list_to_anim
        self.keyframes_manager = KeyframesManager()

        if default is None:
            default = min
        self.default = default
        self.step = 0
        self.height = height

        self.on_value_changed = None  # set this to a function you want to be called when the slider changes
        self.setattr = None  # set this to (object, 'attrname') to set that value when the slider changes

        self.label = Text(parent=self, origin=(0.5, 0), x=-0.025, text=text)

        self.bg = Entity(parent=self, model=Quad(scale=(width, height), radius=0, segments=3),
                         origin_x=-0.25, collider='box', color=bar_color)

        self.knob = Draggable(parent=self,
                              min_x=0, max_x=0.5,
                              min_y=0, max_y=.5,
                              step=self.step,
                              model=Quad(radius=0, scale=(0.01, height)), collider='box', color=color.light_gray,
                              text='0', text_origin=(0, -.55), z=-.1)

        self.add_key_button = Button(parent=self, scale=(0.125 / 1.2, 0.125 / 1.2), text="Add", x=0.625,
                                     radius=0, on_click=self.add_keyframes)

        self.kf = Button(parent=self, scale=(0.01, 0.01), rotation=(0, 0, 45), radius=0, color=color.white, disabled=True,
                         visible=False)

        print(self.height, self.scale_x)

        def bg_click():
            self.knob.x = mouse.point[0]
            self.knob.start_dragging()

        self.bg.on_click = bg_click

        def drop():
            self.knob.z = -.1
            if self.setattr:
                if isinstance(self.setattr[0], dict):  # set value of dict
                    self.setattr[0][self.setattr[1]] = self.value
                else:  # set value of Entity
                    setattr(self.setattr[0], self.setattr[1], self.value)

            if self.on_value_changed:
                self.on_value_changed()

        self.knob.drop = drop
        self._prev_value = self.default
        self.value = self.default
        self.dynamic = dynamic  # if set to True, will call on_value_changed() while dragging. if set to False, will only call on_value_changed() after dragging.

        self.knob.text_entity.text = str(round(self.default, 2))

        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.vertical:
            self.rotation_z = -90
            self.knob.lock = (1, 0, 0)
            self.knob.text_entity.rotation_z = 90
            self.knob.text_entity.position = (.015, 0)
        else:
            self.knob.lock = (0, 1, 1)
            self.knob.text_entity.y

    @property
    def value(self):
        val = lerp(self.min, self.max, self.knob.x * 2)
        if isinstance(self.step, int) and not self.step == 0:
            val = int(round(val, 0))

        return val

    @value.setter
    def value(self, value):
        self.knob.x = (value - self.min) / (self.max - self.min) / 2
        self.slide()

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        self._step = value
        self.knob.step = value / (self.max - self.min) / 2

    def update(self):
        if self.knob.dragging:
            self.slide()

    def slide(self):
        t = self.knob.x / .5

        if self.step > 0:
            if isinstance(self.step, int) or self.step.is_integer():
                self.knob.text_entity.text = str(self.value)

        if self.dynamic and self._prev_value != t:
            if self.on_value_changed:
                self.on_value_changed()

            if self.setattr:
                target_object, attr = self.setattr
                setattr(target_object, attr, self.value)

            self._prev_value = t

        invoke(self._update_text, delay=1 / 60)

    def _update_text(self):
        self.knob.text_entity.text = str(round(self.value, 2))

    def __setattr__(self, name, value):
        if name == 'eternal':
            try:
                self.label.eternal = value
                self.bg.eternal = value
                self.knob.eternal = value
            except:
                pass
        try:
            super().__setattr__(name, value)
        except Exception as e:
            return e

    def add_keyframes(self):
        for cube in self.list_to_anim:
            print(cube.name)

            dict_cube = {
                "model": {
                    "name": str(cube.name),
                    "position": list(cube.position),
                    "scale": list(cube.scale),
                    "color": str(cube.color),
                }
            }

            self.keyframes_manager.add_key(list_to_add=dict_cube, key_number=self.value)

        print(self.value)
        duplicate(self.kf, position=(self.knob.x, self.y), visible=True, x=self.knob.x)
        print(self.knob.x)


if __name__ == '__main__':
    app = Ursina()
    window.borderless = False
    window.fullscreen = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    cube_nmb = []

    slider = Timeline(width=0.525, height=Text.size * 5, x=-0.19, step=1, list_to_anim=cube_nmb)

    cube1 = Draggable(parent=scene, model="cube", color=color.white, name="HELLO", collider="box",
                      position=(0, 0, 0), scale=(1, 1, 1))

    cube_nmb.append(cube1)

    EditorCamera()

    app.run()
