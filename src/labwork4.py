import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from helpers import altList, toNVC


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


RESOLUTION = 600

#shearing matrix
shearing = np.array(
    [
        1.0,  # D1
        0.8,  # ShearX
        0.0,
        0.0,
        0.0,  # ShearY
        1.0,  # D2
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    np.float32,
)

reflection = np.array(
    [
        -1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    np.float32,
)
rotation = np.array(
    [
        np.cos((np.pi / 180) * 45),  # D1
        np.sin((np.pi / 180) * 45),
        0.0,
        0.0,
        np.sin(-(np.pi / 180) * 45),
        np.cos((np.pi / 180) * 45),  # D2
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    dtype=np.float32,
)

translation = np.array(
    [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.5,
        0.5,
        0.0,
        1.0,
    ],
    dtype=np.float32,
)
rotation = np.array(
    [
        np.cos((np.pi / 180) * 45),
        np.sin((np.pi / 180) * 45),
        0.0,
        0.0,
        np.sin(-(np.pi / 180) * 45),
        np.cos((np.pi / 180) * 45),
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    dtype=np.float32,
)

scaling = np.array(
    [
        1.5,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    dtype=np.float32,
)

reflection = np.array(
    [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        -1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    np.float32,
)

default = np.array(
    [
        1.0,  # D1
        0.0,  # ShearX
        0.0,
        0.0,
        0.0,  # ShearY
        1.0,  # D2
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    ],
    np.float32,
)


def main(transformation):

    vertex_src = """
  #version 330 
  layout(location=0) in vec3 aPos;
  uniform mat4 transformation;
  void main(){
      gl_Position = transformation * vec4(aPos,1.0);
  
      }
  """

    fragment_src = """
  #version 330 
  out vec4 FragColor;
  void main(){
      FragColor = vec4(0.3f,1.0f,1.0f,0.0f);
    
  }
  """

    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    window = glfw.create_window(RESOLUTION, RESOLUTION, "LAB4", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    glfw.set_window_pos(window, 100, 100)
    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    vertices = [
        -0.25,
        0.49890625000000003,
        0,
        -0.00,
        -0.49890625000000003,
        0,
        0.34421874999999985,
        -0.49890625000000003,
        0,
    ]
    vertices = np.array(vertices, dtype=np.float32)
    indices = [1, 2, 3]
    indices = np.array(indices, dtype=np.uint32)

    shader = compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER),
    )

    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STREAM_DRAW)

    element_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices,
                 GL_STREAM_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

    glUseProgram(shader)
    transformation_location = glGetUniformLocation(shader, "transformation")

    while not glfw.window_should_close(window):

        glfw.poll_events()

        glUniformMatrix4fv(transformation_location, 1, GL_FALSE,
                           transformation)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        glfw.swap_buffers(window)

    glfw.terminate()


main(shearing)
