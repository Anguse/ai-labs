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
import random
import math

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))
# initially standing still
motorSpeed = dict(speedLeft=0, speedRight=0)
# timing for movement sequence
currentSequenceTime = 0
lastSequenceEnd = 0

# return forward or backwards
def getRandomDirection():
    directions = [dict(speedLeft=1, speedRight=1),dict(speedLeft=-1, speedRight=-1)]
    direction = random.choice(directions)
    return direction

# return 0/90/180/270 degree turn
def getRandomTurn():
    turns = [0,90,180,270]    
    turn = random.choice(turns)
    return turn

//Initials
turn = 0
while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime % 1000 == 0:
        # print some useful info, but not too often
        print 'Time:',simulationTime,\
              'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
              "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight")

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    currentSequenceTime = simulationTime-lastSequenceEnd
    if currentSequenceTime % 5000 == 0:
        turn = getRandomTurn()
    print 'Making a ', turn, ' degree turn'
    if turn != 0:
        World.execute(dict(speedLeft=1, speedRight=-1), 28*turn, -1)

        motorSpeed = getRandomDirection()
    lastSequenceEnd = World.getSimulationTime()
    print lastSequenceEnd
        
    #######################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    #if simulationTime%10000==0:
    #    print "Trying to collect a block...",World.collectNearestBlock()
