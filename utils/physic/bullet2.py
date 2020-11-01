import pybullet as p
import pybullet_data
import time

client = p.connect(p.GUI)

p.createCollisionShape(p.GEOM_PLANE)
p.createMultiBody(0, 0)
p.setGravity(0, 0, -10)


#planeId = p.loadURDF("plane.urdf")

pyramid_start_pos = [0, 0, 10]
pyramid_start_orientation = p.getQuaternionFromEuler([1.56, 0, 0])

pyramid = p.loadURDF("simplecar.urdf", pyramid_start_pos, pyramid_start_orientation)

for i in range(100000):
    p.stepSimulation()
    time.sleep(1./240)