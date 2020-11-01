from utils.camera.camera import *
from utils.lighting.light import Light
from utils.objects.gameObject import GameObject
from utils.resourceManager import *
from utils.renderer.spriteRenderer import *
from utils.renderer.spriteRenderer_pyramid import *
import glm
import math
from utils.physic.my_physic import *
from utils.window.windowManager import *


class State:
    GAME_ACTIVE, GAME_MENU, GAME_WIN = range(0, 3)


def update_view():
    view = glm.mat4(1.0)
    radius = 1.0

    camX = math.sin(glfw.get_time()) * radius
    camZ = math.cos(glfw.get_time()) * radius
    view = glm.lookAt(glm.vec3(1.0, 1.0, 4.0), glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.0, 1.0, 0.0))
    ResourceManager.get_shader("sprite").set_matrix_4f("view", view)


def clear_color():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


class PyEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.state = State.GAME_ACTIVE
        self.keys = [0 for i in range(1024)]

        # init camera
        self.currentFrame = 0
        self.lastFrame = 0
        self.camera = Camera()

        # init mouse positions
        self.lastX = self.width / 2
        self.lastY = self.height / 2
        self.firstMouse = True

        # init renderer and physic
        self.Renderer = None
        self.Renderer2 = None
        self.Renderer_pyramid = None

        # init physic engine
        self.simulation_speed = 1
        self.p = None

        # GUI
        self.GUI = True

    def init(self, GUI=True):
        if GUI:
            ResourceManager.load_shader("glsl/light/vertex.glsl", "glsl/light/fragment.glsl", "sprite")
            ResourceManager.load_shader("glsl/light/light_vertex.glsl", "glsl/light/light_fragment.glsl", "light")
            ResourceManager.load_shader("glsl/vertex.glsl", "glsl/fragment.glsl", "sprite2")

            projection = glm.mat4(1.0)
            projection = glm.perspective(glm.radians(45.0), self.width / self.height, 0.1, 100.0)

            # init light shader
            ResourceManager.get_shader("sprite").use().set_integer("texture1", 0)
            ResourceManager.get_shader("sprite").set_matrix_4f("projection", projection)

            ResourceManager.get_shader("sprite").set_vector_3f("lightColor", glm.vec3(1.0, 1.0, 1.0))
            ResourceManager.get_shader("sprite").set_vector_3f("lightPos", glm.vec3(0.0, 1.0, 0.0))
            ResourceManager.get_shader("sprite").set_vector_3f("viewPos", self.camera.position)

            self.Renderer = SpriteRenderer(ResourceManager.get_shader("sprite"))

            # init without light
            ResourceManager.load_shader("glsl/vertex.glsl", "glsl/fragment.glsl", "sprite2")
            ResourceManager.get_shader("sprite2").use().set_integer("texture1", 0)
            ResourceManager.get_shader("sprite2").set_matrix_4f("projection", projection)

            self.Renderer2 = SpriteRenderer(ResourceManager.get_shader("sprite2"))

            self.Pyramid_renderer = SpriteRenderer_pyramid(ResourceManager.get_shader("sprite"))
            self.Pyramid_renderer2 = SpriteRenderer_pyramid(ResourceManager.get_shader("sprite2"))

            # init pyhsic engine
            self.p = Physic()

            glEnable(GL_DEPTH_TEST)

        else:
            self.p = Physic()
            self.GUI = False

    def load_texture(self, name, path):
        ResourceManager.load_texture(name, path)

    def create_object(self, texture_name, orientation, position, size, geom_type="cube"):

        if geom_type == "cube":
            if self.GUI:
                texture = ResourceManager.get_texture(texture_name)
                return GameObject(self.Renderer, self.Renderer2, texture, orientation, position, size, geom_type)
            else:
                return GameObject(None, None, None, orientation, position, size, geom_type)

        elif geom_type == "pyramid":
            if self.GUI:
                texture = ResourceManager.get_texture(texture_name)
                return GameObject(self.Pyramid_renderer, self.Pyramid_renderer2, texture, orientation, position, size, geom_type)
            else:
                return GameObject(None, None, None, orientation, position, size, geom_type)


    def add_box_to_engine(self, object):
        if object.geom_type == "cube":
            size = object.size[0]
            object.box_uid = self.p.add_object(object.position, size)
        elif object.geom_type == "pyramid":
            object.box_uid = self.p.add_pyramid_object(object.position)

    def update_camera_view(self, window):
        self.currentFrame = glfw.get_time()
        deltaTime = self.currentFrame - self.lastFrame
        self.lastFrame = self.currentFrame

        self.process_input(window)

        view = self.camera.get_view_matrix()

        # light shaders
        ResourceManager.get_shader("light").set_matrix_4f("view", view, True)
        ResourceManager.get_shader("sprite").set_matrix_4f("view", view, True)
        ResourceManager.get_shader("sprite").set_vector_3f("viewPos", self.camera.position)

        # without light shaders
        ResourceManager.get_shader("sprite2").set_matrix_4f("view", view, True)

    def update_from_physic_engine(self, l):
        positionsAndOrientations = self.p.get_position(self.simulation_speed)

        for key in positionsAndOrientations:
            position = positionsAndOrientations[key][0]
            orientation = positionsAndOrientations[key][1]

            for object in l:
                if object.box_uid == key:
                    object.position = [position[0], position[2], position[1]]
                    object.orientation = orientation
                    break

    def enable_mouse(self, window):
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        glfw.set_cursor_pos_callback(window, self.mouse_callback)

    def mouse_callback(self, window, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos

        self.lastX = xpos
        self.lastY = ypos

        self.camera.process_mouse_movement(xoffset, yoffset)

    def process_input(self, window):
        self.currentFrame = glfw.get_time()
        deltaTime = self.currentFrame - self.lastFrame
        self.lastFrame = self.currentFrame

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            self.camera.process_keyboard("forward", deltaTime)

        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            self.camera.process_keyboard("backward", deltaTime)

        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            self.camera.process_keyboard("left", deltaTime)

        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            self.camera.process_keyboard("right", deltaTime)

    def init_light_shader(self):
        projection = glm.mat4(1.0)
        projection = glm.perspective(glm.radians(45.0), self.width / self.height, 0.1, 100.0)
        ResourceManager.get_shader("light").set_matrix_4f("projection", projection, True)
        self.light = Light([0.0, 2, 0.0])

    def draw_light(self):
        self.light.draw(ResourceManager.get_shader("light"))
        position = glm.vec3(self.light.position[0], self.light.position[1], self.light.position[2])
        ResourceManager.get_shader("sprite").set_vector_3f("lightPos", position, True)

    def is_L_pressed(self, window):
        if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
            return True

    def set_simulation_speed(self, x):
        self.simulation_speed = x
