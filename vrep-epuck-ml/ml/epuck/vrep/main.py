from math import pi
import vrepWrapper
import epuck
import epuckController
from config import config

print 'Program started'
vrepWrapper = vrepWrapper.VrepWrapper()
print 'Connecting to: ' + config['host'] + ':' + str(config['port'])
connection = vrepWrapper.connect(config['host'], config['port'])
print 'Connected to remote API server'

ePuckList = epuck.EPuck.findAll(connection)
if (len(ePuckList) == 0):
    print 'No e-puck found!'
else:
    print 'Found', len(ePuckList), 'e-puck(s)'
    
    controllerList = map(lambda ePuck: epuckController.EPuckController(ePuck), ePuckList)
    
    #    while (vrep.simxGetSimulationState(clientID)!=sim_simulation_advancing_abouttostop):
    while (True):
        for controller in controllerList:
            controller.process()
    
    for controller in controllerList:
        controller.reset()

connection.disconnect()

print 'Program ended'
