import os
import psutil
import math

from ursina import *
from MeshStudio.ObjectOriented.AddEntity import AddEntity
from MeshStudio.ObjectOriented.WorldDirectionBox import DirectionBox
from MeshStudio.ObjectOriented.WorldGrid import WorldGrid
from MeshStudio.Prefabs.additive_function import MultiFunctionCaller, TextToVar
from MeshStudio.ObjectOriented.Gizmo.GizmoManager import GizmoManager
from MeshStudio.ObjectOriented.ColorMenu import ColorMenu
from MeshStudio.Prefabs.memory_counter import MemoryCounter


class SceneEditor(Entity):
    def __init__(self, ProjectName, ProjectDescription, ParentProjectEditor=scene, **kwargs):
        super().__init__(kwargs)
        self.ProjectName = ProjectName
        self.ProjectDescription = ProjectDescription
        self.EditorCamera = EditorCamera()
        self.sky = Sky(texture="sky_default")
        self.CurrentGizmo: str = "PositionGizmo"

        self.GizmoManager: GizmoManager = GizmoManager()

        self.WorldItems = []
        self.ParentProjectEditor = ParentProjectEditor
        self.MemoryCounter = MemoryCounter()
        self.Setup()

        self.AddObjectTextList = ["Add static object", "Add dynamic object", "Add FPC", "Add TPC", "Add abstraction"]
        self.AddObjectOnClickFuncList = [self.AddEntityInScene, self.AddEntityInScene, self.AddEntityInScene,
                                         self.AddEntityInScene, self.AddEntityInScene]
        self.BasicFunctions = ["Name: ", "Parent: ", "Position x: ", "Position y: ", "Position z: ", "Rotation x: ",
                               "Rotation y: ", "Rotation z: ", "Scale x: ", "Scale y: ", "Scale z: ", "Color: ",
                               "Model: ", "Texture: ", "Texture scale: "]
        self.SpecialFunctions: dict = {
            "Color: ": lambda Obj, Parent, i: ColorMenu(Obj, (2.5, 15), BGPos=(1, 1, 0), scale=(.5, .05), parent=Parent,
                                                        y=-i * 0.08 + .34, z=-20, x=.13, radius=1).SetUp()}

        self.SpecialExtractingMethods: dict = {"Parent: ": (
            lambda Field: setattr(Field.Obj, "parent", scene), lambda Filed: ...,
            lambda Field: (getattr(Field.Obj.parent, "name")),
            "1234567890qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_", True),
            "Name: ": (
                lambda Field: setattr(Field.Obj, 'name', Field.text), lambda Field: ...,
                lambda Field: (getattr(Field.Obj, "name")),
                "1234567890qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_", True),
            "Model: ": (
                lambda Field: setattr(Field.Obj, 'model', Field.text), lambda Field: ...,
                lambda Field: (getattr(Field.Obj.model, "name")),
                "1234567890qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_./({[]})",
                True),
            "Texture: ": (lambda Field: setattr(Field.Obj, 'texture', Field.text),
                          lambda Field: ...,
                          lambda Field: getattr(Field.Obj, "texture"),
                          "1234567890qwertyuiopasdfghklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_./({[]})",
                          True),
            "Texture scale: ": (
                lambda Field: setattr(Field.Obj, 'texture_scale', eval(Field.text)),
                lambda Field: setattr(Field, 'text', str(Field.Obj.texture_scale)),
                lambda Field: getattr(Field.Obj, "texture_scale"), "1234567890()Vec.,",
                True),

            "Rotation x: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "rotation",
                     Vec3(eval(Filed.text), Filed.Obj.rotation_y,
                          Filed.Obj.rotation_z))),
                             lambda Field: setattr(Field, "text",
                                                   str(Field.Obj.rotation_x)),
                             lambda Filed: str(getattr(Filed.Obj.rotation, "x")),
                             "1234567890.-", False),
            "Rotation y: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "rotation",
                     Vec3(Filed.Obj.rotation_x, eval(Filed.text),
                          Filed.Obj.rotation_z))),
                             lambda Filed: setattr(Filed, "text",
                                                   str(Filed.Obj.rotation_y)),
                             lambda Filed: str(getattr(Filed.Obj.rotation, "y")),
                             "1234567890.-", False),
            "Rotation z: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "rotation",
                     Vec3(Filed.Obj.rotation_x, Filed.Obj.rotation_y,
                          eval(Filed.text)))), lambda Filed: setattr(Filed, "text",
                                                                     str(Filed.Obj.rotation_z)),
                             lambda Filed: str(getattr(Filed.Obj.rotation, "z")),
                             "1234567890.-", False),

            "Scale x: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "scale_x", eval(Filed.text))),
                          lambda Field: setattr(Field, "text",
                                                str(Field.Obj.scale_x)),
                          lambda Filed: str(getattr(Filed.Obj.scale, "x")),
                          "1234567890.-", False),
            "Scale y: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "scale_y", eval(Filed.text))),
                          lambda Filed: setattr(Filed, "text",
                                                str(Filed.Obj.scale_y)),
                          lambda Filed: str(getattr(Filed.Obj.scale, "y")),
                          "1234567890.-", False),
            "Scale z: ": (lambda Filed: MultiFunctionCaller(
                Func(setattr, Filed.Obj, "scale_z", eval(Filed.text))),
                          lambda Filed: setattr(Filed, "text",
                                                str(Filed.Obj.scale.z)),
                          lambda Filed: str(getattr(Filed.Obj.scale, "z")),
                          "1234567890.-", False)}

        self.UniversalParentEntity = Entity(parent=camera.ui, enabled=True)
        self.SideBarTopParentEntity = Entity(parent=self.UniversalParentEntity, model="cube",
                                             position=window.top_right - 0.12, scale=Vec3(0.45, 0.65, 2),
                                             color=color.gray)
        self.SideBarTopSlideHandler = Button(name="GlobalEntityInfo", parent=self.SideBarTopParentEntity, model="cube", radius=0,
                                             visible_self=False,
                                             y=-0.22, z=-200)

        self.ObjetInformationParentEntity = Entity(parent=self.UniversalParentEntity, scale=(55 / 80, window.size.y),
                                                   model=Quad(aspect=3, radius=0), color=color.tint(color.gray, -.1),
                                                   position=window.right)
        self.TimelineParentEntity = Entity(parent=camera.ui, scale=(0.45, 51 / 900),
                                           position=(-0.688, -0.3, 0),
                                           model=Quad(aspect=3, radius=0), color=color.gray, )

        self.WorldGrid = WorldGrid()

        self.DirectionEntity = DirectionBox(parent=camera.ui, camera=self.EditorCamera, enabled=True,
                                            always_on_top=True, render_queue=1,
                                            position=window.top_right - Vec2(.49, .1))

        self.AddEntityInScene()

    def AddEntityInScene(self):
        self.WorldItems.append(
            AddEntity())
        #Entity(name=f"item_{len(self.WorldItems)}", parent=scene, model="cube", texture="white_cube",
        #collider="mesh", collision=True, color=color.white))
        self.ShowObjectContent(self.WorldItems[-1], self.SideBarTopSlideHandler)
        #self.AddGizmoTo(self.WorldItems[len(self.WorldItems) - 1])

        print(self.WorldItems[len(self.WorldItems) - 1])

    def ShowObjectContent(self, Obj, Parent: Entity):
        self.TempLen = len(Parent.children)
        for i in range(self.TempLen - 1, -1, -1):
            destroy(Parent.children[i])
        del self.TempLen
        Parent.children = []

        Text(parent=Parent, text=type(Obj).__name__, scale=3, origin=(0, 0), y=.45, z=20, scale_x=3.5)
        Entity(name="Line", parent=Parent, model="line", color=color.black, scale=Vec3(0.99, 1.02, 1),
               position=Vec3(0.01, 0.39, 20))

        for i in range(len(self.BasicFunctions)):
            Text(parent=Parent, text=f"{self.BasicFunctions[i]}", scale=2, y=-i * 0.08 + .36, z=20, x=-.47)

        for i in range(len(self.BasicFunctions)):
            if self.BasicFunctions[i] in self.SpecialFunctions.keys():
                self.SpecialFunctions[self.BasicFunctions[i]](Obj, Parent, i)
            else:
                def UpdateFieldContent(field):
                    if field.active:
                        return

                    if type(getattr(field.Obj, field.name)) in (int, float) and not self.IsFieldActive:
                        # if getattr(Obj,field.name) == field.text:
                        field.text = f"{round(getattr(field.Obj, field.name), 11)}"

                TempChild = InputField(submit_on=["enter", "escape"], parent=Parent, y=-i * 0.08 + .34, z=-20, x=.13,
                                       active=False, text_scale=.75, cursor_y=.1, enter_active=True, character_limit=13,
                                       Obj=Obj)

                if self.BasicFunctions[i] in self.SpecialExtractingMethods.keys():
                    TempChild.SetNewValue = self.SpecialExtractingMethods[self.BasicFunctions[i]][0]
                    TempChild.DumpValue = self.SpecialExtractingMethods[self.BasicFunctions[i]][2]
                    TempChild.limit_content_to = self.SpecialExtractingMethods[self.BasicFunctions[i]][3]
                    TempChild.text = f"{TempChild.DumpValue(TempChild)}"
                    TempChild.on_submit = Func(TempChild.SetNewValue, TempChild)
                    if self.SpecialExtractingMethods[self.BasicFunctions[i]][4]:

                        TempChild.ToUpdateOnEnter = Func(MultiFunctionCaller,
                                                         Func(self.SpecialExtractingMethods[self.BasicFunctions[i]][1],
                                                              TempChild), Func(self.UpdateItemContent, Obj, Parent))

                    else:
                        TempChild.UpdateContent = self.SpecialExtractingMethods[self.BasicFunctions[i]][1]

                else:
                    def TryExtractData(Field):
                        return float(Field.text)

                    TempChild.text = f"{getattr(Obj, TextToVar(self.BasicFunctions[i], '_'))}"
                    TempChild.ExtractData = TryExtractData
                    TempChild.name = TextToVar(self.BasicFunctions[i], '_')

                    def ReturnName(field):
                        return setattr(field.Obj, f"{field.name}", eval(field.text))

                    TempChild.SetNewValue = ReturnName

                    TempChild.UpdateContent = UpdateFieldContent
                    TempChild.on_submit = Func(self.UpdateItemContent, Obj, Parent)

    def UpdateItemContent(self, Obj, Parent):
        for i in range((len(Parent.children))):
            try:
                if hasattr(Parent.children[i], "SetNewValue"):
                    Parent.children[i].SetNewValue(Parent.children[i])

            except Exception as e:
                self.ShowInstructionFunc(Title="Error", Str=f"you got {type(e).__name__} error: {e}")

    def AddGizmoTo(self, Entity):
        self.ShowObjectContent(Entity, self.SideBarTopSlideHandler)
        self.ToEditEntity = Entity
        # self.GizmoManager.OnDrag = self.SideBarTopParentEntity.UpdateField
        self.GizmoManager.AddGizmo(self.ToEditEntity, self.CurrentGizmo)

    def inputUni(self, key):
        if key == "left mouse up":
            self.SideBarTopParentEntity.UpdateIsFieldActive()
            if not self.IsEditing or self.IsFieldActive:
                return
            if mouse.hovered_entity in self.WorldItems:
                self.AddGizmoTo(mouse.hovered_entity)

    def update(self):
        pass

    def GetState(self):
        return {"GizmoState": {"Type": self.CurrentGizmo, "Snapping": self.GizmoManager.CurrentGizmo.Snapping,
                               "Entity": self.GizmoManager.CurrentGizmoEntity},
                "CamState": {"Position": self.EditorCamera.position, "Rotation": self.EditorCamera.rotation}}

    def SetState(self, State):
        self.CurrentGizmo = State["GizmoState"]["Type"]

        if State["GizmoState"]["Entity"] is not None:
            for entity in self.WorldItems:
                name = re.search(r"name='([^']*)'", State["GizmoState"]["Entity"]['args']).group(1)
                if str(entity) == str(name):
                    self.ToEditEntity = entity
                    self.AddGizmoTo(entity)
                    self.GizmoManager.CurrentGizmo.Snapping = State["GizmoState"]["Snapping"]
                    self.ParentProjectEditor.OnGizmoUpdated()

        self.EditorCamera.position = State["CamState"]["Position"]
        self.EditorCamera.rotation = State["CamState"]["Rotation"]

    def MakeEditorEnvironment(self, cam, color, size):
        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255)

    def Setup(self):
        def UpdateField():
            for child in self.SideBarTopSlideHandler.children:
                if type(child) == InputField and hasattr(child, "UpdateContent"):
                    child.UpdateContent(child)

        #self.SideBarTopParentEntity.UpdateField = UpdateField


if __name__ == "__main__":
    app = Ursina()
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    se = SceneEditor("My First Porject", "Nothing")
    se.Setup()

    app.run()
