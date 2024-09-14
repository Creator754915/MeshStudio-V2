from ursina import *
import math

# Initialize the Ursina app
app = Ursina()

# Create a custom plane with more subdivisions for detailed water
subdivisions = 60
water_model = Mesh(vertices=[], uvs=[], triangles=[])
for i in range(subdivisions):
    for j in range(subdivisions):
        x = i / (subdivisions - 1)  # Normalized [0, 1]
        y = j / (subdivisions - 1)  # Normalized [0, 1]
        water_model.vertices.append(Vec3(x - 0.5, 0, y - 0.5))
        water_model.uvs.append((x, y))

for i in range(subdivisions - 1):
    for j in range(subdivisions - 1):
        a = i * subdivisions + j
        b = (i + 1) * subdivisions + j
        c = (i + 1) * subdivisions + (j + 1)
        d = i * subdivisions + (j + 1)
        water_model.triangles.append((a, b, d))
        water_model.triangles.append((b, c, d))

water_model.generate()

# Create a shader for the water to apply a gradient and animate it
water_shader = Shader(language=Shader.GLSL,
                      vertex="""
#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
out vec2 uv;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
    uv = p3d_MultiTexCoord0;
}
""",
                      fragment="""
#version 140
uniform sampler2D tex;
in vec2 uv;
out vec4 fragColor;

void main() {
    vec3 color_top = vec3(0.0, 0.5, 1.0);
    vec3 color_bottom = vec3(0.0, 0.2, 0.5);
    float gradient = uv.y;
    vec3 color = mix(color_bottom, color_top, gradient);
    fragColor = vec4(color, 0.7);  // Adjust alpha for transparency
}
""")

# Create the water entity
water = Entity(model=water_model, scale=(10, 1, 10), shader=water_shader, position=(0, 0, 0))


# Create a function to animate the water surface
def update():
    t = time.time() * 1.25  # Slower animation
    for i, vertex in enumerate(water.model.vertices):
        vertex.y = (math.sin(t + vertex.x * 10) + math.cos(t + vertex.z * 10)) * 0.1
        water.model.vertices[i] = vertex
    water.model.generate()


# Add some lighting to the scene for better visualization
light = PointLight(position=(0, 10, 0), color=color.white)

EditorCamera()
# Run the Ursina app
app.run()
