from ursina import *
from ursina.color import tint


class SideBarTools(Entity):
    def __init__(self,
                 SideColor=color.rgba(0, 0, 0, 0), position=window.left):
        super().__init__(color=SideColor, position=position)
        self.parent = camera.ui
        self._value = 0
        self._Initposition = .35

        self.background = Entity(parent=self, scale=Vec2(0.4, 1), model=Quad(aspect=3, radius=0),
                                 color=SideColor)

        self.hamburger = Button(parent=self, scale=.05, position=Vec2(.225, self._Initposition),
                                icon="../../MeshStudio/icons/back.png")
        self.hamburger.on_click = self.show_hide

        self.addEntity = Button(parent=self, text="Add", scale=0.08, position=Vec2(0.04, self._Initposition))
        Button(parent=self, text="Add", scale=0.08, position=Vec2(0.04, self._Initposition-0.08*2))

    def show_hide(self):
        if self._value == 0:
            self._value = 1
            self.hamburger.icon = "../../MeshStudio/icons/run.png"
            self.animate_x(self.x - .2, duration=.2)
        else:
            self._value = 0
            self.hamburger.icon = "../../MeshStudio/icons/back.png"
            self.animate_x(self.x + .2, duration=.2)


if __name__ == "__main__":
    app = Ursina()
    window.fullscreen = False
    window.borderless = False
    window.exit_button.enabled = False
    window.fps_counter.enabled = False

    SideBarTools()

    app.run()
