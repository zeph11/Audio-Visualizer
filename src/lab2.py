import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

def window_resize(window, width, height):
    glViewport(0,0,width,height)

def dda(start_x,start_y,end_x,end_y):
  dx=end_x-start_x
  dy=end_y-start_y
  step=abs(dy)
  if abs(dx)>abs(dy): 
    step=abs(dx)
  new_x=start_x
  new_y=start_y
  
  



def main():
  if not glfw.init():
    raise Exception("glfw cannot be initialised")

  window = glfw.create_window(500,500,"LAB2",None,None)

  if not window:
    glfw.terminate()
    raise Exception("glfw window cannot be created!")

  glfw.set_window_size_callback(window,window_resize)
  glfw.make_context_current(window)

  while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

  glfw.terminate()

main()





  

  


main()