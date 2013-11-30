from epuck import EpuckFunctions
from recorder import CsvRecorder
import behaviors
import random
import datetime
#import sys
import os
from config import config

random_alpha = config['randomness']
time_step_size = config['time.step.size']
time_step_count = config['time.step.count']
max_speed = 1.0
mode = config['mode']

actual_time = datetime.datetime.now()
ignore_first_iteration = False

description = "time.step.size=" + str(time_step_size) + "\ntime.step.count=" + str(time_step_count) + "\nrandomness=" + str(random_alpha) + "\nmode=" + mode 
if (mode == "wall"):
    behavior = behaviors.WallFollowingBehavior()
elif (mode == "path"):
    behavior = behaviors.TargetFollowingBehavior()
    behavior.set_target_coordinates_list(config['targets'], config['targets.reverse'])
    description = description + "\ntargets=" + str(config['targets'])
    description = description + "\ntargets.reverse=" + str(config['targets.reverse'])
    ignore_first_iteration = config['targets.reverse']
elif (mode == "random"):
    behavior = behaviors.RandomMovementBehavior()
else:
    raise Exception("invalid mode: " + str(mode))

print "description=\n", description

epuck_controller = EpuckFunctions()
epuck_controller.basic_setup(time_step_size)

recorder = None
if (config['data.record']):
    actual_time_formatted = actual_time.strftime("%Y-%m-%d-%H-%M")
    home = os.path.dirname(os.path.realpath(__file__))
    name = epuck_controller.getName()
    file_name = config['data.file'].format(home=home, datetime=actual_time_formatted, name=name, mode=mode)
    print "recording to: ", file_name
    recorder = CsvRecorder(file_name)
    recorder.prepare()
    # clear file if we should not append it to the existing file 
    if (not (config['data.append'])):
        recorder.clear()
    recorder.info(description)
    #sys.exit(0)

current_time = 0
time_step_index = 0
first_time_step_index = -1

while (((time_step_count == 0) or (first_time_step_index < 0) or (time_step_index - first_time_step_index < time_step_count)) and (not behavior.done())):
    epuck_controller.step(time_step_size)
    current_time = current_time + time_step_count
    time_step_index = time_step_index + 1

    epuck_controller.update_proximities()
    
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
        if ((not ignore_first_iteration) or (not behavior.first_iteration())):
            if (first_time_step_index < 0):
                first_time_step_index = (time_step_index - 1)
            recorder.record(sensorData, speeds)    

# reset speeds
epuck_controller.move_wheels([0, 0])
