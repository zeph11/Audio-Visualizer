import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# vertex shaders
vertex_src = """
# version 330 core
in vec3 a_position;
void main()
{
    gl_Position=vec4(a_position,1.0);
}
"""

fragment_src = """
# version 330 core
out vec4 out_color;
void main(){
    out_color=vec4(1.0, 0.0, 0.0, 1.0)
}
"""


# checking and initializing glfw library
if not glfw.init():
    raise Exception("glfw cannot be initialized")

# creating window, width, height, name, monitor, share
window = glfw.create_window(1280, 720, "Test Opengl", None, None)

# check if window

if not window:
    glfw.terminate()
    raise Exception("window cannot be created")

glfw.set_window_pos(window, 400, 300)

# context initializes opengl  a state machine that stores all data related to rendering
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0, 0.5, -0.5, 0, 0, 0.5, 0]
colors = [1.0, 0, 0, 0, 1.0, 0, 0, 0, 1.0]

vertices = np.array(vertices, dtype=np.float32)
colors = np.array(colors, dtype=np.float32)

shader = compileProgram(compileShader(
    vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

glfw.terminate()
