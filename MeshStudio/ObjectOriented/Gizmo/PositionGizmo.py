import os
import sys
import site
from pathlib import Path

from ursina import *


class PositionGizmo(Entity):
    def __init__(self, Entity, Snapping, OnDrag, **kwargs):
        super().__init__()
        self.Entity = Entity
        self._Snapping = Snapping
        self.OnDrag = OnDrag

        self.GizmoX = Draggable(parent=self, lock=(1, 0, 0), plane_direction=(0, 1, 0), scale=(.5, .5, .5), rotation=(90, 90, 90),
                                color=color.red,
                                model=f"../../Assets/Models/PositionGizmo.obj", collider="mesh", double_sided=True, step=Snapping,
                                position=Entity.position)
        self.GizmoY = Draggable(parent=self, lock=(1, 0, 1), scale=(.5, .5, .5), rotation=(0, 90, 0), color=color.blue,
                                model=f"../../Assets/Models/PositionGizmo.obj", collider="mesh", double_sided=True, step=Snapping,
                                position=Entity.position)
        self.GizmoZ = Draggable(parent=self, lock=(0, 1, 1), rotation=(90, 90, 0),
                                scale=(.5, .5, .5), color=color.green, model=f"../../Assets/Models/PositionGizmo.obj", collider="mesh",
                                double_sided=True, step=Snapping, position=Entity.position)

        self.CurrentlyDragging: Draggable = self.GizmoX

        for attribute, value in kwargs.items():
            setattr(self, attribute, value)

    def update(self):
        if self.CurrentlyDragging.dragging:
            self.Entity.position = self.CurrentlyDragging.position
            self.GizmoX.position = self.CurrentlyDragging.position
            self.GizmoY.position = self.CurrentlyDragging.position
            self.GizmoZ.position = self.CurrentlyDragging.position
            self.OnDrag()

    def SetUp(self):
        self.GizmoX.drag = lambda: setattr(self, "CurrentlyDragging", self.GizmoX)
        self.GizmoY.drag = lambda: setattr(self, "CurrentlyDragging", self.GizmoY)
        self.GizmoZ.drag = lambda: setattr(self, "CurrentlyDragging", self.GizmoZ)
        # self.GizmoX.position = self.Entity.position
        # self.GizmoY.position = self.Entity.position
        # self.GizmoZ.position = self.Entity.position

    @property
    def Snapping(self):
        return self._Snapping

    @Snapping.setter
    def Snapping(self, NewValue):
        self._Snapping = NewValue
        self.GizmoX.step = self._Snapping
        self.GizmoY.step = self._Snapping
        self.GizmoZ.step = self._Snapping

    def GoToEntity(self):
        self.GizmoX.position = self.Entity.position
        self.GizmoY.position = self.Entity.position
        self.GizmoZ.position = self.Entity.position


if __name__ == "__main__":
    app = Ursina()
    print(application.asset_folder)
    a = Entity(model="cube")
    ed = PositionGizmo(a, 0, lambda: ...)
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
