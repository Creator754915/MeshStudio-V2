from ursina import *


class DirectionBox(Entity):
    def __init__(self, parent=camera.ui, position=window.top_right - Vec2(.065, .1), camera=None, scale=.025, **kwargs):
        self.camera = camera
        super().__init__(parent=parent, model="../Assets/Models/WorldDirection.obj", collider='box', texture='white_cube',
                         scale=scale, position=position)
        self.color = color.white
        self.front_text = Text(parent=self, text='-Y', z=-3, scale=40, origin=(0, 0), color=color.green)
        self.back_text = Text(parent=self, text='Y', z=3, scale=40, origin=(0, 0), color=color.green,
                              double_sided=True, rotation=(180, 0, 180))
        self.left_text = Text(parent=self, text='-X', z=0, x=3.3, scale=40, origin=(0, 0), color=color.red,
                              double_sided=True, rotation=(0, 0, 0))
        self.right_text = Text(parent=self, text='X', z=0, x=-3.3, scale=40, origin=(0, 0), color=color.red,
                               double_sided=True, rotation=(0, 0, 0))
        self.top_text = Text(parent=self, text='Z', z=0, y=3.3, scale=40, origin=(0, 0), color=color.blue,
                             double_sided=True, rotation=(0, 0, 0))
        self.bottom_text = Text(parent=self, text='-Z', z=0, y=-3.3, scale=40, origin=(0, 0), color=color.blue,
                                double_sided=True, rotation=(0, 0, 0))

        for key, value in kwargs.items():
            setattr(self, key, value)

    def on_click(self):
        if mouse.normal == Vec3(0, 0, -3):
            self.camera.animate_rotation((0, 0, 0))  # front
        elif mouse.normal == Vec3(0, 0, 3):
            self.camera.animate_rotation((0, 180, 0))  # back
        elif mouse.normal == Vec3(3, 0, 0):
            self.camera.animate_rotation((0, 90, 0))  # right
        elif mouse.normal == Vec3(-3, 0, 0):
            self.camera.animate_rotation((0, -90, 0))  # right
        elif mouse.normal == Vec3(0, 3, 0):
            self.camera.animate_rotation((90, 0, 0))  # top
        elif mouse.normal == Vec3(0, -3, 0):
            self.camera.animate_rotation((-90, 0, 0))  # top

    def update(self):
        self.rotation = -self.camera.rotation
        # print(self.editor_camera.rotation)

    def input(self, key):
        if held_keys['shift']:
            if key == '1':
                self.camera.animate_rotation((0, 0, 0))  # front
            elif key == '2':
                self.camera.animate_rotation((0, 180, 0))  # front
            elif key == '3':
                self.camera.animate_rotation((0, -90, 0))  # left
            elif key == '4':
                self.camera.animate_rotation((0, 90, 0))  # right
            elif key == '5':
                self.camera.animate_rotation((90, 0, 0))  # top
            elif key == '6':
                self.camera.animate_rotation((-90, 0, 0))  # bottom

            # elif key == '7': self.editor_camera.animate_rotation((90,0,0)) # top
            # elif key == '5': self.camera.orthographic = not self.camera.orthographic


if __name__ == "__main__":
    from ursina import *

    app = Ursina()

    ed = EditorCamera()

    DirectionBox(parent=camera.ui, position=(0, 0, 0), camera=ed, enabled=True, z=-30, scale=0.025)

    app.run()
