import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


def window_resize(window, width, height):

    glViewport(0, 0, width, height)
    print(f"The Resolution of the Output Screen is:{width} x {height}")


def main():

    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    window = glfw.create_window(1000, 500, "Display Resolution", None, None)

    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    # glfw.set_window_pos(window,100,100)
    glfw.set_window_size_callback(window, window_resize)
    glfw.make_context_current(window)

    glClearColor(1, 1, 1, 1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(window)

    glfw.terminate()


main()