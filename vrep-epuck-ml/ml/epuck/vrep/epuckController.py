import time
import math

class EPuckController(object):
    def __init__(self, ePuck):
        self.ePuck = ePuck
        self.maxVel = 120 * math.pi / 180
        self.ledColors = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        
        # Braitenberg weights for the 4 front prox sensors (avoidance):
        self.braitFrontSens_leftMotor = [1, 2, -2, -1]
        # Braitenberg weights for the 2 side prox sensors (following):
        self.braitSideSens_leftMotor = [-1, 0]
        # Braitenberg weights for the 8 sensors (following):
        self.braitAllSensFollow_leftMotor = [-3, -1.5, -0.5, 0.8, 1, 0, 0, -4]
        self.braitAllSensFollow_rightMotor = [0, 1, 0.8, -0.5, -1.5, -3, -4, 0]
        self.braitAllSensAvoid_leftMotor = [0, 0.5, 1, -1, -0.5, -0.5, 0, 0]
        self.braitAllSensAvoid_rightMotor = [-0.5, -0.5, -1, 1, 0.5, 0, 0, 0]
        
        self.relLedPositions = [[-0.0343, 0, 0.0394], [-0.0297, 0.0171, 0.0394], [0, 0.0343, 0.0394],
                    [0.0297, 0.0171, 0.0394], [0.0343, 0, 0.0394], [0.0243, -0.0243, 0.0394],
                    [0.006, -0.0338, 0.0394], [-0.006, -0.0338, 0.0394], [-0.0243, -0.0243, 0.0394]]
        self.drawingObject = False

    def actualizeLEDs(self):
    #         if (relLedPositions==nil):
    #             relLedPositions=[[-0.0343,0,0.0394],[-0.0297,0.0171,0.0394],[0,0.0343,0.0394],
    #                         [0.0297,0.0171,0.0394],[0.0343,0,0.0394],[0.0243,-0.0243,0.0394],
    #                         [0.006,-0.0338,0.0394],[-0.006,-0.0338,0.0394],[-0.0243, -0.0243,0.0394]]
        
#        if (self.drawingObject):
#            simRemoveDrawingObject(drawingObject)
            
#        type = vrep.sim_drawing_painttag + vrep.sim_drawing_followparentvisibility + vrep.sim_drawing_spherepoints + \
#             vrep.sim_drawing_50percenttransparency + vrep.sim_drawing_itemcolors + vrep.sim_drawing_itemsizes + \
#             vrep.sim_drawing_backfaceculling + vrep.sim_drawing_emissioncolor
        # drawingObject = vrep.simxAddDrawingObject(clientID, type, 0, 0, bodyElements, 27, vrep.simx_opmode_oneshot_wait)
        # m = vrep.simxGetObjectMatrix(clientID, ePuckBase, -1, vrep.simx_opmode_oneshot_wait)
#        itemData = [0, 0, 0, 0, 0, 0, 0]
        # vrep.simxSetLightParameters(clientID, ledLight, 0, vrep.simx_opmode_oneshot_wait)
    #         for i in range(9):
    #             if (ledColors[i][0] + ledColors[i][1] + ledColors[i][2] != 0):
    #                 p = vrep.simxMultiplyVector(clientID, m, relLedPositions[i], vrep.simx_opmode_oneshot_wait)
    #                 itemData[0] = p[0]
    #                 itemData[1] = p[1]
    #                 itemData[2] = p[2]
    #                 itemData[3] = ledColors[i][0]
    #                 itemData[4] = ledColors[i][1]
    #                 itemData[5] = ledColors[i][2]
    #                 vrep.simxSetLightParameters(clientID, ledLight, 1, [ledColors[i][1], ledColors[i][2], ledColors[i][3]], vrep.simx_opmode_oneshot_wait)
    #                 for j in range(3):
    #                     itemData[7] = j * 0.003
    #                     #simAddDrawingObjectItem(clientID, drawingObject, itemData, vrep.simx_opmode_oneshot_wait)
        return
    
    def reset(self):
        for i in range(9):
            # no light
            self.ledColors[i] = {0, 0, 0} 
        self.actualizeLEDs()
            
    def getLightSensors(self):
    #         data=vrep.simxReceiveData(clientID,0,'EPUCK_lightSens')
    #         if (data):
    #             lightSens=simUnpackFloats(data)
    #         return lightSens
        return 0

    def process(self):
        # st=vrep.simxGetSimulationTime(clientID)
        st = time.clock()
        velLeft = 0
        velRight = 0
    #        opMode=vrep.simxGetScriptSimulationParameter(clientID, sim_handle_self,'opMode')
        opMode = 0
        lightSens = self.getLightSensors()
        # make sure that if we scale the robot during simulation, other values are scaled too!
    #        s=vrep.simxGetObjectSizeFactor(clientID, bodyElements, vrep.simx_opmode_oneshot_wait)
        s = 1
        noDetectionDistance = 0.05 * s
        proxSensDist = [noDetectionDistance, noDetectionDistance, noDetectionDistance, noDetectionDistance, noDetectionDistance, noDetectionDistance, noDetectionDistance, noDetectionDistance]
        for i in range(8):
            reading = self.ePuck.proximitySensors[i].readProximitySensor()
            if ((reading.detectionState) and (reading.distance < noDetectionDistance)):
                proxSensDist[i] = reading.distance
        # We wanna follow the line
        if (opMode == 0): 
            if ((st % 2) > 1.5):
                intensity = 1
            else:
                intensity = 0
                
            for i in range(9):
                # red
                self.ledColors[i] = [intensity, 0, 0]
                
            # Now make sure the light sensors have been read, we have a line and the 4 front prox. sensors didn't detect anything:
            if lightSens and ((lightSens[1] < 0.5)or(lightSens[2] < 0.5)or(lightSens[3] < 0.5)) and (proxSensDist[2] + proxSensDist[3] + proxSensDist[4] + proxSensDist[5] == noDetectionDistance * 4):
                if (lightSens[1] > 0.5):
                    velLeft = self.maxVel
                else:
                    velLeft = self.maxVel * 0.25
                    
                if (lightSens[3] > 0.5): 
                    velRight = self.maxVel
                else:
                    velRight = self.maxVel * 0.25
                    
            else:
                velRight = self.maxVel
                velLeft = self.maxVel
                if (proxSensDist[2] + proxSensDist[3] + proxSensDist[4] + proxSensDist[5] == noDetectionDistance * 4):
                    # Nothing in front. Maybe we have an obstacle on the side, in which case we wanna keep a constant distance with it:
                    if (proxSensDist[1] > 0.25 * noDetectionDistance):
                        velLeft = velLeft + self.maxVel * self.braitSideSens_leftMotor[0] * (1 - (proxSensDist[0] / noDetectionDistance))
                        velRight = velRight + self.maxVel * self.braitSideSens_leftMotor[1] * (1 - (proxSensDist[0] / noDetectionDistance))
    
                    if (proxSensDist[6] > 0.25 * noDetectionDistance):
                        velLeft = velLeft + self.maxVel * self.braitSideSens_leftMotor[1] * (1 - (proxSensDist[5] / noDetectionDistance))
                        velRight = velRight + self.maxVel * self.braitSideSens_leftMotor[0] * (1 - (proxSensDist[5] / noDetectionDistance))
                        
                else:
                    # Obstacle in front. Use Braitenberg to avoid it
                    for i in range(3):
                        velLeft = velLeft + self.maxVel * self.braitFrontSens_leftMotor[i] * (1 - (proxSensDist[1 + i] / noDetectionDistance))
                        velRight = velRight + self.maxVel * self.braitFrontSens_leftMotor[3 - i] * (1 - (proxSensDist[1 + i] / noDetectionDistance))
    
        # We wanna follow something!
        if (opMode == 1):
            index = math.floor(1 + (st * 3 % 9))
            for i in range(9):
                if (index == i):
                    # light blue
                    self.ledColors[i] = {0, 0.5, 1} 
                else:
                    # off
                    self.ledColors[i] = {0, 0, 0} 
                    
            velRightFollow = self.maxVel
            velLeftFollow = self.maxVel
            minDist = 1000
            for i in range(8):
                velLeftFollow = velLeftFollow + self.maxVel * self.braitAllSensFollow_leftMotor[i] * (1 - (proxSensDist[i] / noDetectionDistance))
                velRightFollow = velRightFollow + self.maxVel * self.braitAllSensFollow_rightMotor[i] * (1 - (proxSensDist[i] / noDetectionDistance))
                if (proxSensDist[i] < minDist):
                    minDist = proxSensDist[i]
    
            velRightAvoid = 0
            velLeftAvoid = 0
            for i in range(8):
                velLeftAvoid = velLeftAvoid + self.maxVel * self.braitAllSensAvoid_leftMotor[i] * (1 - (proxSensDist[i] / noDetectionDistance))
                velRightAvoid = velRightAvoid + self.maxVel * self.braitAllSensAvoid_rightMotor[i] * (1 - (proxSensDist[i] / noDetectionDistance))
    
            if (minDist > 0.025 * s):
                minDist = 0.025 * s
            t = minDist / (0.025 * s)
            velLeft = velLeftFollow * t + velLeftAvoid * (1 - t)
            velRight = velRightFollow * t + velRightAvoid * (1 - t)
    
        self.ePuck.leftMotor.setJointTargetVelocity(velLeft)
        self.ePuck.rightMotor.setJointTargetVelocity(velRight)
        self.actualizeLEDs()
        # Don't waste too much time in here (simulation time will anyway only change in next thread switch)
        #vrep.simxSwitchThread(clientID, vrep.simx_opmode_oneshot_wait)

