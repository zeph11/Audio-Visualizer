import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# vertex shaders
vertex_src = """
# version 330 

layout(location=0) in vec3 a_position;
layout(location=1)in vec3 a_Color;

out vec3 vColor;

void main()
{
    gl_Position=vec4(a_position,1.0);
    vColor=a_Color;
}
"""

fragment_src = """
# version 330 

in vec3 vColor;
out vec4 out_color;

void main(){
    out_color=vec4(vColor, 0.0f);
}
"""


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# checking and initializing glfw library
if not glfw.init():
    raise Exception("glfw cannot be initialized")

# creating window, width, height, name, monitor, share
window = glfw.create_window(500, 500, "Lab Opengl", None, None)

# check if window

if not window:
    glfw.terminate()
    raise Exception("window cannot be created")

glfw.set_window_pos(window, 400, 300)

#set size callback and window is resized
glfw.set_window_size_callback(window, window_resize)

# context initializes opengl  a state machine that stores all data related to rendering
glfw.make_context_current(window)

vertices = [
    #1st
    -0.30000000000000004,
    0.44999999999999996,
    0,
    -0.30000000000000004,
    -0.012968750000000029,
    0,
    0.43124999999999997,
    -0.012968750000000029,
    0,
    #2nd
    -0.30000000000000004,
    0.25625,
    0,
    -0.30000000000000004,
    -0.4501562500000001,
    0,
    0.40937500000000004,
    -0.4501562500000001,
    0,
    #3rd
    -0.27326877,
    0.4015625,
    0,
    -0.27326877,
    0.014062500000000033,
    0,
    0.34437500000000004,
    0.014062500000000033,
    0,
    #4th
    -0.27390625,
    0.19890625000000003,
    0,
    -0.27390625,
    -0.4223437499999999,
    0,
    0.34421874999999985,
    -0.4223437499999999,
    0,
]

colors = [  #inner
    0,
    0,
    0.5,
    0,
    0,
    0.5,
    0,
    0,
    0.5,
    #inner
    0,
    0,
    0.5,
    0,
    0,
    0.5,
    0,
    0,
    0.5,
    #outer
    1,
    0,
    0,
    1,
    0,
    0,
    1,
    0,
    0,
    #outer
    1,
    0,
    0,
    1,
    0,
    0,
    1,
    0,
    0,
]

#concatinating two lists
bufferData = vertices + colors

indicesData = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=np.uint32)
bufferData = np.array(bufferData, dtype=np.float32)
vertices = np.array(vertices, dtype=np.float32)

# glEnableClientState(GL_VERTEX_ARRAY)
# glVertexPointer(3, GL_FLOAT, 0, vertices)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                        compileShader(fragment_src, GL_FRAGMENT_SHADER))

#initializing VBO
vertex_buffer_obj = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_obj)
glBufferData(GL_ARRAY_BUFFER, bufferData.nbytes, bufferData, GL_STREAM_DRAW)

#initializing EBO
element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indicesData.nbytes, indicesData,
             GL_STREAM_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0,
                      ctypes.c_void_p(vertices.nbytes))

glUseProgram(shader)
# glClearColor(0, 0.1, 0.1, 1)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES, len(indicesData), GL_UNSIGNED_INT, None)
    glfw.swap_buffers(window)

glfw.terminate()
