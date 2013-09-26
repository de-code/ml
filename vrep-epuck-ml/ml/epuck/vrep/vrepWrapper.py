import vrep
import math
from collections import namedtuple

VrepProximitySensorResult = namedtuple('VrepProximitySensorResult', 'detectionState distance detectedPoint detectedObjectHandle detectedSurfaceNormalVector')

class VrepObject(object):
    def __init__(self, connection, handle):
        self.connection = connection
        self.handle = handle
        
    def readProximitySensor(self, operationMode = vrep.simx_opmode_oneshot_wait):
        return self.connection.readProximitySensor(self.handle, operationMode)

    def setJointTargetVelocity(self, targetVelocity, operationMode = vrep.simx_opmode_oneshot_wait):
        return self.connection.setJointTargetVelocity(self.handle, targetVelocity, operationMode)

class VrepConnection(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientID = vrep.simxStart(host, port, True, True, 5000, 5)
        if (not self.connected()):
            raise Exception('Unable to connect to vrep server', host, port)

    def connected(self):
        return self.clientID != -1

    def disconnect(self):
        return vrep.simxFinish(self.clientID)
    
    def handleErrorCode(self, errorCode):
        if (errorCode != 0):
            raise Exception('Unexpected error', errorCode)

    def raw_getObjectGroupData(self, objectType, dataType, operationMode = vrep.simx_opmode_oneshot_wait):
        return vrep.simxGetObjectGroupData(self.clientID, objectType, dataType, operationMode)

    def getObjectNames(self, objectType = vrep.sim_appobj_object_type, operationMode = vrep.simx_opmode_oneshot_wait):
        errorCode, handles, intData, floatData, stringData = self.raw_getObjectGroupData(objectType, 0, operationMode)
        self.handleErrorCode(errorCode)
        return stringData

    def getObjectInstanceNames(self, baseObjectName, objectType = vrep.sim_appobj_object_type, operationMode = vrep.simx_opmode_oneshot_wait):
        objectNames = self.getObjectNames(objectType, operationMode)
        return [objectName for objectName in objectNames
                if ((objectName == baseObjectName) or
                    objectName.startswith(baseObjectName + '#'))]

    def getObjects(self, objectType, operationMode = vrep.simx_opmode_oneshot_wait):
        return vrep.simxGetObjects(self.clientID, objectType, operationMode)

    def raw_getObjectHandle(self, objectName, operationMode = vrep.simx_opmode_oneshot_wait):
        return vrep.simxGetObjectHandle(self.clientID, objectName, operationMode)

    def getObjectHandle(self, objectName, operationMode = vrep.simx_opmode_oneshot_wait):
        res, handle = self.raw_getObjectHandle(objectName, operationMode)
        self.handleErrorCode(res)
        return handle

    def getObject(self, objectName, operationMode = vrep.simx_opmode_oneshot_wait):
        return VrepObject(self, self.getObjectHandle(objectName, operationMode))

    def objectExists(self, objectName, operationMode = vrep.simx_opmode_oneshot_wait):
        result = self.raw_getObjectHandle(objectName, operationMode)
        return result[0] == 0

    def setJointTargetVelocity(self, jointHandle, targetVelocity, operationMode = vrep.simx_opmode_oneshot_wait):
        return vrep.simxSetJointTargetVelocity(self.clientID, jointHandle, targetVelocity, operationMode)

    def raw_readProximitySensor(self, sensorHandle, operationMode = vrep.simx_opmode_oneshot_wait):
        return vrep.simxReadProximitySensor(self.clientID, sensorHandle, operationMode)

    def readProximitySensor(self, sensorHandle, operationMode = vrep.simx_opmode_oneshot_wait):
        res, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = self.raw_readProximitySensor(sensorHandle, operationMode)
        self.handleErrorCode(res)
        distance =  math.sqrt(sum([x ** 2 for x in detectedPoint]))
        return VrepProximitySensorResult(detectionState, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector)

class VrepWrapper(object):
    
    def connect(self, host, port):
        return VrepConnection(host, port)
