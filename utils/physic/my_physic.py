import pybullet as p

class Physic:
    def __init__(self):
        p.connect(p.DIRECT)
        p.createCollisionShape(p.GEOM_PLANE)
        p.createMultiBody(0, 0)

        p.setGravity(0, 0, -10)
        self.objects = []

    def add_object(self, position, size):
        basePosition = position
        baseOrientation = [0, 0, 0, 1]

        self.colBoxId = p.createCollisionShape(p.GEOM_BOX, halfExtents=[size, size, size])

        mass = 1
        visualShapeId = -1

        link_Masses = [1]
        linkCollisionShapeIndices = [self.colBoxId]
        linkVisualShapeIndices = [-1]
        linkPositions = [[0, 0, 0.05]]
        linkOrientations = [[0, 0, 0, 1]]
        linkInertialFramePositions = [[0, 0, 0]]
        linkInertialFrameOrientations = [[0, 0, 0, 1]]
        indices = [0]
        jointTypes = [p.JOINT_REVOLUTE]
        axis = [[0, 0, 1]]

        self.boxUid = p.createMultiBody(mass,
                                        self.colBoxId,
                                        visualShapeId,
                                        basePosition,
                                        baseOrientation)

        p.changeDynamics(self.boxUid,
                         -1,
                         spinningFriction=0.01,
                         rollingFriction=0.01,
                         linearDamping=0.1)

        for joint in range(p.getNumJoints(self.boxUid)):
            p.setJointMotorControl2(self.boxUid, joint, p.VELOCITY_CONTROL, targetVelocity=0, force=0)

        self.objects.append(self.boxUid)
        return self.boxUid

    def add_pyramid_object(self, position):
        pyramid_start_pos = position
        pyramid_start_orientation = p.getQuaternionFromEuler([1.56, 0, 0])
        self.pyramid = p.loadURDF("utils/physic/simplecar.urdf", pyramid_start_pos, pyramid_start_orientation)

        self.objects.append(self.pyramid)
        return self.pyramid

    def get_position(self, simulation_speed):

        for i in range(simulation_speed):
            p.stepSimulation()

        positionAndOrientation = {}

        for boxUid in self.objects:
            position = list(p.getBasePositionAndOrientation(boxUid)[0])
            orientation = list(p.getBasePositionAndOrientation(boxUid)[1])
            y = orientation[2]
            orientation[2] = orientation[1]
            orientation[1] = y
            orientation = list(p.getMatrixFromQuaternion(orientation))
            # print(orientation)
            positionAndOrientationList = []
            positionAndOrientationList.append(position)
            positionAndOrientationList.append(orientation)

            positionAndOrientation[boxUid] = positionAndOrientationList

        # print(positionAndOrientation)
        return positionAndOrientation
