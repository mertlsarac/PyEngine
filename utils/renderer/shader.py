from OpenGL.GL import *
import glm
"""
def printOpenGLError():
    err = glGetError() # pylint: disable=E1111
    if (err != GL_NO_ERROR):
        print('GLERROR: ', glErrorString(err)) # pylint: disable=E1101
"""

import os
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
class Shader():
    def use(self):
        glUseProgram(self.ID)
        # printOpenGLError()
        return self

    def compile(self, vertex_shader_source, fragment_shader_source):
        # create program
        self.ID = glCreateProgram() # pylint: disable=E1111
        #print('create program ',self.program)
        # printOpenGLError()

        # vertex shader
        #print('compile vertex shader...')
        self.vs = glCreateShader(GL_VERTEX_SHADER) # pylint: disable=E1111
        glShaderSource(self.vs, vertex_shader_source)
        glCompileShader(self.vs)
        if(GL_TRUE != glGetShaderiv(self.vs, GL_COMPILE_STATUS)):
            err = glGetShaderInfoLog(self.vs)
            raise Exception(err)
        glAttachShader(self.ID, self.vs)
        # printOpenGLError()

        # fragment shader
        #print('compile fragment shader...')
        self.fs = glCreateShader(GL_FRAGMENT_SHADER) # pylint: disable=E1111
        glShaderSource(self.fs, fragment_shader_source)
        glCompileShader(self.fs)
        if GL_TRUE != glGetShaderiv(self.fs, GL_COMPILE_STATUS):
            err = glGetShaderInfoLog(self.fs)
            raise Exception(err)
        glAttachShader(self.ID, self.fs)
        # printOpenGLError()

        #print('link...')
        glLinkProgram(self.ID)
        if GL_TRUE != glGetProgramiv(self.ID, GL_LINK_STATUS):
            err =  glGetShaderInfoLog(self.vs)
            raise Exception(err)
        # printOpenGLError()

    def set_float(self, name, value, useShader=False):
        if useShader:
            self.use()
        glUniform1f(glGetUniformLocation(self.ID, name), value)

    def set_integer(self, name, value, useShader=False):
        if useShader:
            self.use()
        glUniform1i(glGetUniformLocation(self.ID, name), value)

    def set_vector_2f(self, name, x, y, useShader=False):
        if useShader:
            self.use()
        glUniform2f(glGetUniformLocation(self.ID, name), x, y)

    def set_vector_2f(self, name, value, useShader=False):
        if useShader:
            self.use()
        glUniform2f(glGetUniformLocation(self.ID, name), value.x, value.y)

    def set_vector_3f(self, name, x, y, z, useShader=False):
        if useShader:
            self.use()
        glUniform3f(glGetUniformLocation(self.ID, name), x, y, z)

    def set_vector_3f(self, name, value, useShader=False):
        if useShader:
            self.use()
        glUniform3f(glGetUniformLocation(self.ID, name), value.x, value.y, value.z)

    def set_vector_4f(self, name, x, y, z, w, useShader=False):
        if useShader:
            self.use()
        glUniform4f(glGetUniformLocation(self.ID, name), x, y, z, w)

    def set_vector_4f(self, name, value, useShader=False):
        if useShader:
            self.use()
        glUniform4f(glGetUniformLocation(self.ID, name), value.x, value.y, value.z, value.w)

    def set_matrix_4f(self, name, matrix, useShader=False):
        if useShader:
            self.use()
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(matrix))