import glfw

# checking and initializing glfw library
if not glfw.init():
    raise Exception("glfw cannot be initialized")

# creating window, width, height, name, monitor, share
window = glfw.create_window(1280, 720, "Test Opengl", None, None)

# check if window

if not window:
    glfw.terminate()
    raise Exception("window cannot be created")

glfw.set_window_pos(window, 400, 300)

# context initializes opengl  a state machine that stores all data related to rendering
glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glfw.poll_events()

    glfw.swap_buffers(window)

glfw.terminate()
