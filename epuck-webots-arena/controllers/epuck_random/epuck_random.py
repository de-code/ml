from epuck import EpuckFunctions
from recorder import CsvRecorder
import behaviors
import random
import math
from config import config

random_alpha = 0.2
timestep = 100
max_speed = 1.0
mode = "random"

recorder = None
if (config['data.record']):
    recorder = CsvRecorder(config['data.file'])
    # clear file if we should not append it to the existing file 
    if (not (config['data.append'])):
        recorder.clear()

if (mode == "wall"):
    behavior = behaviors.WallFollowingBehavior()
else:
    behavior = behaviors.RandomMovementBehavior()

epuck_controller = EpuckFunctions()
epuck_controller.basic_setup()

epuck_controller.update_proximities()
epuck_controller.step(timestep)

current_time = 0

while True:
    # epuck_controller.stop_moving()
    epuck_controller.update_proximities()
    epuck_controller.step(timestep)
    current_time = current_time + timestep
    
    # sensor data...
    
    # coordinates
    gps_sensors = epuck_controller.gps.getValues();
    coordinates = [gps_sensors[0], gps_sensors[2]]
    
    # compass
    compass_values = epuck_controller.compass.getValues();
    # subtract math.pi/2 (90) so that the heading is 0 facing 'north' (given x going from left to right) 
    rad = math.atan2(compass_values[0], compass_values[2]) - (math.pi / 2);
    if (rad < -math.pi):
        rad = rad + (2 * math.pi)
    compass_heading = rad / math.pi * 180.0
    
    sensorData = {
        'current_time': current_time,
        'distance_sensor_values': epuck_controller.dist_sensor_values,
        'coordinates': coordinates,
        'compass_heading': compass_heading,
        'camera': epuck_controller.get_average_intensity_in_grids()}
    
    #print "compass: ", compass_values, ", compass_heading: ", compass_heading, ", rad: ", rad

    # calculate motor speeds
    speeds = behavior.calculate_motor_speeds(sensorData)

    # add randomness
    speeds = [speeds[0] + random.uniform(-random_alpha, random_alpha), speeds[1] + random.uniform(-random_alpha, random_alpha)]
    
    # speed limit
    speeds = [min(max_speed, speeds[0]), min(max_speed, speeds[1])]

    epuck_controller.move_wheels(speeds)

    if (recorder != None):
        recorder.record(sensorData, speeds)    
