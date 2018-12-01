# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
import math
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))

while 1:

    simulationTime = World.getSimulationTime()
    leftSensor = World.getSensorReading("ultraSonicSensorLeft")
    rightSensor = World.getSensorReading("ultraSonicSensorRight")
    energySensor = World.getSensorReading("energySensor")
    robotDirection = math.degrees(World.robotDirection())  # Direction robot is facing in degrees
    robotPosition = World.robotPosition()
    energyBlocks = World.findEnergyBlocks()
    blockHandle, blockName, blockDistance, blockDirection = energyBlocks[0]
    blockDirection = math.degrees(blockDirection)

    # Facing a wall, go backwards and turn 90 degrees
    if leftSensor < 0.3 and rightSensor < 0.3:
        print "Facing wall, going back"
        motorSpeed = (dict(speedLeft=-2, speedRight=-2))
        World.execute(motorSpeed, 2500, -1)
        motorSpeed = (dict(speedLeft=-0.5, speedRight=0.5))
        World.execute(motorSpeed, 2500, -1)
    # Left/Right sensor too close? Turn the other direction
    elif leftSensor <= 0.7:
        print "Turn a little left"
        motorSpeed = dict(speedLeft=2, speedRight=0.5)
    elif rightSensor <= 0.7:
        print "Turn a little right"
        motorSpeed = dict(speedLeft=0.5, speedRight=2)
    # Block nearby and not stuck, head towards the block
    elif blockDistance <= 1.6:
        # Get the correct angle
        if blockDirection <= 0.5:
            motorSpeed = dict(speedLeft=-0.5, speedRight=0.5)
        elif blockDirection < -0.5:
            motorSpeed = dict(speedLeft=0.5, speedRight=-0.5)
        else:
            motorSpeed = dict(speedLeft=2, speedRight=2)
    # Otherwise just go forward
    else:
        motorSpeed = dict(speedLeft=2, speedRight=2)

    World.collectNearestBlock()
    World.setMotorSpeeds(motorSpeed)
