from ursina import *
from MeshStudio.ObjectOriented.Gizmo.PositionGizmo import PositionGizmo
from MeshStudio.ObjectOriented.Gizmo.ScaleGizmo import ScaleGizmo


class AddEntity(Entity):
    def __init__(self, parent=scene, model="cube", name="Entity1", color=color.white, scale=(1, 1, 1),
                 texture="white_cube", **kwargs):
        super().__init__(parent=parent, model=model, color=color, name=name, scale=scale, texture=texture, **kwargs)
        self.color = rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        self.positionGizmo = PositionGizmo(self, 0, lambda: ...)
        self.scaleGizmo = ScaleGizmo(self, lambda: ...)

        self.positionGizmo.scale = self.scale / 1
        self.scaleGizmo.scale = self.scale / 1,

        self.positionGizmo.SetUp()
        self.scaleGizmo.SetUp()

        self.positionGizmo.enabled = True
        self.scaleGizmo.enabled = False

        self.EntityName = Text(parent=self, text=name, position=(0, self.scale.y * 2.2, 0), scale=12,
                               origin=(.03, .5),
                               double_sided=True)

        self.globalInformation = f'''
Global Information
    -Entity name: {self.name}
    -Entity Position: {self.position}
    -Entity Rotation: {self.rotation}
    -Entity Scale: {self.scale}'''

        # self.TEXT = Text(text=self.globalInformation, align="left")

    def update(self):
        self.globalInformation = f'''
        Global Information
            -Entity name: {self.name}
            -Entity Position: {self.position}
            -Entity Rotation: {self.rotation}
            -Entity Scale: {self.scale}'''

    def PositionGizmoEnabled(self, Enable: bool):
        if Enable:
            self.positionGizmo.enabled = Enable
            self.scaleGizmo.enabled = False
        else:
            self.positionGizmo.enabled = Enable
            self.scaleGizmo.enabled = True

    def ScaleGizmoEnabled(self, Enable: bool):
        if Enable:
            self.scaleGizmo.enabled = Enable
            self.positionGizmo.enabled = False
        else:
            self.scaleGizmo.enabled = Enable
            self.positionGizmo.enabled = True

    def DestroyGizmo(self):
        destroy(self.positionGizmo, self.scaleGizmo)

    def input(self, key):
        if key == "s" and self.positionGizmo.enabled is True:
            self.PositionGizmoEnabled(False)
        elif key == "s" and self.positionGizmo.enabled is False:
            self.PositionGizmoEnabled(True)


if __name__ == "__main__":
    app = Ursina()

    EditorCamera()

    cube = AddEntity()

    app.run()
