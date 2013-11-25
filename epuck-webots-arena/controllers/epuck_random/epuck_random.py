from epuck import EpuckFunctions
from recorder import CsvRecorder
import behaviors
import random
from config import config

random_alpha = 0.0
timestep = 100
max_speed = 1.0
mode = "target"

recorder = None
if (config['data.record']):
    recorder = CsvRecorder(config['data.file'])
    # clear file if we should not append it to the existing file 
    if (not (config['data.append'])):
        recorder.clear()

if (mode == "wall"):
    behavior = behaviors.WallFollowingBehavior()
elif (mode == "target"):
    behavior = behaviors.TargetFollowingBehavior()
    behavior.set_target_coordinates_list([[-0.9, -0.9], [0.9, -0.9], [0.9, 0.9], [-0.9, 0.9]])
else:
    behavior = behaviors.RandomMovementBehavior()

epuck_controller = EpuckFunctions()
epuck_controller.basic_setup()

epuck_controller.update_proximities()
epuck_controller.step(timestep)

current_time = 0

while not behavior.done():
    epuck_controller.step(timestep)
    epuck_controller.update_proximities()
    current_time = current_time + timestep
    
    # sensor data    
    sensorData = {
        'current_time': current_time,
        'distance_sensor_values': epuck_controller.dist_sensor_values,
        'coordinates': epuck_controller.get_coordinates(),
        'compass_heading': epuck_controller.get_compass_heading_in_grad(),
        'camera': epuck_controller.get_average_intensity_in_grids()}

    # calculate motor speeds
    speeds = behavior.calculate_motor_speeds(sensorData)

    # add randomness
    speeds = [speeds[0] + random.uniform(-random_alpha, random_alpha), speeds[1] + random.uniform(-random_alpha, random_alpha)]
    
    # speed limit
    speeds = [min(max_speed, speeds[0]), min(max_speed, speeds[1])]

    epuck_controller.move_wheels(speeds)

    if (recorder != None):
        recorder.record(sensorData, speeds)    
