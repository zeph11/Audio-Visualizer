import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from Luniva.helpers import toNVC

RESOLUTION = 800


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def bh(x_start, y_start, x_end, y_end, res):
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

    window = glfw.create_window(RESOLUTION, RESOLUTION, "Bresenham", None,
                                None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window cannot be created!")

    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    # temp = bh(-250,-250,1000,1000,RESOLUTION)

    # temp = bh(-250,250,1000,-1000,RESOLUTION)

    temp = bh(-250, 250, 250, 250, RESOLUTION)

    vertices = np.array(temp, dtype=np.float32)

    render_count = round(len(temp) / 2)

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
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glUseProgram(shader)

    print(render_count)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glDrawElements(GL_POINTS, len(indices), GL_UNSIGNED_BYTE, None)

        glfw.swap_buffers(window)

    glfw.terminate()


main()
