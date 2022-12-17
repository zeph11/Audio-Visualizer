import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC

resolution = 500


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


#bresenham algorithm
def bresenham(x_start, y_start, x_end, y_end, res):
    dx = abs(x_end - x_start)
    dy = abs(y_end - y_start)
    pk = 2 * dy - dx
    x_coordinates = np.array([])
    y_coordinates = np.array([])
    for i in range(0, dx + 1):
        x_coordinates = np.append(x_coordinates, x_start)
        y_coordinates = np.append(y_coordinates, y_start)
        if x_start < x_end:
            x_start = x_start + 1

        else:
            x_start = x_start - 1
        if pk < 0:
            pk = pk + 2 * dy
        else:
            if y_start < y_end:
                y_start = y_start + 1
            else:
                y_start = y_start - 1
            pk = pk + 2 * dy - 2 * dx
    return toNVC(x_coordinates, y_coordinates, res)


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
    window = glfw.create_window(resolution, resolution, "Bresenham", None,
                                None)

    # check if window
    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    #set size callback and window is resized
    glfw.set_window_size_callback(window, window_resize)
    # context initializes opengl  a state machine that stores all data related to rendering
    glfw.make_context_current(window)

    # function_call = bresenham(-50, -50, 50, 50, resolution)
    function_call = bresenham(-250, 250, 250, 250, resolution)

    vertices = np.array(function_call, dtype=np.float32)

    render_count = round(len(function_call) / 2)

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
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 30, ctypes.c_void_p(0))

    glUseProgram(shader)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()


def mid_point(x0, y0, x1, y1, res):
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    if dx > dy and dy != 0:
        decision = 0
        pk = dx - (dy / 2)
    else:
        decision = 1
        pk = dy - (dx / 2)
    x_coordinates = np.array([])
    y_coordinates = np.array([])
    print(y > y1)
    while (x < x1) if (decision) else (y > y1):

        x_coordinates = np.append(x_coordinates, x)
        y_coordinates = np.append(y_coordinates, y)
        if decision:
            x = x + 1
            if pk < 0:
                pk = pk + dy
            else:
                pk = pk + (dy - dx)
                y = y + 1
        else:
            y = y - 1
            if pk < 0:
                pk = pk + dx

            else:
                pk = pk + (dx - dy)
                x = x + 1
    return toNVC(x_coordinates, y_coordinates, res)