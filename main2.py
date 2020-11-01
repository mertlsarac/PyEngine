from utils import pyengine
import glfw

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

window = pyengine.create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

# engine initialization
scene = pyengine.PyEngine(SCREEN_WIDTH, SCREEN_HEIGHT)
scene.init(GUI=False)

scene.State = pyengine.State.GAME_ACTIVE

# set light
light = False

# set game object's attributes
orientation = [1.0, 0.0, 0.0,
               0.0, 1.0, 0.0,
               0.0, 0.0, 1.0]
position = [0.0, 0.0, 0.0]
size = [3.0, 0.0, 3.0]

# create ground object
ground = scene.create_object("ground", orientation, position, size)

# create boxes
boxes = []
for i in range(5):
    for j in range(5):
        for k in range(5):
            size = 0.05
            basePosition = [
                i * 5 * size + (k * size), j * 10 * size, k * 5 * size + 5
            ]
            size = [0.05, 0.05, 0.05]
            box = scene.create_object("box", orientation, basePosition, size)
            scene.add_box_to_engine(box)
            boxes.append(box)

scene.set_simulation_speed(1)

timer = glfw.get_time()
frames = updates = 0

while 1:
    now_time = glfw.get_time()
    scene.update_from_physic_engine(boxes)

    for box in boxes:
        box.draw(light=False, GUI=False)

    frames += 1

    if glfw.get_time() - timer > 1.0:
        timer += 1
        print("FPS: ", frames)
        updates = frames = 0

pyengine.terminate()
