import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC

resolution = 500


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# #dda algorithm


def dda_algol(x0, y0, x1, y1, res):
    dx = abs(x0 - x1)
    dy = abs(y0 - y1)
    steps = max(dx, dy)
    xinc = dx / steps
    yinc = dy / steps
    x = float(x0)
    y = float(y0)
    x_coordinates = np.array([])
    y_coordinates = np.array([])

    for i in range(steps):
        x_coordinates = np.append(x_coordinates, x)
        y_coordinates = np.append(y_coordinates, y)
        x = x + xinc
        y = y + yinc
    return toNVC(x_coordinates, y_coordinates, resolution)


def main():

    vertex_src = """
    #version 330
    layout (location=0) in vec3 a_position;
    void main(){
        gl_Position=vec4(a_position, 1.0f);
    }
    """

    fragment_src = """

    #version 330

    out vec4 FragColor;

    void main(){
        FragColor= vec4(1.0f,1.0f,0.0f,1.0f);
    }

    """

    # checking and initializing glfw library
    if not glfw.init():
        raise Exception("glfw cannot be initialised")

    # creating window, width, height, name, monitor, share
    window = glfw.create_window(resolution, resolution, "LAB2", None, None)

    # check if window
    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    #set size callback and window is resized
    glfw.set_window_size_callback(window, window_resize)
    # context initializes opengl  a state machine that stores all data related to rendering
    glfw.make_context_current(window)

    dda_call = dda_algol(-250, -250, 350, 350, resolution)

    vertices = np.array(dda_call, dtype=np.float32)

    render_count = round(len(dda_call) / 2)

    indices = np.array([i for i in range(1, render_count + 1)],
                       dtype=np.uint32)

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                            compileShader(fragment_src, GL_FRAGMENT_SHADER))

    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    element_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices,
                 GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 25, ctypes.c_void_p(0))

    glUseProgram(shader)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()