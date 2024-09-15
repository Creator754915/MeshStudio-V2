from ursina import *


class SideBarTools(Entity):
    def __init__(self, scale=(55 / 80, window.size.y), model=Quad(aspect=3, radius=0),
                 color=color.tint(color.gray, -.1), position=window.left):
        super().__init__(scale=scale, model=model, color=color, position=position)
        self.parent = camera.ui

if __name__ == "__main__":
    app = Ursina()

    SideBarTools()

    app.run()