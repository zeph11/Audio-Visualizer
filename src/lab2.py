import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from helpers import toNVC 


RESOLUTION = 500

def window_resize(window, width, height):
    glViewport(0,0,width,height)

def dda(start_x,start_y,end_x,end_y, resolution):
  x_points = np.array([])
  y_points = np.array([])
  dx=end_x-start_x
  dy=end_y-start_y
  step=abs(dy)
  if abs(dx)>abs(dy): 
    step=abs(dx)
  new_x=start_x
  new_y=start_y
  x_inc=dx/step
  y_inc=dy/step

  for i in range(step):
    x_points=np.append(x_points,new_x)
    y_points=np.append(y_points,new_y)
    new_x += x_inc
    new_y += y_inc

  return toNVC(x_points,y_points,resolution)

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

  window = glfw.create_window(RESOLUTION,RESOLUTION ,"LAB2",None,None)

  if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be created!")

  glfw.set_window_size_callback(window,window_resize)
  glfw.make_context_current(window)

  temp = dda(2,3,6,15,RESOLUTION)
 
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
  glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,0,ctypes.c_void_p(0))

  glUseProgram(shader)

  print(render_count)

  while not glfw.window_should_close(window):
    glfw.poll_events()
    
    glDrawElements(GL_POINTS,len(indices),GL_UNSIGNED_BYTE,None)

    glfw.swap_buffers(window)

  glfw.terminate()

main()
