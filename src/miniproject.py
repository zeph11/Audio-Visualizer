import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from audio_analyzer import fft_points
from helpers import altList, toNVC2


RESOLUTION = 800
x_change = float(0.0)
numberofspikes = 0


def window_resize(window, width, height):
    glViewport(0, 0, width, height)


def subbufferfun():
    current_value_x = -1 + numberofspikes*x_change
    vertices = [
        current_value_x, 0.5, 0.0,
        current_value_x+x_change, 0.5, 0.0,
        current_value_x, 0.0, 0.0,
        current_value_x+x_change, 0.0, 0.0,
    ]

    glBufferSubData(GL_ARRAY_BUFFER, numberofspikes*24, 24, vertices)


def main():

    # after how much to trigger it
    time = float(10.0)

    previous = float(glfw.get_time())

    vertex_src = """
    
    #version 330
    layout(location=0) in vec2 aPos;
    uniform mat4 translation;
    
    void main(){
        
        gl_Position = translation * vec4(aPos,0.0f,1.0f);
        
        }
    """

    fragment_src = """
    
    #version 330
    
    out vec4 FragColor;
    
    void main(){
        
        FragColor = vec4(1.0f,1.0f,0.0f,0.0f);
        }
    
    """

    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    window = glfw.create_window(RESOLUTION, RESOLUTION, "Display", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    # glfw.set_window_pos(window,100,100)
    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    y_coordinates = [abs(i) for i in fft_points()]

    if len(y_coordinates) > RESOLUTION - 100:
        y_coordinates = y_coordinates[0:RESOLUTION-100]

    x_coordinates = [i for i in range(-RESOLUTION, RESOLUTION)]
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
            0.1,
            -0.9,
            0.0,
            1.0,
        ],
        dtype=np.float32,
    )

    vertices = toNVC2(altList(x_coordinates, y_coordinates), RESOLUTION)

    vertices = np.array(vertices, dtype=np.float32)

    shader = compileProgram(compileShader(
        vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
    print(vertices)
    vertex_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STREAM_DRAW)
    # element_buffer_object= glGenBuffers(1)
    # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,element_buffer_object)
    # glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE,
                          vertices.itemsize*2, ctypes.c_void_p(0))

    glUseProgram(shader)

    glClearColor(0.1, 0.1, 0.1, 0.1)
    transformation_location = glGetUniformLocation(shader, "translation")

    while not glfw.window_should_close(window):
        glfw.poll_events()
        now = float(glfw.get_time())
        delta = float(now-previous)
        previous = now

        # for each timer
        time -= delta
        if (time <= 0.0):
            # timer triggerthing need to do here
            subbufferfun()

        glUniformMatrix4fv(transformation_location, 1, GL_FALSE, translation)
        glDrawArrays(GL_LINES, 0, len(y_coordinates)*2)
        glfw.swap_buffers(window)
    glfw.terminate()


main()
