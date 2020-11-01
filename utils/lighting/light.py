import numpy
from OpenGL.GL import *
import glm
from utils.renderer.shader import Shader


class Light:
    def __init__(self, position):
        self.VAO = self.__init_render_data()
        self.position = position

    def __init_render_data(self):
        vertices = [
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, 1.0, -1.0,
            1.0, 1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0,

            -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            -1.0, 1.0, 1.0,
            -1.0, -1.0, 1.0,

            -1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0,
            -1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            -1.0, 1.0, 1.0,

            1.0, 1.0, 1.0,
            1.0, 1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, 1.0,
            1.0, 1.0, 1.0,

            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, 1.0,
            1.0, -1.0, 1.0,
            -1.0, -1.0, 1.0,
            -1.0, -1.0, -1.0,

            -1.0, 1.0, -1.0,
            1.0, 1.0, -1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            -1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0]
        vertices = numpy.array(vertices, dtype=numpy.float32)

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * numpy.dtype(numpy.float32).itemsize, vertices, GL_STATIC_DRAW)

        glBindVertexArray(VAO)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 3, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return VAO

    def draw(self, shader):
        shader.use()

        model = glm.mat4(1.0)
        position = glm.vec3(self.position[0], self.position[1], self.position[2])

        model = glm.translate(model, position)

        model = glm.scale(model, glm.vec3(0.1))

        shader.set_matrix_4f("model", model)

        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

