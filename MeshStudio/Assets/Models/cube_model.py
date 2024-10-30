from ursina import *
from ursina.mesh_importer import ursina_mesh_to_obj

from MeshStudio.MainFiles.Gizmo.PositionGizmo import PositionGizmo


class DraggablePoint(Draggable):
    def __init__(self, position=(0, 0, 0), color=color.white, index=0, **kwargs):
        super().__init__(
            model='sphere',
            parent=scene,
            color=color,
            scale=0.15,
            position=position,
            **kwargs
        )
        self.index = index
        self.original_position = position
        self.step = 0.5

        print(self.position)

    def drop(self):
        print(f"Sphère {self.index} relâchée à la position {self.position}")


class CustomCube(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.vertices = [
            Vec3(-0.5, -0.5, -0.5),  # Coin inférieur gauche arrière
            Vec3(0.5, -0.5, -0.5),  # Coin inférieur droit arrière
            Vec3(0.5, 0.5, -0.5),  # Coin supérieur droit arrière
            Vec3(-0.5, 0.5, -0.5),  # Coin supérieur gauche arrière
            Vec3(-0.5, -0.5, 0.5),  # Coin inférieur gauche avant
            Vec3(0.5, -0.5, 0.5),  # Coin inférieur droit avant
            Vec3(0.5, 0.5, 0.5),  # Coin supérieur droit avant
            Vec3(-0.5, 0.5, 0.5)  # Coin supérieur gauche avant
        ]
        self.triangles = [
            (0, 1, 2), (2, 3, 0),  # Face arrière
            (4, 5, 6), (6, 7, 4),  # Face avant
            (0, 4, 7), (7, 3, 0),  # Face gauche
            (1, 5, 6), (6, 2, 1),  # Face droite
            (3, 2, 6), (6, 7, 3),  # Face supérieure
            (0, 1, 5), (5, 4, 0)  # Face inférieure
        ]

        self.spheres = []
        for i, vertex in enumerate(self.vertices):
            sphere = DraggablePoint(position=vertex, color=color.red, index=i)
            ed = PositionGizmo(sphere, 0, lambda: ..., .2)
            ed.SetUp()
            self.spheres.append(sphere)

        # Crée le modèle du cube
        self.model = self.create_custom_cube()
        self.texture = 'white_cube'

    def create_custom_cube(self):
        return Mesh(vertices=self.vertices, triangles=self.triangles, mode='triangle')

    def update_vertices(self):
        for sphere in self.spheres:
            self.vertices[sphere.index] = sphere.position
        self.model = self.create_custom_cube()


    def update(self):
        self.update_vertices()


    def ExportToOBJ(self, name: str):
        ursina_mesh_to_obj(self.model, name=name, out_path=Func(getattr, application, 'compressed_models_folder'),
                           max_decimals=5, flip_faces=True)


# Lancer l'application
if __name__ == '__main__':
    app = Ursina()
    custom_cube = CustomCube()

    EditorCamera()

    app.run()
