import glm
import numpy
from OpenGL.GL import *
import ctypes

class SpriteRenderer:
    def __init__(self, shader):
        self.shader = shader
        self.__init_render_data()

    def draw_sprite(self, texture, position, size, orientation):
        self.shader.use()

        rotationMatrix = glm.mat4(orientation[0], orientation[1], orientation[2], 0.0,
                             orientation[3], orientation[4], orientation[5], 0.0,
                             orientation[6], orientation[7], orientation[8], 0.0,
                             0.0, 0.0, 0.0, 1.0)


        model = glm.mat4(1.0)
        model = glm.translate(model, position)

        model = glm.scale(model, size)

        model = model * rotationMatrix

        self.shader.set_matrix_4f("model", model)
        glActiveTexture(GL_TEXTURE0)
        texture.bind()

        glBindVertexArray(self.quadVAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)

    # poss	tex
    def __init_render_data(self):
        vertices = [
            -1.0, -1.0, -1.0, 0.0, 0.0,     0.0, 0.0, -1.0,
            1.0, -1.0, -1.0, 1.0, 0.0,      0.0, 0.0, -1.0,
            1.0, 1.0, -1.0, 1.0, 1.0,       0.0, 0.0, -1.0,
            1.0, 1.0, -1.0, 1.0, 1.0,       0.0, 0.0, -1.0,
            -1.0, 1.0, -1.0, 0.0, 1.0,      0.0, 0.0, -1.0,
            -1.0, -1.0, -1.0, 0.0, 0.0,     0.0, 0.0, -1.0,

            -1.0, -1.0, 1.0, 0.0, 0.0,      0.0, 0.0, 1.0,
            1.0, -1.0, 1.0, 1.0, 0.0,       0.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0,        0.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0,        0.0, 0.0, 1.0,
            -1.0, 1.0, 1.0, 0.0, 1.0,       0.0, 0.0, 1.0,
            -1.0, -1.0, 1.0, 0.0, 0.0,      0.0, 0.0, 1.0,

            -1.0, 1.0, 1.0, 1.0, 0.0,       -1.0, 0.0, 0.0,
            -1.0, 1.0, -1.0, 1.0, 1.0,      -1.0, 0.0, 0.0,
            -1.0, -1.0, -1.0, 0.0, 1.0,     -1.0, 0.0, 0.0,
            -1.0, -1.0, -1.0, 0.0, 1.0,     -1.0, 0.0, 0.0,
            -1.0, -1.0, 1.0, 0.0, 0.0,      -1.0, 0.0, 0.0,
            -1.0, 1.0, 1.0, 1.0, 0.0,       -1.0, 0.0, 0.0,

            1.0, 1.0, 1.0, 1.0, 0.0,        1.0, 0.0, 0.0,
            1.0, 1.0, -1.0, 1.0, 1.0,       1.0, 0.0, 0.0,
            1.0, -1.0, -1.0, 0.0, 1.0,      1.0, 0.0, 0.0,
            1.0, -1.0, -1.0, 0.0, 1.0,      1.0, 0.0, 0.0,
            1.0, -1.0, 1.0, 0.0, 0.0,       1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 1.0, 0.0,        1.0, 0.0, 0.0,

            -1.0, -1.0, -1.0, 0.0, 1.0,     0.0, -1.0, 0.0,
            1.0, -1.0, -1.0, 1.0, 1.0,      0.0, -1.0, 0.0,
            1.0, -1.0, 1.0, 1.0, 0.0,       0.0, -1.0, 0.0,
            1.0, -1.0, 1.0, 1.0, 0.0,       0.0, -1.0, 0.0,
            -1.0, -1.0, 1.0, 0.0, 0.0,      0.0, -1.0, 0.0,
            -1.0, -1.0, -1.0, 0.0, 1.0,     0.0, -1.0, 0.0,

            -1.0, 1.0, -1.0, 0.0, 1.0,      0.0, 1.0, 0.0,
            1.0, 1.0, -1.0, 1.0, 1.0,       0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0, 0.0,        0.0, 1.0, 0.0,
            1.0, 1.0, 1.0, 1.0, 0.0,        0.0, 1.0, 0.0,
            -1.0, 1.0, 1.0, 0.0, 0.0,       0.0, 1.0, 0.0,
            -1.0, 1.0, -1.0, 0.0, 1.0,       0.0, 1.0, 0.0]
        vertices = numpy.array(vertices, dtype=numpy.float32)

        self.quadVAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, len(vertices) * numpy.dtype(numpy.float32).itemsize, vertices, GL_STATIC_DRAW)

        glBindVertexArray(self.quadVAO)

        #glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 5, ctypes.c_void_p(0))
        #glEnableVertexAttribArray(0)

        #glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 5, ctypes.c_void_p(3 * numpy.dtype(numpy.float32).itemsize))
        #glEnableVertexAttribArray(1)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 8, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 8, ctypes.c_void_p(3 * numpy.dtype(numpy.float32).itemsize))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, numpy.dtype(numpy.float32).itemsize * 8, ctypes.c_void_p(5 * numpy.dtype(numpy.float32).itemsize))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
