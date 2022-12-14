import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC

resolution = 500


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


# ellipse drawing algorithm
# def ellipse_algo(h, k, a, b, resolution):
#     x_coordinates = ([])
#     y_coordinates = ([])
#     x = 0
#     y = b

#     #initial decision parameter for R1
#     d1 = ((b * b) - (a * a * b) + (0.25 * a * a))
#     dx = 2 * b * b * x
#     dy = 2 * a * a * y

#     #for r1
#     while (dx < dy):
#         x_coordinates = np.append(x_coordinates, x + h)
#         x_coordinates = np.append(x_coordinates, -x + h)
#         x_coordinates = np.append(x_coordinates, x + h)
#         x_coordinates = np.append(x_coordinates, -x + h)
#         y_coordinates = np.append(y_coordinates, y + k)
#         y_coordinates = np.append(y_coordinates, y + k)
#         y_coordinates = np.append(y_coordinates, -y + k)
#         y_coordinates = np.append(y_coordinates, -y + k)

#         if (d1 < 0):
#             x += 1
#             dx = dx + (2 * b * b)
#             d1 = d1 + dx + (b * b)
#         else:
#             x += 1
#             y -= 1
#             dx = dx + (2 * b * b)
#             dy = dy - (2 * a * a)
#             d1 = d1 + dx - dy + (b * b)

#     #initial decision parameter for R2
#     d2 = (((b * b) * ((x + 0.5) * (x + 0.5))) +
#           ((a * a) * ((y - 1) * (y - 1))) - (a * a * b * b))

#     while (y >= 0):
#         x_coordinates = np.append(x_coordinates, x + h)
#         x_coordinates = np.append(x_coordinates, -x + h)
#         x_coordinates = np.append(x_coordinates, x + h)
#         x_coordinates = np.append(x_coordinates, -x + h)
#         y_coordinates = np.append(y_coordinates, y + k)
#         y_coordinates = np.append(y_coordinates, y + k)
#         y_coordinates = np.append(y_coordinates, -y + k)
#         y_coordinates = np.append(y_coordinates, -y + k)

#         if (d2 > 0):
#             y -= 1
#             dy = dy - (2 * a * a)
#             d2 = d2 + (a * a) - dy
#         else:
#             y -= 1
#             x += 1
#             dx = dx + (2 * b * b)
#             dy = dy - (2 * a * a)
#             d2 = d2 + dx - dy + (a * a)

#     return toNVC(x_coordinates, y_coordinates, resolution)


def ellipse_algo(xc, yc, rx, ry, res):
    x = 0
    y = ry
    x_coordinates = np.array([])
    y_coordinates = np.array([])
    pk1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
    dx = 2 * ry * ry * x
    dy = 2 * rx * rx * y
    while dx < dy:
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)

        y_coordinates = np.append(y_coordinates, -y + yc)
        if pk1 < 0:
            x += 1
            dx = dx + (2 * ry * ry)
            pk1 = pk1 + dx + (ry * ry)
        else:
            x += 1
            y -= 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            pk1 = pk1 + dx - dy + (ry * ry)
    pk2 = (((ry * ry) * ((x + 0.5) * (x + 0.5))) +
           ((rx * rx) * ((y - 1) * (y - 1))) - (rx * rx * ry * ry))
    while y >= 0:
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        x_coordinates = np.append(x_coordinates, x + xc)
        x_coordinates = np.append(x_coordinates, -x + xc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)
        y_coordinates = np.append(y_coordinates, -y + yc)
        if pk2 > 0:
            y -= 1
            dy = dy - (2 * rx * rx)
            pk2 = pk2 + (rx * rx) - dy
        else:
            y -= 1
            x += 1
            dx = dx + (2 * ry * ry)
            dy = dy - (2 * rx * rx)
            pk2 = pk2 + dx - dy + (rx * rx)
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
    window = glfw.create_window(resolution, resolution, "LAB2", None, None)

    # check if window
    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    #set size callback and window is resized
    glfw.set_window_size_callback(window, window_resize)
    # context initializes opengl  a state machine that stores all data related to rendering
    glfw.make_context_current(window)

    dda_call = ellipse_algo(0, 0, 50, 40, resolution)

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