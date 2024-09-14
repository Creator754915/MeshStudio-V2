from ursina import *
from ursina import invoke
from ursina.color import tint
from MeshStudio.Prefabs.additive_function import CustomWindow, MultiFunctionCaller, RecursivePerformer, \
    CurrentFolderNameReturner
from MeshStudio.ObjectOriented.SceneEditor import SceneEditor
from MeshStudio.ShaderEditor.OpenFile import Openselector, OpenFile


# import site
# from panda3d.core import SamplerState

class ProjectEditor(Entity):
    def __init__(self, enabled=True, **kwargs):
        super().__init__(kwargs)
        self.UDVars = []  # User defined vars (like bye = 2 or helo = 3)
        self.UDFunc = []  # User defined func (any function)
        self.UDSrc = []  # User defined script or run after initializing  the item (like item.add_script(whatever the script is))
        self.UDWindowConfig = []  # User defined configuration to apply to the window
        self.ToImport = {"from ursina import *",
                         "from panda3d.core import AntialiasAttrib"}  # modules to import before the game starts (stored in a set)
        self._ProjectName = ""
        self.CurrentEditor = None
        self.CurrentSceneEditor: SceneEditor = None

        self.EditorCamera = EditorCamera
        self.IsEditing = True
        self.enabled = enabled



    def updateVal(self):
        if len(self.ProjectTabsScrollEntity.children) == 4:
            self.val = self.val - .13
        else:
            self.val = self.val - .096

    def FinishProject(self):
        invoke(self.ShowCustomWindow, ToEnable=self.CancelFinishingProject, Title="Export to py",
               OnEnable=self.ShowFinishProjectMenu,
               CalcAndAddTextLines=False, ToAddHeight=3,
               Content=[Text(
                   "Note: You can later export the project to cpp.\nWhen it is implemented ;)\n\nNote: There will be a folder named 'Exported games'\n           in your selected dir and your game will be saved in \n           that folder in a .py format."),
                   Button(color=color.rgba(255, 255, 255, 125), text="Open file selector",
                          highlight_color=color.blue,
                          on_click=Sequence(Func(self.ExportToPy), Func(self.DestroyCurrentWindow))),
                   Button(color=color.rgba(255, 255, 255, 125), text="Cancel", highlight_color=color.blue,
                          click_to_destroy=True)],
               delay=.1)

    def ShowFinishProjectMenu(self):
        self.EditorCamera.disable()
        for i in range(len(self.CurrentTabs)):
            if isinstance(self.CurrentTabs, SceneEditor):
                self.CurrentTabs[i].IsEditing = False

    def ExportToPy(self):
        self.ExportToPyFunc(Openselector())

    def CancelFinishingProject(self):
        self.EditorCamera.enable()
        for i in range(len(self.CurrentTabs)):
            if isinstance(self.CurrentTabs, SceneEditor):
                self.CurrentTabs[i].IsEditing = True

    def EnableEditor(self, EditorsOldestAncestor):
        EditorsOldestAncestor.enable()
        for i in range(len(EditorsOldestAncestor.children)):
            EditorsOldestAncestor.children[i].enable()
            if len(EditorsOldestAncestor.children[i].children) > 0:
                self.EnableEditor(EditorsOldestAncestor.children[i])

    def ShowCustomWindow(self, ToEnable, OnEnable, Title="Info", CalcAndAddTextLines=True, ToAddHeight=0, Content=None):
        self.CurrentCustomWindow = CustomWindow(ToEnable=ToEnable, title=Title, OnEnable=OnEnable,
                                                CalcAndAddTextLines=CalcAndAddTextLines, ToAddHeight=ToAddHeight,
                                                content=Content, Queue=4)

        self.CurrentCustomWindow.WindowPanelOfQuit.text_entity.render_queue = 5

    def ShowTabMenu(self):
        # print(len(self.CurrentTabs))
        if self.IsEditing:
            if not held_keys["control"] and not held_keys["shift"] and not held_keys["alt"]:
                if round(self.TabsMenuParentEntity.y, 2) == 0.39:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.5, 0), .5)
                    if self.AddEditorToPrjectButtonList.enabled:
                        self.AddEditorToPrjectButtonList.disable()
                        self.AddEditorToPrjectButtonList.Background.disable()

                else:
                    self.TabsMenuParentEntity.animate_position(Vec3(0, 0.39, 0), .5)

    def SaveAllEditors(self):
        self.ShowInstructionFunc("Your project is saved :)", Color=tint(color.white, -.6), Title="Saved!")

    def JumpTabs(self, ToJump):
        if self.CurrentTabs[ToJump] == self.CurrentEditor and len(self.CurrentTabs) > 1:
            return

        self.CurrentEditor.UniversalParentEntity.disable()
        self.CurrentEditor.disable()
        self.CurrentEditor.ignore = True

        if type(self.CurrentEditor).__name__ == "SceneEditor":
            RecursivePerformer(self.CurrentEditor.SpecialEntities, "disable")

        self.CurrentEditor = self.CurrentTabs[ToJump]
        self.CurrentEditor.enable()
        self.CurrentEditor.ignore = False
        RecursivePerformer(self.CurrentEditor.UniversalParentEntity)
        # self.CurrentEditor.SetUp()
        if hasattr(self.CurrentEditor, "MakeEditorEnvironment"):
            if type(self.CurrentEditor).__name__ == "CodeEditorPython":
                self.CurrentEditor.MakeEditorEnvironment(application.base.camNode, (255, 255, 255, 0),
                                                         (0.0019, 0.355, 0.4599, 0.935))

            elif type(self.CurrentEditor).__name__ == "CodeEditorUrsaVisor":
                self.CurrentEditor.MakeEditorEnvironment(application.base.camNode, (200, 200, 200, 0),
                                                         (0.0019, 0.355, 0.4599, 0.935))

            elif type(self.CurrentEditor).__name__ == "SceneEditor":
                self.CurrentEditor.MakeEditorEnvironment(application.base.camNode, (255, 255, 255, 0),
                                                         (0.2399, .999, 0.1009, 0.938))
        if type(self.CurrentTabs[ToJump]).__name__ == "SceneEditor":
            self.CurrentSceneEditor = self.CurrentTabs[ToJump]
            RecursivePerformer(self.CurrentEditor.SpecialEntities)

        def DisableInputFields(Entity):
            if isinstance(Entity, (InputField, TextField)):
                Entity.active = False
            return

        RecursivePerformer(self.CurrentEditor.UniversalParentEntity, ToPerform=DisableInputFields, BasicFunc=False)

        for i in range(len(self.ProjectTabsScrollEntity.children)):
            if self.ProjectTabsScrollEntity.children[i].TabNum == ToJump:
                self.ProjectTabsScrollEntity.children[i].color = tint(color.black, .3)
                self.ProjectTabsScrollEntity.children[i].highlight_color = tint(tint(color.black, .3), .2)
            else:
                self.ProjectTabsScrollEntity.children[i].color = color.black66

        # for i in range(len(self.ProjectTabsScrollEntity.children)):
        #     if self.CurrentTabs[self.ProjectTabsScrollEntity.children[i].TabNum] == self.CurrentEditor:
        #         self.ProjectTabsScrollEntity.children[i].color = color.red
        #         self.ProjectTabsScrollEntity.children[i].highlight_color = color.red

    def UpdateTabsMenu(self):
        # for i in range(len())
        self.ProjectTabsScrollEntity.children.append(
            Button(text=self.CurrentTabs[len(self.ProjectTabsScrollEntity.children)].name,
                   TabNum=len(self.ProjectTabsScrollEntity.children), parent=self.ProjectTabsScrollEntity,
                   scale=(.28, .4), position=(len(self.ProjectTabsScrollEntity.children) / 3 + .2, 0, -22), radius=0,
                   render_queue=self.ProjectTabsScrollEntity.render_queue))
        self.ProjectTabsScrollEntity.children[-1].text_entity.render_queue = self.ProjectTabsScrollEntity.render_queue
        self.ProjectTabsScrollEntity.children[-1].text_entity.wordwrap = 10
        self.ProjectTabsScrollEntity.children[-1].text_entity.scale -= .2
        self.ProjectTabsScrollEntity.children[-1].on_click = Func(self.JumpTabs,
                                                                  self.ProjectTabsScrollEntity.children[-1].TabNum)

        for i in range(len(self.ProjectTabsScrollEntity.children)):
            self.ProjectTabsScrollEntity.children[i].text_entity.render_queue = self.ProjectTabsScrollEntity.children[
                i].text_entity.render_queue

        if len(self.ProjectTabsScrollEntity.children) > 3:
            if len(self.ProjectTabsScrollEntity.children) == 4:
                self.ProjectTabsScrollEntity.scale_x = self.ProjectTabsScrollEntity.scale_x + .14
            else:
                self.ProjectTabsScrollEntity.scale_x = self.ProjectTabsScrollEntity.scale_x + .09582

            for i in range(len(self.ProjectTabsScrollEntity.children)):
                self.ProjectTabsScrollEntity.children[0].x = .08 / self.ProjectTabsScrollEntity.scale_x
                self.ProjectTabsScrollEntity.children[i].scale_x = .08 / self.ProjectTabsScrollEntity.scale_x
                self.ProjectTabsScrollEntity.children[i].text = self.ProjectTabsScrollEntity.children[i].text
                self.ProjectTabsScrollEntity.children[i].text_entity.render_queue = \
                    self.ProjectTabsScrollEntity.children[i].text_entity.render_queue
                self.ProjectTabsScrollEntity.children[i].text_entity.scale -= .1

            for i in range(1, len(self.ProjectTabsScrollEntity.children)):
                self.ProjectTabsScrollEntity.children[i].x = self.ProjectTabsScrollEntity.children[i - 1].x + (
                    self.ProjectTabsScrollEntity.children[i].scale_x) * 1.2
                # print(self.ProjectTabsScrollEntity.children[i-1].x + (self.ProjectTabsScrollEntity.children[i].scale_x) * 1.2)
            self.updateVal()
            self.Scroller.update_target("min", self.val)

    def PrintItemStatTemp(self, Entity):
        for i in range(len(Entity.children)):
            print(
                f"name: {Entity.children[i].name} position = {Entity.children[i].position},rotation = {Entity.children[i].rotation},scale = {Entity.children[i].scale}")
            if len(Entity.children[i].children) > 0:
                self.PrintItemStatTemp(Entity.children[i])

    def ShowToAddTabsMenu(self):
        self.AddEditorToPrjectButtonList.enable()
        self.AddEditorToPrjectButtonList.Background.enable()

    def OnFileAdded(self):
        for i in self.CurrentTabs:
            if type(i).__name__ in ["CodeEditorPython"]:
                i.FileMenu.ReCheckCodeFiles()

    def DestroyCurrentWindow(self):
        self.CurrentCustomWindow.PlayerNotQuitting()
        # print("hi")

    def SetUp(self):
        self.AddEditorToPrjectButton.position = Vec3(0.476, 0, -23)
        self.AddEditorToPrjectButton.scale = Vec3(0.0299989, 0.369998, 1)
        self.AddEditorToPrjectButton.text = self.AddEditorToPrjectButton.text
        self.AddEditorToPrjectButton.text_entity.render_queue = self.AddEditorToPrjectButton.render_queue

        self.SnappingChangingButton.position = Vec3(0.41, 0, -25)
        self.SnappingChangingButton.scale = Vec3(0.0599978, 0.739996, 1)
        self.SnappingChangingButton.text = self.AddEditorToPrjectButton.text
        self.SnappingChangingButton.text_entity.render_queue = self.AddEditorToPrjectButton.render_queue

        self.SnappingIncreaseButton.text_entity.scale = (0.4, 1)
        self.SnappingDecreaseButton.text_entity.scale = (0.4, 1)

        self.SnappingChangingButton.text_entity.render_queue = self.SnappingChangingButton.render_queue
        self.SnappingIncreaseButton.text_entity.render_queue = self.SnappingChangingButton.render_queue
        self.SnappingDecreaseButton.text_entity.render_queue = self.SnappingChangingButton.render_queue

        self.ConfigEditorAsSettings(self.EditorDataDict)

        self.val = .22
        self.Scroller = self.ProjectTabsScrollEntity.add_script(
            Scrollable(axis="x", scroll_speed=0.004, min=self.val, max=.2))
        self.AddEditorToPrjectButtonList.text_entity.color = color.white
        self.AddEditorToPrjectButtonList.text_entity.always_on_top = True
        self.AddEditorToPrjectButtonList.text_entity.render_queue = 1
        # for i in range(len(self.AddEditorToPrjectButtonList.button_dict)):
        #     self.AddEditorToPrjectButtonList.button_dict[list(self.AddEditorToPrjectButtonList.button_dict)[i]]

    def AfterSceneEditorSetUp(self):
        # self.SnappingChangingButton.text = f"{self.CurrentSceneEditor.CurrentGizmo[0]}:{self.CurrentSceneEditor.GizmoManager.CurrentGizmo.Snapping}" if type(self.CurrentSceneEditor.GizmoManager.CurrentGizmo).__name__ != "NoneType" else  f"{self.CurrentSceneEditor.CurrentGizmo[0]}:N/A"
        # self.SnappingChangingButton.SnappingType = self.CurrentSceneEditor.CurrentGizmo
        self.OnGizmoUpdated()

    def OnGizmoUpdated(self):
        self.SnappingChangingButton.text = f"{self.CurrentSceneEditor.CurrentGizmo[0]}:{self.CurrentSceneEditor.GizmoManager.CurrentGizmo.Snapping}" if type(
            self.CurrentSceneEditor.GizmoManager.CurrentGizmo).__name__ != "NoneType" else f"{self.CurrentSceneEditor.CurrentGizmo[0]}:N/A"
        self.SnappingChangingButton.SnappingType = self.CurrentSceneEditor.CurrentGizmo
        self.SnappingChangingButton.text_entity.render_queue = self.AddEditorToPrjectButton.render_queue

    def ConfigEditorAsSettings(self, DataDict):
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self, value):
        self.ItemToToolTipList = (self.AddEditorToPrjectButton, self.SnappingChangingButton)
        if value:
            self.ToolTipList = (
                'Add different editors as many as you want in the form of tabs', "Change snapping of the gizmo")
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i], z=-30, render_queue=2,
                                                             always_on_top=True)
                self.ItemToToolTipList[i].tool_tip.background.render_queue = 1


        else:
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

    @property
    def ProjectName(self):
        return self._ProjectName

    @ProjectName.setter
    def ProjectName(self, Value):
        self._ProjectName = Value
        self.EditingProjectText.text = Value
        self.UDSrc = OpenFile(f"{self._ProjectName}/User defined src.txt",
                              f"{CurrentFolderNameReturner()}/Current Games", [])
        return


if __name__ == "__main__":
    from ursina import print_on_screen

    app = Ursina()
    cam = EditorCamera()
    Sky()
    editor = ProjectEditor(ExportToPyFunc=Func(print_on_screen, "<red>yeah <blue>yes"), CurrentTabs=[],
                           EditorCamera=cam, ToAddTabsText=["helo", "by", "hi"],
                           ToAddTabsFunc=[Func(print, "helo"), Func(print, "by"), Func(print, "hi")],
                           PlayFunction=lambda: ..., EditorDataDict={"Hell": 1, "Show tooltip": True},
                           ShowInstructionFunc=lambda: ..., ReadyToHostProjectFunc=lambda: ...,
                           HostProjectFunc=lambda: ...)
    # editor.AddTabsMenuButtons()
    editor.SetUp()
    editor.UpdateTabsMenu()
    editor.AfterSceneEditorSetUp()
    editor.JumpTabs(0)
    top, left = 0.001, 0.001
    app.run()
