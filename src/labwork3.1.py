import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC2, altList

RESOLUTION = 500


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def midPointCircle(x_centre, y_centre, r, resolution):
    x_points = []
    y_points = []
    x = 0
    y = r
    p = 1 - r
    while x <= y:
        x_points.append(x)
        y_points.append(y)
        if p < 0:
            p = p + 2 * x + 3
        else:
            p = p + (2 * (x - y)) + 5
            y = y - 1
        x = x + 1

    neg_x_list = [-i + x_centre for i in x_points]
    neg_y_list = [-i + y_centre for i in y_points]
    x_points = [i + x_centre for i in x_points]
    y_points = [i + y_centre for i in y_points]

    midPointPoints = altList(x_points, y_points) + altList(
        neg_x_list, y_points) + altList(neg_x_list, neg_y_list) + altList(
            x_points, neg_y_list) + altList(y_points, x_points) + altList(
                neg_y_list, x_points) + altList(
                    neg_y_list, neg_x_list) + altList(y_points, neg_x_list)
    return toNVC2(midPointPoints, resolution)


def main():

    vertex_src = """
   #version 330

   layout(location=0) in vec3 aPos;

   void main(){

    gl_Position =vec4(aPos,1.0f);

   }

  """
    fragment_src = """

  #version 330

  out vec4 FragColor;

  void main(){
    FragColor =vec4 (1.0f,1.0f,0.0f,1.0f);

  }
  
  """
    if not glfw.init():
        raise Exception("glfw cannot be initialised")

    window = glfw.create_window(RESOLUTION, RESOLUTION, "LAB2", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    glfw.set_window_pos(window, RESOLUTION, RESOLUTION)

    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    temp = midPointCircle(0, 0, 130, RESOLUTION)

    vertices = np.array(temp, dtype=np.float32)

    render_count = round(len(temp))

    print(temp)
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

    print(render_count)

    while not glfw.window_should_close(window):

        glfw.poll_events()

        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()
