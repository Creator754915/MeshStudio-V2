from ursina import *


class WorldGrid(Entity):
    def __init__(self):
        super().__init__()
        self.WorldGrid = [
            Entity(parent=self, model=Grid(200, 200, thickness=2), rotation_x=90, scale=Vec3(200, 200, 200),
                   collider=None,
                   color=color.red),
            Entity(parent=self, model=Grid(100, 100, thickness=3), rotation_x=90, scale=Vec3(200, 200, 200),
                   collider=None,
                   color=color.black33),
            Entity(parent=self, model=Grid(400, 400), rotation_x=90, scale=Vec3(40, 40, 40), collider=None,
                   color=color.green)]

    def update(self):
        if 1 < distance(camera.position, (0, 0, 0)):
            self.distance = distance(camera.position, (0, 0, 0))
            if self.distance > 150:
                self.distance = 150
        else:
            self.distance = 0

        if self.distance > 10:
            self.WorldGrid[0].color = color.rgba(70, 70, 70, 1000 / self.distance)
            if int(self.WorldGrid[0].color[3]) == 0 and self.distance < 50: self.WorldGrid[0].enable()

            self.WorldGrid[1].color = color.rgba(50, 50, 50, self.distance)
            if int(self.WorldGrid[1].color[3]) == 0: self.WorldGrid[1].enable()

            self.WorldGrid[2].color = color.rgba(0, 0, 0, 200 / self.distance)
            if int(self.WorldGrid[2].color[3]) == 0 and self.distance < 50: self.WorldGrid[2].enable()

        if self.distance < 10:
            self.WorldGrid[1].color = color.rgba(50, 50, 50, 0)
            self.WorldGrid[1].disable()

        if self.distance > 50:
            self.WorldGrid[2].color = color.rgba(0, 0, 0, 0)
            self.WorldGrid[2].disable()
            self.WorldGrid[0].color = (70, 70, 70, 0)
            self.WorldGrid[0].disable()


if __name__ == "__main__":
    from ursina import *

    app = Ursina()

    EditorCamera()

    WorldGrid()

    app.run()