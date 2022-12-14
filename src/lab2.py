import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC

RESOLUTION = 800


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def dda(start_x, start_y, end_x, end_y, resolution):
    x_points = []
    y_points = []
    dx = end_x - start_x
    dy = end_y - start_y
    step = abs(dy)
    if abs(dx) > abs(dy):
        step = abs(dx)
    new_x = start_x
    new_y = start_y
    x_inc = dx / step
    y_inc = dy / step

    for i in range(step):
        x_points.append(new_x)
        y_points.append(new_y)
        new_x += x_inc
        new_y += y_inc

    return toNVC(x_points, y_points, resolution)


# def mp(x0, y0, x1, y1, res):
#   dx = x1 - x0
#   dy = y1 - y0
#   x = x0
#   y = y0
#   if dx > dy and dy != 0:
#    decide = 0
#    pk = dx - (dy / 2)
#   else:
#     decide = 1
#     pk = dy - (dx / 2)
#   x_coordinates = np.array([])
#   y_coordinates = np.array([])
#   print(y > y1)
#   while (x < x1) if (decide) else (y > y1):
#     print("hi")
#     x_coordinates = np.append(x_coordinates, x)
#     y_coordinates = np.append(y_coordinates, y)
#     if decide:
#       x = x + 1
#       print("hi")
#       if pk < 0:
#        pk = pk + dy
#       else:
#         pk = pk + (dy - dx)
#         y = y + 1
#     else:
#       y = y - 1
#       if pk < 0:
#        pk = pk + dx

#       else:
#         pk = pk + (dx - dy)
#         x = x + 1
#   return toNVC(x_coordinates, y_coordinates, res)

# def bh(x_start, y_start, x_end, y_end, res):
#   dx = abs(x_end - x_start)
#   dy = abs(y_end - y_start)
#   pk = 2 * dy - dx
#   x_coordinates = np.array([])
#   y_coordinates = np.array([])
#   for i in range(0, dx + 1):
#     x_coordinates = np.append(x_coordinates, x_start)
#     y_coordinates = np.append(y_coordinates, y_start)
#     if x_start < x_end:
#      x_start = x_start + 1

#     else:
#      x_start = x_start - 1
#     if pk < 0:
#       pk = pk + 2 * dy
#     else:
#       if y_start < y_end:
#         y_start = y_start + 1
#       else:
#        y_start = y_start - 1
#       pk = pk + 2 * dy - 2 * dx
#   return toNVC(x_coordinates, y_coordinates, res)


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

    glfw.set_window_pos(window, 100, 100)

    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    temp = dda(-500, -500, 1500, 1500, RESOLUTION)

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

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

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
