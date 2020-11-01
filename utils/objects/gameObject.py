import glm

class GameObject:
    def __init__(self, renderer, renderer2, texture, orientation, position, size, geom_type):
        self.renderer = renderer
        self.renderer2 = renderer2
        self.texture = texture
        self.orientation = orientation
        self.position = position
        self.size = size
        self.box_uid = None
        self.geom_type = geom_type

    def draw(self, light=True, GUI=True):
        if GUI:
            if light:
                self.renderer.draw_sprite(self.texture, glm.vec3(self.position[0], self.position[1], self.position[2]),
                                          glm.vec3(self.size[0], self.size[1], self.size[2]),
                                          self.orientation)

            else:
                self.renderer2.draw_sprite(self.texture, glm.vec3(self.position[0], self.position[1], self.position[2]),
                                          glm.vec3(self.size[0], self.size[1], self.size[2]),
                                          self.orientation)

        else:
            print("BoxUID: ", self.box_uid)
            print("Position: ", self.position)
            print("Orientation: ", self.orientation)



    def update(self, position, orientation):
        self.position = position
        self.orientation = orientation
