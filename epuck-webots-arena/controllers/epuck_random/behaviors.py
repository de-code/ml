import numpy

class Behavior:
    def calculate_motor_speeds(self, sensorData):
        print "Not implemented"

class RandomMovementBehavior (Behavior):
    def __init__(self):
        self.sensor_factor = 900

    def calculate_motor_speeds(self, sensorData):
        distance_sensor_values = sensorData['distance_sensor_values']
        left_sensors = distance_sensor_values[0:4]
        right_sensors = distance_sensor_values[4:8]
        sensor_factor = self.sensor_factor
        if ((numpy.max(left_sensors) >= 200) and (numpy.max(right_sensors) >= 200)):
            speeds = [numpy.sum(right_sensors)/sensor_factor, -numpy.sum(left_sensors)/sensor_factor]
        else:
            speeds = [numpy.sum(right_sensors)/sensor_factor, numpy.sum(left_sensors)/sensor_factor]
        return speeds

class WallFollowingBehavior (Behavior):
    def __init__(self):
        self.weights_left =  [-0.5078135186133784, 0.7222157247342318, 0.16710861504732655, 0.8424141006027197, -0.6450806300178749, 0.35411263077168975, -0.10513930708875899, -0.8255870801456526, 0.5978402786160035, 0.571675635961613, -0.18152760189205397, 0.7066086455047382, -0.8896903957861825, -0.7474154866963203, -0.21436170231816987, 0.5906249468113174][0:8]
        self.weights_right =  [-0.5078135186133784, 0.7222157247342318, 0.16710861504732655, 0.8424141006027197, -0.6450806300178749, 0.35411263077168975, -0.10513930708875899, -0.8255870801456526, 0.5978402786160035, 0.571675635961613, -0.18152760189205397, 0.7066086455047382, -0.8896903957861825, -0.7474154866963203, -0.21436170231816987, 0.5906249468113174][8:16]

    def calculate_motor_speeds(self, sensorData):
        distance_sensor_values = sensorData['distance_sensor_values']
        left = 0.0
        right = 0.0
        for i in range(0, len(self.weights_left)):
            left += float(self.weights_left[i] * (distance_sensor_values[i])/1000.0)
        for i in range(0, len(self.weights_right)):
            right += float(self.weights_right[i]*(distance_sensor_values[i])/1000.0)
        return [left, right]
