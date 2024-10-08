# from BaseGizmo import BaseGizmoClass
from ursina import *
from MeshStudio.MainFiles.Gizmo.GizmoUpdater import NewDraggable


class RotationGizmo(Entity):
    def __init__(self, Entity, OnDrag, Snapping=0, **kwargs):
        super().__init__()
        self.Entity = Entity
        self._Snapping = Snapping
        self.OnDrag = OnDrag

        self.GizmoX = NewDraggable(name="rotation_x", Num=0, parent=self, RetVal=self.GetVal, Entity=Entity,
                                   lock=(0, 1, 1), scale=2, rotation=(90, 90, 0), color=color.red,
                                   model=Circle(16, mode='line', thickness=12), collider="mesh", double_sided=True,
                                   step=self._Snapping, position=Entity.position)
        self.GizmoY = NewDraggable(name="rotation_y", Num=1, parent=self, RetVal=self.GetVal, Entity=Entity,
                                   lock=(1, 0, 1), scale=2, rotation=(0, 90, 0), color=color.blue,
                                   model=Circle(16, mode='line', thickness=12), collider="mesh", double_sided=True,
                                   step=self._Snapping, position=Entity.position)
        self.GizmoZ = NewDraggable(name="rotation_z", Num=2, parent=self, RetVal=self.GetVal, Entity=Entity,
                                   lock=(1, 0, 0), scale=2, plane_direction=(0, 1, 0), rotation=(0, 0, 90),
                                   color=color.green,
                                   model=Circle(16, mode='line', thickness=12), collider="mesh",
                                   double_sided=True, step=self._Snapping, position=Entity.position)

        self.CurrentlyScaling: Draggable = self.GizmoX

        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def GetVal(self, Dist, Num):
        if Dist[Num] > 0:
            setattr(self.Entity, self.CurrentlyScaling.name, Dist[Num] * 100)
            self.OnDrag()

    def SetUp(self):
        self.GizmoX.drag = lambda: setattr(self, "CurrentlyScaling", self.GizmoX)
        self.GizmoY.drag = lambda: setattr(self, "CurrentlyScaling", self.GizmoY)
        self.GizmoZ.drag = lambda: setattr(self, "CurrentlyScaling", self.GizmoZ)

    def GoToEntity(self):
        self.GizmoX.position = self.Entity.position
        self.GizmoY.position = self.Entity.position
        self.GizmoZ.position = self.Entity.position

    @property
    def Snapping(self):
        return self._Snapping

    @Snapping.setter
    def Snapping(self, NewValue):
        self._Snapping = NewValue
        self.GizmoX.step = self._Snapping
        self.GizmoY.step = self._Snapping
        self.GizmoZ.step = self._Snapping


if __name__ == "__main__":
    app = Ursina()
    a = Entity(model="cube", texture="white_cube")
    ed = RotationGizmo(a, lambda: ...)
    ed.SetUp()


    def input(key):
        if key == "1":
            ed.Snapping = 1
        elif key == "2":
            ed.Snapping = .2
        elif key == "3":
            ed.Snapping = 0


    EditorCamera()
    app.run()
