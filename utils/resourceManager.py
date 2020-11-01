from utils.renderer.shader import Shader
from PIL import Image
import os
from utils.renderer.texture import *

textures = {}
shaders = {}


# noinspection PyMethodParameters
class ResourceManager:
    def load_shader(vertex_shader_path, fragment_shader_path, name):
        shaders[name] = ResourceManager.load_shader_from_file(vertex_shader_path, fragment_shader_path)
        return shaders[name]

    def get_shader(name):
        return shaders[name]

    def load_texture(name, file):
        textures[name] = ResourceManager.load_texture_from_file(file)
        return textures[name]

    def get_texture(name):
        return textures[name]
    def clear():
        for name in textures:
            glDeleteTextures(textures[name])

        for name in shaders:
            glDeleteProgram(shaders[name])

    def load_shader_from_file(vertex_shader_path, fragment_shader_path):
        absDIR = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), "."), vertex_shader_path))
        f = open(absDIR, 'rb')
        vertex_shader = f.read()
        f.close()

        absDIR = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), "."), fragment_shader_path))
        f = open(absDIR, 'rb')
        fragment_shader = f.read()
        f.close()

        shader = Shader()
        shader.compile(vertex_shader, fragment_shader)

        return shader

    def load_texture_from_file(texture_path):
        texture = Texture2D()

        im = Image.open(texture_path)
        converted = im.convert("RGB")
        # imdata = numpy.array(list(im.getdata()), numpy.uint8)

        texture.generate(im.size[0], im.size[1], converted.tobytes())

        im.close()

        return texture
