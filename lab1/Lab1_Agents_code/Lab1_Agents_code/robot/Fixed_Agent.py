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
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))
while 1:
    simulationTime = World.getSimulationTime()
    if simulationTime < 5000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
    elif simulationTime < 15000:
        if World.robotDirection() > 0.001:
            motorSpeed = (dict(speedLeft=-0.5, speedRight=0.5))
        else:
            motorSpeed = dict(speedLeft=0, speedRight=0)
    elif simulationTime < 25000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
    elif simulationTime < 35000:
        motorSpeed = dict(speedLeft=-2, speedRight=-2)
    elif simulationTime < 45000:
        if World.robotDirection() < 1.5:
            motorSpeed = (dict(speedLeft=0.5, speedRight=-0.5))
        else:
            motorSpeed = dict(speedLeft=0, speedRight=0)
    elif simulationTime < 71000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
    elif simulationTime < 85000:
        if World.robotDirection() > 0.001:
            motorSpeed = (dict(speedLeft=-0.5, speedRight=0.5))
        else:
            motorSpeed = dict(speedLeft=0, speedRight=0)
    elif simulationTime < 116000:
        motorSpeed = dict(speedLeft=2, speedRight=2)
    else:
        motorSpeed = dict(speedLeft=0, speedRight=0)
    World.collectNearestBlock()
    World.setMotorSpeeds(motorSpeed)
