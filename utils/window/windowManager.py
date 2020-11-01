import glfw
from OpenGL.GL import *


def create_window(width, height, title="PyEngine"):
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)  # for macOS
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

    window = glfw.create_window(width, height, title, None, None)

    glfw.make_context_current(window)

    return window


def window_should_close(window):
    return glfw.window_should_close(window)


def poll_events():
    glfw.poll_events()


def swap_buffers(window):
    glfw.swap_buffers(window)


def terminate():
    glfw.terminate()
