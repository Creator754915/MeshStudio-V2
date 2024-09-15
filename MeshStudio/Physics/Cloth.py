from ursina import *
import numpy as np


class ClothPoint(Entity):
    def __init__(self, position, fixed=False):
        super().__init__(model='sphere', scale=0.05, color=color.white)
        self.position = position
        self.prev_position = position
        self.fixed = fixed

    def update_position(self, dt):
        if not self.fixed:
            velocity = self.position - self.prev_position
            self.prev_position = Vec3(self.position)
            self.position += velocity * 0.99  # Damping
            self.position.y -= 9.81 * dt * 0.1  # Gravity


class ClothSimulation(Entity):
    def __init__(self, width=10, height=10, spacing=0.2, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.spacing = spacing

        self.points = []
        self.lines = []

        self.create_points()
        self.create_lines()
        self.fix_points()

    def create_points(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                position = Vec3(x * self.spacing, 0, y * self.spacing)
                point = ClothPoint(position)
                row.append(point)
            self.points.append(row)

    def create_lines(self):
        for y in range(self.height):
            for x in range(self.width):
                if x < self.width - 1:
                    self.add_line(self.points[y][x], self.points[y][x + 1])
                if y < self.height - 1:
                    self.add_line(self.points[y][x], self.points[y + 1][x])

    def add_line(self, p1, p2):
        line = Entity(model=Mesh(vertices=[p1.position, p2.position], mode='line', thickness=5), color=color.black)
        line.p1 = p1
        line.p2 = p2
        self.lines.append(line)

    def fix_points(self):
        self.points[0][0].fixed = True
        self.points[0][-1].fixed = True
        self.points[-1][0].fixed = True
        self.points[-1][-1].fixed = True

    def update(self):
        dt = time.dt

        # Update points
        for row in self.points:
            for point in row:
                point.update_position(dt)

        # Correct positions based on springs
        for line in self.lines:
            p1, p2 = line.p1, line.p2
            direction = p2.position - p1.position
            distance = direction.length()
            correction = direction.normalized() * (distance - self.spacing) * 0.5
            if not p1.fixed:
                p1.position += correction
            if not p2.fixed:
                p2.position -= correction

        # Update line vertices
        for line in self.lines:
            line.model.vertices = [line.p1.position, line.p2.position]
            line.model.generate()


class InteractableCube(Draggable):
    def __init__(self):
        super().__init__(parent=scene, model='cube', color=color.red, scale=(0.2, 0.2, 0.2))
        self.position = Vec3(1, 1, 1)


if __name__ == "__main__":
    app = Ursina()
    cloth = ClothSimulation()

    cube = InteractableCube()


    def update():
        cloth.update()
        cube.update()
        for row in cloth.points:
            for point in row:
                if (point.position - cube.position).length() < 0.2:
                    point.position += (point.position - cube.position).normalized() * 0.05


    EditorCamera()
    app.run()
