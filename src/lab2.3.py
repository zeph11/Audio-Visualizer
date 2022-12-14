import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC 


RESOLUTION = 800

def window_resize(window, width, height):
    glViewport(0,0,width,height)

def mp(x0, y0, x1, y1, res):
  dx = x1 - x0
  dy = y1 - y0
  x = x0
  y = y0
  if dx > dy and dy != 0:
   decide = 0
   pk = dx - (dy / 2)
  else:
    decide = 1
    pk = dy - (dx / 2)
  x_coordinates = np.array([])
  y_coordinates = np.array([])
  print(y > y1)
  while (x < x1) if (decide) else (y > y1):
    print("hi")
    x_coordinates = np.append(x_coordinates, x)
    y_coordinates = np.append(y_coordinates, y)
    if decide:
      x = x + 1
      print("hi")
      if pk < 0:
       pk = pk + dy
      else:
        pk = pk + (dy - dx)
        y = y + 1
    else:
      y = y - 1
      if pk < 0:
       pk = pk + dx
      
      else:
        pk = pk + (dx - dy)
        x = x + 1
  return toNVC(x_coordinates, y_coordinates, res)

def main():

  vertex_src ="""
   #version 330

   layout(location=0) in vec3 aPos;

   void main(){

    gl_Position =vec4(aPos,1.0f);

   }

  """

  fragment_src="""

  #version 330

  out vec4 FragColor;

  void main(){
    FragColor =vec4 (1.0f,1.0f,0.0f,1.0f);

  }
  
  """
  if not glfw.init():
    raise Exception("glfw cannot be initialised")

  window = glfw.create_window(RESOLUTION,RESOLUTION ,"mid-point",None,None)

  if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be created!")

  glfw.set_window_size_callback(window,window_resize)
  glfw.make_context_current(window)

  # temp = bh(-250,-250,1000,1000,RESOLUTION)

  # temp = bh(-250,250,1000,-1000,RESOLUTION)

  temp = mp(-250,250,250,250,RESOLUTION)


 
  vertices = np.array(temp,dtype=np.float32)

  render_count=round(len(temp)/2 )

  print(temp)
  indices = np.array([i for i in range(1,render_count+1)], dtype=np.uint32)
  
  shader =  compileProgram(compileShader(vertex_src,GL_VERTEX_SHADER),compileShader(fragment_src,GL_FRAGMENT_SHADER))

  vertex_buffer_object= glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER,vertex_buffer_object)
  glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)
  
  element_buffer_object= glGenBuffers(1)
  glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,element_buffer_object)
  glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

  glEnableVertexAttribArray(0)
  glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

  glUseProgram(shader)

  print(render_count)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    
    glDrawElements(GL_POINTS,len(indices),GL_UNSIGNED_BYTE,None)

    glfw.swap_buffers(window)

  glfw.terminate()

main()
