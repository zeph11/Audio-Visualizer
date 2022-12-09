import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


def main():

  vertex_src = """
  #version 330 

  layout(location=0) in vec3 aPos;
  layout(location =1) in vec3 aPos2;

  void main(){
      gl_Position = vec4(aPos,1.0);
      gl_Position = vec4(aPos2,1.0);
      }
  """

  fragment_src = """
  #version 330 

  out vec4 FragColor;

  void main(){
      FragColor = vec4(0.0f, 0.0f, 1.0f, 0.0f);
    
  }
  """
  def window_resize(window, width, height):
    glViewport(0,0,width,height)

  if not glfw.init():
      raise Exception("glfw can not be initialized!")

  window = glfw.create_window(1280, 720, "LAB1", None, None)

  if not window:
      glfw.terminate()
      raise Exception("glfw window can not be created!")

  glfw.set_window_pos(window,100,100)
  glfw.set_window_size_callback(window,window_resize)

  glfw.make_context_current(window)

  vertices = [-0.3,0.7,0,
              -0.3,-0.7,0,
              0.5,-0.7,0,
              -0.0,0.0,0,
               0.5,0.0,0]

  vertices2 = [ i*0.5 for i in vertices]

  # colors = [1,0,0,
  #           0.5,0,1,
  #           0,0.5,
  #           1,0,0.5,
  #           1,0,0.5,]

  vertices = np.array(vertices,dtype=np.float32)
  vertices2 = np.array(vertices2,dtype=np.float32)
  # colors = np.array(colors,dtype=np.float32)

  shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
  # shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))
  vertex_buffer_object = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER,vertex_buffer_object)
  glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)

  vertex2_buffer_object = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER,vertex2_buffer_object)
  glBufferData(GL_ARRAY_BUFFER,vertices2.nbytes,vertices2,GL_STATIC_DRAW)

  
  glEnableVertexAttribArray(0)
  glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

  glEnableVertexAttribArray(1)
  glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

  glUseProgram(shader)
  glClearColor(0,0.1,0.1,0)

  while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays( GL_LINE_LOOP,0,5)

    glfw.swap_buffers(window)

  glfw.terminate()

main()
