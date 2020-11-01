from utils import pyengine
import glfw

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

window = pyengine.create_window(SCREEN_WIDTH, SCREEN_HEIGHT)

# engine initialization
scene = pyengine.PyEngine(SCREEN_WIDTH, SCREEN_HEIGHT)
scene.init()

scene.enable_mouse(window)
scene.State = pyengine.State.GAME_ACTIVE

# load textures
scene.load_texture("box", "resources/textures/container.jpg")
scene.load_texture("ground", "resources/textures/wall2.jpg")
scene.load_texture("pyramid", "resources/textures/pyramid.jpg")
scene.load_texture("grass", "resources/textures/grass.jpg")
# set light
light = False

# set game object's attributes
orientation = [1.0, 0.0, 0.0,
               0.0, 1.0, 0.0,
               0.0, 0.0, 1.0]
position = [0.0, 0.0, 0.0]
size = [10.0, 10.0, 10.0]

# create ground object
ground = scene.create_object("ground", orientation, position, size)
size = [10.0, 0.0, 10.0]
ground2 = scene.create_object("grass", orientation, position, size)

# create boxes
boxes = []
for i in range(5):
    for j in range(5):
        for k in range(5):
            size = 0.1
            basePosition = [
                i * 5 * size + (k * size), j * 10 * size, k * 5 * size + 5
            ]
            size = [0.05, 0.05, 0.05]
            box = scene.create_object("box", orientation, basePosition, size)
            scene.add_box_to_engine(box)
            boxes.append(box)

#create pyramid object
size = 0.8
orientation = [1.0, 0.0, 0.0,
               0.0, 1.0, 0.0,
               0.0, 0.0, 1.0]
position = [0.4, 1, 5]
size = [size, size, size]
pyramid = scene.create_object("pyramid", orientation, position, size, geom_type="pyramid")
scene.add_box_to_engine(pyramid)
boxes.append(pyramid)

#create pyramid object 2
orientation = [1.0, 0.0, 0.0,
               0.0, 1.0, 0.0,
               0.0, 0.0, 1.0]
position = [0.4, 2, 8]
pyramid = scene.create_object("pyramid", orientation, position, size, geom_type="pyramid")
scene.add_box_to_engine(pyramid)
boxes.append(pyramid)

scene.set_simulation_speed(1)
scene.init_light_shader()

timer = glfw.get_time()
frames = updates = 0
while not pyengine.window_should_close(window):
    now_time = glfw.get_time()

    pyengine.poll_events()

    if scene.is_L_pressed(window):
        light = True

    pyengine.clear_color()

    scene.update_camera_view(window)

    ground.draw(light)
    ground2.draw(light)

    scene.update_from_physic_engine(boxes)

    for box in boxes:
        box.draw(light)

   #pyramid.draw(light)
    if light:
        scene.draw_light()

    light = False
    pyengine.swap_buffers(window)
    frames += 1

    if glfw.get_time() - timer > 1.0:
        timer += 1
        print("FPS: ", frames)
        updates = frames = 0

pyengine.terminate()
