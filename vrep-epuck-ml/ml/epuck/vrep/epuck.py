
class EPuck(object):
    def __init__(self, connection, suffix = ''):
        self.connection = connection
        self.bodyElements = connection.getObject('ePuck_bodyElements' + suffix)
        self.leftMotor = connection.getObject('ePuck_leftJoint' + suffix)
        self.rightMotor = connection.getObject('ePuck_rightJoint' + suffix)
        self.ePuck = connection.getObject('ePuck' + suffix)
        self.ePuckBase = connection.getObject('ePuck_base' + suffix)
        self.ledLight = connection.getObject('ePuck_ledLight' + suffix)
        self.proximitySensors = [-1, -1, -1, -1, -1, -1, -1, -1]
        for i in range(8):
            self.proximitySensors[i] = connection.getObject('ePuck_proxSensor' + str(1 + i) + suffix)

    @staticmethod
    def findAll(connection):
        baseObjectName = 'ePuck';
        objectNames = connection.getObjectInstanceNames(baseObjectName)
        return map(lambda objectName: EPuck(connection, objectName[len(baseObjectName):]), objectNames)
