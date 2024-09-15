from ursina import Ursina, Entity, camera, color
from panda3d.core import LineSegs, NodePath

# Initialize Ursina application
app = Ursina()


# Function to create a 2D line using Panda3D and Ursina
def create_2d_line(start, end, line_color, thickness):
    line = LineSegs()
    line.setThickness(thickness)  # Set the thickness of the line
    line.setColor(line_color[0], line_color[1], line_color[2], line_color[3])
    line.moveTo(start[0], start[1], 0)
    line.drawTo(end[0], end[1], 0)

    line_node = line.create()
    line_node_path = NodePath(line_node)
    line_entity = Entity(model=line_node_path, color=color.white)
    line_entity.model.setTwoSided(True)

    return line_entity


# Set orthographic camera for 2D view
camera.orthographic = True
camera.fov = 10

# Create a white 2D line with specific thickness
start_point = (-2, 0)  # Starting point of the line (x, y)
end_point = (2, 0)  # Ending point of the line (x, y)
line_color = (1, 1, 1, 1)  # White color in RGBA
line_thickness = 5.0  # Thickness of the line

line_entity = create_2d_line(start_point, end_point, line_color, line_thickness)

# Run the Ursina app
app.run()
