from ursina import *
from MeshStudio.MainFiles.Gizmo.GizmoUpdater import NewDraggable

app = Ursina(borderless=False, fullscreen=False, development_mode=False, vsync=False)

class ScaleGizmo(Entity):
    def __init__(self, Entity, OnDrag, Snapping=0, **kwargs):
        super().__init__()
        self.Entity = Entity
        self._Snapping = Snapping
        self._Sensitivity = 100
        self.OnDrag = OnDrag

        self.GizmoX = NewDraggable(name="scale_x", Num=0, parent=self, axis=(1, 0, 0), RetVal=self.GetVal,
                                   Entity=Entity, lock=(0, 1, 1), scale=(0.5, 0.5, 0.5), rotation=(90, 90, 0),
                                   color=color.red, model=f"../../Assets/Models/ScaleGizmo.obj", collider="mesh",
                                   double_sided=True, step=self._Snapping, sensitivity=self._Sensitivity,
                                   position=Entity.position)
        self.GizmoY = NewDraggable(name="scale_y", Num=1, parent=self, axis=(0, 1, 0), RetVal=self.GetVal,
                                   Entity=Entity, lock=(1, 0, 1), scale=(0.5, 0.5, 0.5), rotation=(0, 90, 0),
                                   color=color.blue, model=f"../../Assets/Models/ScaleGizmo.obj", collider="mesh",
                                   double_sided=True, step=self._Snapping, sensitivity=self._Sensitivity,
                                   position=Entity.position)
        self.GizmoZ = NewDraggable(name="scale_z", Num=2, parent=self, axis=(0, 0, 1), RetVal=self.GetVal,
                                   Entity=Entity, lock=(1, 0, 0), plane_direction=(0, 1, 0), rotation=(90, 90, 90),
                                   scale=(0.5, 0.5, 0.5), color=color.green, model=f"../../Assets/Models/ScaleGizmo.obj",
                                   collider="mesh", double_sided=True, step=self._Snapping,
                                   sensitivity=self._Sensitivity, position=Entity.position)

        self.CurrentlyScaling: Draggable = self.GizmoX

        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def update(self):
        self.position = self.Entity.position

    def GetVal(self, Dist, Num):
        # print(Dist.x)
        if getattr(self.Entity, self.CurrentlyScaling.name) + Dist[Num] > 0:
            if self.CurrentlyScaling.step[0] != 0:
                setattr(self.Entity, self.CurrentlyScaling.name,
                        getattr(self.Entity, self.CurrentlyScaling.name) + Dist[Num])
                self.OnDrag()
                return
            setattr(self.Entity, self.CurrentlyScaling.name,
                    getattr(self.Entity, self.CurrentlyScaling.name) + Dist[Num])
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

    @property
    def Sensitivity(self):
        return self._Sensitivity

    @Sensitivity.setter
    def Sensitivity(self, Value):
        self.GizmoX.sensitivity = Value
        self.GizmoY.sensitivity = Value
        self.GizmoZ.sensitivity = Value
        self._Sensitivity = Value


if __name__ == "__main__":
    a = Entity(model="cube")
    ed = ScaleGizmo(a, lambda: ...)
    ed.SetUp()


    def input(key):
        if key == "1":
            ed.Sensitivity = 100
        elif key == "2":
            ed.Sensitivity = 20
        elif key == "3":
            ed.Sensitivity = 110


    EditorCamera()
    app.run()
