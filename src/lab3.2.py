import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC2, toNVC, altList

resolution = 600


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def ellipse_algo(xc, yc, rx, ry, resolution):
    x = 0
    y = ry
    x_coordinates = []
    y_coordinates = []

    d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y

    while dx < dy:
        x_coordinates.append(x + xc)
        x_coordinates.append(-x + xc)
        y_coordinates.append(y + yc)
        y_coordinates.append(-y + yc)

        if d1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            d1 = d1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d1 = d1 + dx - dy + (ry * ry)

    # Decision parameter of region 2
    d2 = (
        ((ry * ry) * ((x + 0.5) * (x + 0.5)))
        + ((rx * rx) * ((y - 1) * (y - 1)))
        - (rx * rx * ry * ry)
    )

    # Plotting points of region 2
    while y >= 0:

        # printing points based on 4-way symmetry
        x_coordinates.append(x + xc)
        x_coordinates.append(-x + xc)
        y_coordinates.append(y + yc)
        y_coordinates.append(-y + yc)
        # Checking and updating parameter
        # value based on algorithm
        if d2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            d2 = d2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            d2 = d2 + dx - dy + (rx * rx)

    return toNVC2(altList(x_coordinates, y_coordinates), resolution)


def main():

    vertex_src = """
    #version 330
    layout (location=0) in vec2 a_position;
    void main(){
        gl_Position=vec4(a_position,0.0f, 1.0f);
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
    window = glfw.create_window(resolution, resolution, "Ellipse", None, None)

    # check if window
    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    # set size callback and window is resized
    glfw.set_window_size_callback(window, window_resize)
    # context initializes opengl  a state machine that stores all data related to rendering
    glfw.make_context_current(window)

    dda_call = ellipse_algo(0, 0, 20, 90, resolution)

    vertices = np.array(dda_call, dtype=np.float32)

    render_count = round(len(dda_call) / 2)

    print(render_count)

    indices = np.array([i for i in range(1, render_count + 1)], dtype=np.uint32)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER),
    )

    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    element_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glUseProgram(shader)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()
