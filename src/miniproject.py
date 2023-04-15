import numpy as np
from OpenGL.GL import *
import OpenGL.GLUT as glut
from audio_analyzer import fft_points
from helpers import toNVC2


RESOLUTION = 800

vertex_src = """

#version 330
layout(location=0) in vec2 aPos;
uniform mat4 translation;

void main(){
    
    gl_Position =  translation*vec4(aPos,0.0f,1.0f);
    
    }
"""

fragment_src = """

#version 330

out vec4 FragColor;

void main(){
    
    FragColor = vec4(1.0f,1.0f,0.0f,0.0f);
    }

"""


def window_resize(width, height):
    glViewport(0, 0, width, height)


def returnIndices(lst):
    indices = []
    current_count = 1
    for i in range(1, len(lst) + 1):
        indices.append(i)
        if (i - current_count) == 3:
            indices.append(i)
            current_count = i
    return indices


def sendRectanglestoGL(x_list, y_list):
    # y_list.append(0)
    offset = x_list[0] - x_list[1]
    # delta = 1
    offset = offset * 3
    rectVertices = []
    for i in range(len(x_list) - 1):
        rectVertices.append(x_list[i])
        rectVertices.append(0)

        rectVertices.append(x_list[i])
        rectVertices.append(y_list[i])

        rectVertices.append(x_list[i] + offset)
        rectVertices.append(y_list[i])

        rectVertices.append(x_list[i] + offset)
        rectVertices.append(0)

    return rectVertices


tempData = fft_points()
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
        -1.0,
        -1.0,
        0.0,
        1.0,
    ],
    dtype=np.float32,
)

x_coordinates = [i for i in range(0, len(tempData[0]), 2)]
y_coordinates = [abs(i) for i in tempData[0]]

temp_coordinates = sendRectanglestoGL(x_coordinates, y_coordinates)

waveVertices = np.zeros(len(temp_coordinates), [("position", np.float32, 1)])
waveVertices["position"] = toNVC2(temp_coordinates, RESOLUTION)

VBO = None
VAO = None

# animation control
current_position = 0


def audioAnimation(value):
    global tempData, current_position, x_coordinates, waveVertices

    y_coordinates = [abs(j) for j in tempData[current_position]]
    temp = sendRectanglestoGL(x_coordinates, y_coordinates)
    waveVertices["position"] = toNVC2(temp, RESOLUTION)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferSubData(GL_ARRAY_BUFFER, 0, waveVertices.nbytes, waveVertices)
    if current_position + 1 <= len(tempData):
        current_position += 1

    glut.glutTimerFunc(int(1000 / 60), audioAnimation, 0)


def initialize():
    global translation, indices, VBO, VAO

    # create program
    program = glCreateProgram()

    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertex_src)
    glCompileShader(vertexShader)
    if not glGetShaderiv(vertexShader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertexShader).decode()
        print(error)
        raise RuntimeError(f"{vertex_src} shader compilation error")

    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragment_src)
    glCompileShader(fragmentShader)

    if not glGetShaderiv(vertexShader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertexShader).decode()
        print(error)
        raise RuntimeError(f"{vertex_src} shader compilation error")

    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)

    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError("Error Linking program")

    glDetachShader(program, vertexShader)
    glDetachShader(program, fragmentShader)

    glUseProgram(program)

    # Main Start
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, waveVertices.nbytes, waveVertices, GL_DYNAMIC_DRAW)

    indices = np.array(returnIndices(y_coordinates), dtype=np.int32)
    eVBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eVBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, eVBO)

    translation_location = glGetUniformLocation(program, "translation")
    glUniformMatrix4fv(translation_location, 1, GL_FALSE, translation)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.1, 0.1, 0.1, 0.1)
    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLE_STRIP, len(indices), GL_UNSIGNED_INT, None)

    glut.glutSwapBuffers()
    glut.glutPostRedisplay()


glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow("Audio Visualizer")
glut.glutReshapeWindow(800, 800)
glut.glutReshapeFunc(window_resize)
initialize()
glut.glutDisplayFunc(display)
audioAnimation(0)
glut.glutMainLoop()
