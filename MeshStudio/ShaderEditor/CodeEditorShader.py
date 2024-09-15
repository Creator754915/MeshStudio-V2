import json
from tkinter import *
from tkinter.filedialog import askopenfile

from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

from FileMenu import FileMenu
from MeshStudio.Prefabs.additive_function import CurrentFolderNameReturner
from MeshStudio.ShaderEditor.ProjectEditor import ProjectEditor
from ursina.color import tint
from MeshStudio.ShaderEditor.LanguagesColors.KeywordsColor import GLSL_KW_Color, CG_KW_Color, HLSL_KW_Color, \
    SPIRV_KW_Color
from MeshStudio.Shaders.SSAOShader import SSAOShader
from MeshStudio.Shaders.PIXELShader import PIXELShader


class CodeEditorShader(Entity):
    def __init__(self, EditorDataDict, ShowInstructionFunc, SaveFunction, OnFileAdded, ProjectName=None, UdSrc=[],
                 **kwargs):
        super().__init__()

        self.EditorDataDict = EditorDataDict
        self.Save = SaveFunction
        self.ShowInstructionFunc = ShowInstructionFunc
        self.ReplacementColors = {"class ": "☾orange☽class ☾default☽",
                                  "def ": "☾rgb(50,50,255)☽def ☾default☽",
                                  "self": "☾yellow☽self☾default☽",
                                  "const": "☾rgb(37, 102, 202)☽const☾default☽",
                                  "float": "☾rgb(37, 102, 202)☽float☾default☽",
                                  "int": "☾rgb(37, 102, 202)☽int☾default☽",
                                  "bool": "☾rgb(37, 102, 202)☽bool☾default☽",
                                  "double": "☾rgb(37, 102, 202)☽double☾default☽",
                                  "void": "☾rgb(37, 102, 202)☽void☾default☽",
                                  "in": "☾rgb(37, 102, 202)☽in☾default☽",
                                  "out": "☾rgb(37, 102, 202)☽out☾default☽",
                                  "return": "☾rgb(112, 80, 115)☽return☾default☽",
                                  "uniform": "☾rgb(112, 80, 115)☽uniform☾default☽",
                                  "continue": "☾rgb(112, 80, 115)☽continue☾default☽",
                                  "for": "☾rgb(223, 96, 235)☽for☾default☽",
                                  "while": "☾rgb(223, 96, 235)☽while☾default☽",
                                  "switch": "☾rgb(223, 96, 235)☽switch☾default☽",
                                  "vec4": "☾rgb(37, 102, 202)☽vec4☾default☽",
                                  "vec3": "☾rgb(37, 102, 202)☽vec3☾default☽",
                                  "vec2": "☾rgb(37, 102, 202)☽vec2☾default☽",
                                  "texture": "☾rgb(255, 252, 140)☽texture☾default☽",
                                  "normalize": "☾rgb(255, 252, 140)☽normalize☾default☽",
                                  "cross": "☾rgb(255, 252, 140)☽cross☾default☽",
                                  "get_normal": "☾rgb(255, 252, 140)☽get_normal☾default☽",
                                  "reconstructPosition": "☾rgb(255, 252, 140)☽reconstructPosition☾default☽",
                                  "reflect": "☾rgb(255, 252, 140)☽reflect☾default☽",
                                  "mat3": "☾rgb(255, 252, 140)☽mat3☾default☽",
                                  "step": "☾rgb(255, 252, 140)☽step☾default☽",
                                  "layout": "☾rgb(255, 252, 140)☽layout☾default☽",
                                  "__init__": "☾rgb(50,150,150)☽__init__☾default☽",
                                  "0": "☾rgb(255, 231, 147)☽0☾default☽",
                                  "1": "☾rgb(255, 231, 147)☽1☾default☽",
                                  "2": "☾rgb(255, 23 1, 147)☽2☾default☽",
                                  "3": "☾rgb(255, 231, 147)☽3☾default☽",
                                  "4": "☾rgb(255, 231, 147)☽4☾default☽",
                                  "5": "☾rgb(255, 231, 147)☽5☾default☽",
                                  "6": "☾rgb(255, 231, 147)☽6☾default☽",
                                  "7": "☾rgb(255, 231, 147)☽7☾default☽",
                                  "8": "☾rgb(255, 231, 147)☽8☾default☽",
                                  "9": "☾rgb(255, 231, 147)☽9☾default☽",
                                  "(": "☾rgb(255, 215, 10)☽(☾default☽",
                                  ")": "☾rgb(255, 215, 10)☽)☾default☽",
                                  "[": "☾rgb(255, 215, 10)☽[☾default☽",
                                  "]": "☾rgb(255, 215, 10)☽]☾default☽",
                                  "{": "☾rgb(255, 215, 10)☽{☾default☽",
                                  "}": "☾rgb(255, 215, 10)☽}☾default☽"}

        self.UniversalParentEntity = Entity(parent=camera.ui, enabled=kwargs["enabled"])

        self.EveryItemMenuParentEntity = Entity(name="EveryItemMenuParentEntity", parent=self.UniversalParentEntity,
                                                model="cube", color=color.black66,
                                                scale=Vec3(0.625005, 0.446007, 1), position=Vec3(-0.656, -0.27, 0),
                                                NotRotateOnHover=True)

        self.CodeWriter = TextField(name="Text field", parent=self.UniversalParentEntity, active=False,
                                    position=Vec3(-0.254003, 0.435, 0), rotation=Vec3(0, 0, 0), scale=Vec3(1, 1, 1),
                                    register_mouse_input=True, NotRotateOnHover=True, render_queue=-3)
        self.CodeWriter.line_numbers.enable()
        self.CodeWriter.line_numbers.color = color.white
        self.CodeWriter.line_numbers.render_queue = self.CodeWriter.render_queue
        # self.CodeWriter.line_numbers_background.enable()

        self.FileMenu = FileMenu(ProjectName=ProjectName, CodeEditorEntity=self.CodeWriter,
                                 Path=f"{CurrentFolderNameReturner()}/Current Games",
                                 parent=self.EveryItemMenuParentEntity, queue=0, z=-10, UdSrc=UdSrc,
                                 ShowInstructionFunc=ShowInstructionFunc, OnFileAdded=OnFileAdded)

        self.UniversalParentEntity = Entity(parent=camera.ui, enabled=self.enabled)

        self.TopButtonsParentEntity = Entity(parent=self.UniversalParentEntity, enabled=self.enabled, model="cube",
                                             color=tint(color.white, -.6), texture="white_cube",
                                             position=(window.top[0], window.top[1] - .03, 0), scale=(
                window.screen_resolution[0] / 1052, window.screen_resolution[1] / 18000, 2), always_on_top=True)

        self.TabsMenuParentEntity = Button(parent=self.UniversalParentEntity, enabled=True,
                                           color=tint(color.rgb(31, 31, 31), .1),
                                           highlight_color=tint(color.rgb(31, 31, 31), .1),
                                           pressed_color=tint(color.rgb(31, 31, 31), .1), position=Vec3(0, .5, -20),
                                           scale=Vec3(1.78, 0.1, 1), always_on_top=True, render_queue=-3,
                                           radius=0)  # Vec3(0, 0.39, 1) animate

        self.EditingProjectText = Text(parent=self.TopButtonsParentEntity,
                                       render_queue=self.TopButtonsParentEntity.render_queue, text="Code Shader Editor",
                                       origin=(-.5, 0),
                                       scale_y=20, scale_x=1)

        self.ProjectTabsScrollEntity = Button(parent=self.TabsMenuParentEntity, radius=0,
                                              color=self.TabsMenuParentEntity.color,
                                              highlight_color=self.TabsMenuParentEntity.highlight_color,
                                              pressed_color=self.TabsMenuParentEntity.pressed_color, origin=(-.5, 0, 0),
                                              position=Vec3(0.2277, 0, -21), rotation=Vec3(0, 0, 0),
                                              scale=Vec3(.271, 1, 1), always_on_top=True, render_queue=-2)

        self.SaveProjectButton = Button(parent=self.TopButtonsParentEntity, text="Save", color=tint(color.green, -.2),
                                        radius=0,
                                        position=(-0.447, 0.01, -25), scale=(0.06, 0.7),
                                        on_click=self.SaveEditor)  # Vec3(0.179, 0.0385, 1)
        self.FinishProjectButton = Button(parent=self.TopButtonsParentEntity, text="Open", color=color.blue, radius=0,
                                          position=(-0.377, 0.01, -25), scale=(0.06, 0.7),
                                          on_click=self.OpenShader)  # Vec3(0.179, 0.0385, 1)
        self.PlayProjectButton = Button(parent=self.TopButtonsParentEntity, text="Run", color=color.blue, radius=0,
                                        position=(-0.307, 0.01, -25), scale=(0.06, 0.7),
                                        on_click=self.RunShader())  # Vec3(0.179, 0.0385, 1)
        self.HomeButton = Button(parent=self.TopButtonsParentEntity, text="Exit", color=tint(color.red, -.2), radius=0,
                                 position=(-0.237, 0.01, -25), scale=(0.06, 0.7),
                                 on_click=lambda: application.quit())  # Vec3(0.179, 0.0385, 1)

        self.ChooseLanguage = DropdownMenu('Language', buttons=(
            DropdownMenuButton('GLSL', on_click=Func(self.ChangeLanguage, "GLSL")),
            DropdownMenuButton('CG', on_click=Func(self.ChangeLanguage, "CG")),
            DropdownMenuButton('HLSL', on_click=Func(self.ChangeLanguage, "HLSL")),
            DropdownMenuButton('SPIR-V', on_click=Func(self.ChangeLanguage, "SPIR-V"))
        ))
        self.ChooseLanguage.always_on_top = True
        self.ChooseLanguage.z = -999
        self.ChooseLanguage.y += -.009
        self.ChooseLanguage.x += 0.56
        self.ChooseLanguage.color = color.blue
        self.ChooseLanguage.highlight_color = color.blue
        self.ChooseLanguage.scale_y = .04

        for i in range(len(self.ChooseLanguage.buttons)):
            self.ChooseLanguage.buttons[i].highlight_color = tint(color.blue, .2)

    def MakeEditorEnvironment(self, cam, color, size):
        self.WorldDr = cam.getDisplayRegion(0)
        self.WorldDr.setDimensions(size)
        base.set_background_color(color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255)

    def SetUp(self):
        '''Sets up the class'''
        self.FileMenu.SetUp()
        self.FileMenu.Show()
        self.ConfigEditorAsSettings(self.EditorDataDict)
        self.CodeWriter.replacements = self.ReplacementColors

    def ConfigEditorAsSettings(self, DataDict: dict):
        self.SetTooltip(DataDict["Show tooltip"])

    def SetTooltip(self, value: bool):
        self.ItemToToolTipList = []
        if value:
            self.ToolTipList = []
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = Tooltip(self.ToolTipList[i], z=-30, render_queue=3,
                                                             always_on_top=True)
                # self.ItemToToolTipList[i].tool_tip.background.z = -1

        else:
            for i in range(len(self.ItemToToolTipList)):
                self.ItemToToolTipList[i].tool_tip = None

    def ChangeLanguage(self, Language: str):
        if Language == "GLSL":
            for i in range(len(self.ChooseLanguage.buttons)):
                self.ChooseLanguage.buttons[i].color = color.blue
                self.ChooseLanguage.buttons[i].highlight_color = tint(color.blue, .2)
            self.ChooseLanguage.buttons[0].color = color.green
            self.ChooseLanguage.buttons[0].highlight_color = tint(color.green, .2)

            self.CodeWriter.replacements = GLSL_KW_Color

        elif Language == "CG":
            for i in range(len(self.ChooseLanguage.buttons)):
                self.ChooseLanguage.buttons[i].color = color.blue
                self.ChooseLanguage.buttons[i].highlight_color = tint(color.blue, .2)
            self.ChooseLanguage.buttons[1].color = color.green
            self.ChooseLanguage.buttons[1].highlight_color = tint(color.green, .2)

            self.CodeWriter.replacements = CG_KW_Color

        elif Language == "HLSL":
            for i in range(len(self.ChooseLanguage.buttons)):
                self.ChooseLanguage.buttons[i].color = color.blue
                self.ChooseLanguage.buttons[i].highlight_color = tint(color.blue, .2)
            self.ChooseLanguage.buttons[2].color = color.green
            self.ChooseLanguage.buttons[2].highlight_color = tint(color.green, .2)

            self.CodeWriter.replacements = HLSL_KW_Color

        elif Language == "SPIR-V":
            for i in range(len(self.ChooseLanguage.buttons)):
                self.ChooseLanguage.buttons[i].color = color.blue
                self.ChooseLanguage.buttons[i].highlight_color = tint(color.blue, .2)
            self.ChooseLanguage.buttons[3].color = color.green
            self.ChooseLanguage.buttons[3].highlight_color = tint(color.green, .2)

            self.CodeWriter.replacements = SPIRV_KW_Color
        else:
            print_on_screen("Language Incorrect")

    def RunShader(self):
        pass

    def SaveEditor(self):
        self.FileMenu.SaveCurrentFile()
        self.Save()

    def OpenShader(self):
        Root = Tk()
        Root.withdraw()

        files = [('OpenGL Shading Language', '*.glsl'),
                 ('CG Document', '*.cg'),
                 ('High-Level Shading Language', '*.hlsl'),
                 ('Standard Portable Intermediate Representation', '*.spv')]
        file = askopenfile(parent=Root, filetypes=files)
        if file is not None:
            content = file.read()
            print(content)

            self.CodeWriter.text = content


if __name__ == "__main__":
    from OpenFile import OpenFile

    app = Ursina()
    window.title = "Code Shader Editor"
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    ed = EditorCamera()

    ConfiableEditorDataDefault = {"Show tooltip": True, "Auto save on exit": False, "Show memory counter": True,
                                  "Fullscreen": False, "Anti-aliasing sample": 4, "Render distance (near)": .10,
                                  "Render distance (far)": 10000.0, }

    ConfiableEditorData = OpenFile("Configable editor data.txt", f"{CurrentFolderNameReturner()}/Editor data",
                                   ConfiableEditorDataDefault, True)

    editor = CodeEditorShader(enabled=True, EditorDataDict=ConfiableEditorData, ProjectName="jh",
                              ShowInstructionFunc=Func(print, "hi"), OnFileAdded=Func(print, "hi"),
                              SaveFunction=Func(print, "hi"))

    editor.SetUp()
    editor.model = "cube"
    editor.texture = 'white_cube'
    Sky()
    left = .001
    right = .001
    top = .001
    bottom = .001
    ProjectEditor()

    editor.MakeEditorEnvironment(application.base.camNode, (125, 125, 124, 0), (0.0019, 0.355, 0.4599, 0.935))

    app.run()
