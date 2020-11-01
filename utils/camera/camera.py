import math

import glm
import glfw

class Camera:
    def __init__(self):
        # set first position of the camera
        self.position = glm.vec3(1.0, 1.0, 4.0)
        self.worldUp = glm.vec3(0.0, 1.0, 0.0)

        self.front = glm.vec3(0.0, 0.0, -1.0)

        self.movementSpeed = 10000.0
        self.mouseSensitivity = 0.5
        self.zoom = 45.0
        # set yaw and pitch
        self.yaw = -90.0
        self.pitch = 0.0

        self.__update_camera_vectors()

    def __update_camera_vectors(self):
        front = glm.vec3()

        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))

        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(front, self.worldUp))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def process_keyboard(self, direction, deltaTime):
        velocity = self.movementSpeed * deltaTime
        # print(direction)
        if direction == "forward":
            self.position += self.front * velocity
        if direction == "backward":
            self.position -= self.front * velocity
        if direction == "left":
            self.position -= self.right * velocity
        if direction == "right":
            self.position += self.right * velocity

    def process_mouse_movement(self, xoffset, yoffset, constrainPitch=True):
        xoffset *= self.mouseSensitivity
        yoffset *= self.mouseSensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrainPitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0

        self.__update_camera_vectors()

    def process_mouse_scroll(self, yoffset):
        self.zoom -= float(yoffset)

        if self.zoom < 1.0:
            self.zoom = 1
        if self.zoom > 45.0:
            self.zoom = 45.0

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

