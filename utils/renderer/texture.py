import glfw
from OpenGL.GL import *

class Texture2D:
    def __init__(self):
        self.width = 0
        self.height = 0

        self.Internal_Format = GL_RGB
        self.Image_Format = GL_RGB

        self.Wrap_S = GL_REPEAT
        self.Wrap_T = GL_REPEAT

        self.Filter_Min = GL_NEAREST
        self.Filter_Max = GL_NEAREST

        self.ID = glGenTextures(1)

    def generate(self, width, height, imdata):
        self.width = width
        self.height = height

        glBindTexture(GL_TEXTURE_2D, self.ID)
        glTexImage2D(GL_TEXTURE_2D, 0, self.Internal_Format, width, height, 0, self.Image_Format, GL_UNSIGNED_BYTE,
                     imdata)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.Wrap_S)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.Wrap_T)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.Filter_Min)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.Filter_Max)

        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.ID)
