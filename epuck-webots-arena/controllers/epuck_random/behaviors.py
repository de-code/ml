import numpy
import math

class Behavior:
    def calculate_motor_speeds(self, sensorData):
        print "Not implemented"

    def done(self):
        return False

    def first_iteration(self):
        return False

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

class TargetFollowingBehavior (Behavior):
    def __init__(self):
        self.distance_tolerance = 0.01
        self.angel_tolerance = 0.5
        self.turn_speed = 0.5
        self.repeat = True
        self.reverse = False
        self.target_coordinates_index = 0
        self.target_coordinates_list = []
        self.iteration_count = 0
        
    def set_target_coordinates_list(self, target_coordinates_list, reverse=False):
        self.target_coordinates_list = target_coordinates_list
        self.reverse = reverse
        self.target_coordinates_index = self.first_target_index()
        self.iteration_count = 0
        print "first target: " + self.current_target_description()
        
    def done(self):
        return ((self.target_coordinates_index >= len(self.target_coordinates_list)) or (self.target_coordinates_index < 0))
    
    def first_iteration(self):
        return (self.iteration_count == 0) or ((self.reverse) and (self.iteration_count == 1) and (self.target_coordinates_index == self.first_target_index()))

    def first_target_index(self):
        return len(self.target_coordinates_list) - 1 if self.reverse else 0

    def next_target_index(self):
        return self.target_coordinates_index - 1 if self.reverse else self.target_coordinates_index + 1

    def next_target(self):
        self.target_coordinates_index = self.next_target_index()
        if ((self.repeat) and (self.done())):
            self.target_coordinates_index = self.first_target_index()
            self.iteration_count = self.iteration_count + 1

    def current_target_description(self):
        if (self.done()):
            return "none (done)"
        else:
            target_coordinates = self.target_coordinates_list[self.target_coordinates_index]
            return str(self.target_coordinates_index) + " (" + str(target_coordinates) + ")"

    def distance(self, v):
        return math.sqrt(v[0] * v[0] + v[1] * v[1]);

    def normalize(self, v):
        n = self.distance(v);
        if (n == 0.0):
            # avoid division by zero where both values are zero, any value will result in the same return value (zero)
            n = 1.0
        return [v[0] / n, v[1] / n];

    def angle_and_distance_to_target(self, target_coordinates, coordinates, compass_heading):
        relative_target_coordinates = [target_coordinates[0] - coordinates[0], target_coordinates[1] - coordinates[1]]
        distance = self.distance(relative_target_coordinates)
        normalised = self.normalize(relative_target_coordinates)
        # negate y (actually z), as this is where the compass is heading towards
        rad = math.atan2(normalised[0], -normalised[1])
        if (rad < -math.pi):
            rad = rad + (2 * math.pi)
        abs_angle = rad / math.pi * 180.0
        #print "compass heading: ", compass_heading, ", target: ", abs_angle, ", relative_target_coordinates: ", relative_target_coordinates, ", target_coordinates:", target_coordinates
        angle = abs_angle - compass_heading
        if (angle < -180.0):
            angle = angle + 360.0
        if (angle >= 180.0):
            angle = angle - 360.0
        return angle, distance

    def calculate_motor_speeds(self, sensorData):
        if (self.done()):
            print "done, ", self.target_coordinates_index
            speeds = [0.0, 0.0]
        else:
            target_coordinates = self.target_coordinates_list[self.target_coordinates_index]
            angle, distance = self.angle_and_distance_to_target(target_coordinates, sensorData['coordinates'], sensorData['compass_heading'])
            if (distance < self.distance_tolerance):
                print "target reached: ", self.current_target_description()
                self.next_target()
                print "next target: " + self.current_target_description()
                # calculate the speeds to reach the next target
                speeds = self.calculate_motor_speeds(sensorData)
            else:
                beta = -(((angle * math.pi) / 180.0))
                if (beta > self.angel_tolerance):
                    speeds = [-self.turn_speed, self.turn_speed]
                elif (beta < -self.angel_tolerance):
                    speeds = [self.turn_speed, -self.turn_speed]
                else:
                    speeds = [1 - (math.pi + beta) / 10, 1 - (math.pi - beta) / 10]
                #print "target heading: ", angle, ", beta: ", beta, ", speeds: ", speeds
        return speeds
