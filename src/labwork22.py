import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC

resolution = 500


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


#dda algorithm
def dda_algol(x0, y0, x1, y1, resolution):
    x_points = np.array([])
    y_points = np.array([])
    change_in_x = x1 - x0
    change_in_y = y1 - y0

    step = max(change_in_x, change_in_y)
    # if abs(change_in_x) > abs(change_in_y):
    #     step = abs(change_in_x)

    # if abs(change_in_y) > abs(change_in_x):
    #     step = abs(change_in_y)

    new_x = x0
    new_y = y0

    x_increament = change_in_x / step
    y_increament = change_in_y / step

    for i in range(step):
        x_points = np.append(x_points, new_x)
        y_points = np.append(y_points, new_y)

        new_x += x_increament
        new_y = y_increament

    return toNVC(x_points, y_points, resolution)


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

    dda_call = dda_algol(-50, -50, 50, 50, resolution)

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
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glUseProgram(shader)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()