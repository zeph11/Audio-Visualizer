import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


RESOLUTION = 800
def window_resize(window, width, height):
    glViewport(0,0,width,height)
    
def main():

  vertex_src = """
  #version 330 

  layout(location=0) in vec3 aPos;
  layout(location=1) in vec3 aColor;

  out vec3 vColor;

  void main(){
      gl_Position = vec4(aPos,1.0);
      vColor= aColor;
      }
  """

  fragment_src = """
  #version 330 

  in vec3 vColor;
  out vec4 FragColor;

  void main(){
      FragColor = vec4(vColor, 0.0f);
    
  }
  """
  
  if not glfw.init():
      raise Exception("glfw can not be initialized!")

  window = glfw.create_window(RESOLUTION, RESOLUTION, "LAB1", None, None)

  if not window:
      glfw.terminate()
      raise Exception("glfw window can not be created!")

  # glfw.set_window_pos(window,100,100)
  glfw.set_window_size_callback(window,window_resize)
  glfw.make_context_current(window)

  vertices = [
        #1st
        -0.30000000000000004, 0.44999999999999996,0,
        -0.30000000000000004, -0.012968750000000029,0,
        0.43124999999999997, -0.012968750000000029,0,
        #2nd
        -0.30000000000000004, 0.25625,0,
        -0.30000000000000004, -0.4501562500000001,0,
        0.40937500000000004, -0.4501562500000001,0,
        #3rd
        -0.27326877, 0.4015625,0,
        -0.27326877, 0.014062500000000033,0,
        0.34437500000000004, 0.014062500000000033,0,
        #4th
        -0.27390625, 0.19890625000000003,0,
        -0.27390625, -0.4223437499999999,0,
        0.34421874999999985, -0.4223437499999999,0,
    ]
  colors = [#1st
            0, 0.10, 0.58,
            0, 0.10, 0.58, 
            0, 0.10, 0.58, 
            #2nd
            0, 0.10, 0.58, 
            0, 0.10, 0.58, 
            0, 0.10, 0.58, 
            #3rd
            0.859, 0.078125, 0.234, 
            0.859, 0.078125, 0.234, 
            0.859, 0.078125, 0.234, 
            #4th
            0.859, 0.078125, 0.234, 
            0.859, 0.078125, 0.234, 
            0.859, 0.078125, 0.234, 
           ]

  bufferData= vertices+colors
  indicesData = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], dtype=np.uint32)
  vertices = np.array(vertices,dtype=np.float32)
  bufferData = np.array(bufferData,dtype=np.float32)
 
  shader = compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))

  vertex_buffer_object = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER,vertex_buffer_object)
  glBufferData(GL_ARRAY_BUFFER,bufferData.nbytes,bufferData,GL_STREAM_DRAW)

  element_buffer_object = glGenBuffers(1)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,element_buffer_object)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER,indicesData.nbytes,indicesData,GL_STREAM_DRAW)

  glEnableVertexAttribArray(0)
  glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))
  
  glEnableVertexAttribArray(1)
  glVertexAttribPointer(1,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(vertices.nbytes))

  glUseProgram(shader)
  glClearColor(0.1,0.1,0.1,0.1)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawElements(GL_TRIANGLES,len(indicesData),GL_UNSIGNED_INT,None)
    glfw.swap_buffers(window)

  glfw.terminate()

main()