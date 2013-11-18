from epuck import EpuckFunctions
import numpy
import random
import csv
from config import config

sensor_factor = 900
speed_offset = 0.01
random_alpha = 0.2
step_size = 100
max_speed = 1.0
mode = "wall"
epuck_controller = EpuckFunctions()
epuck_controller.basic_setup()

# clear file if we should append it to the existing file 
if ((config['data.record']) and (not (config['data.append']))):
    with open(config['data.file'], "wb") as f:
        f.close()

weights_left =  [-0.5078135186133784, 0.7222157247342318, 0.16710861504732655, 0.8424141006027197, -0.6450806300178749, 0.35411263077168975, -0.10513930708875899, -0.8255870801456526, 0.5978402786160035, 0.571675635961613, -0.18152760189205397, 0.7066086455047382, -0.8896903957861825, -0.7474154866963203, -0.21436170231816987, 0.5906249468113174][0:8]
weights_right =  [-0.5078135186133784, 0.7222157247342318, 0.16710861504732655, 0.8424141006027197, -0.6450806300178749, 0.35411263077168975, -0.10513930708875899, -0.8255870801456526, 0.5978402786160035, 0.571675635961613, -0.18152760189205397, 0.7066086455047382, -0.8896903957861825, -0.7474154866963203, -0.21436170231816987, 0.5906249468113174][8:16]
epuck_controller.update_proximities()
epuck_controller.step(step_size)

current_time = 0

while True:
    # epuck_controller.stop_moving()
    epuck_controller.update_proximities()
    epuck_controller.step(step_size)
    current_time = current_time + step_size
    dist_sensor_values = epuck_controller.dist_sensor_values
    left_sensors = dist_sensor_values[0:4];
    right_sensors = dist_sensor_values[4:8];
    r1 = random.uniform(-random_alpha, random_alpha)
    r2 = random.uniform(-random_alpha, random_alpha)
    speeds = [0, 0]
    if (mode == "wall"):
        left = 0.0
        right = 0.0
        for i in range(0,len(weights_left)):
            left += float(weights_left[i]*(epuck_controller.dist_sensor_values[i])/1000.0)
        for i in range(0,len(weights_right)):
            right += float(weights_right[i]*(epuck_controller.dist_sensor_values[i])/1000.0)
        #speeds = [left * 0.9, right * 0.9]
        speeds = [min(max_speed, left + r1), min(max_speed, right + r2)]
        #speeds = [max(0.9, left * 0.9 + r1), max(0.9, right * 0.9 + r2)]
    else:
        if ((numpy.max(left_sensors) >= 200) and (numpy.max(right_sensors) >= 200)):
            speeds = [numpy.sum(right_sensors)/sensor_factor + r1, -numpy.sum(left_sensors)/sensor_factor + r2]
        else:
            speeds = [numpy.sum(right_sensors)/sensor_factor + r1, numpy.sum(left_sensors)/sensor_factor + r2]
        epuck_controller.move_wheels(speeds)

    epuck_controller.move_wheels(speeds)

    gps_sensors = epuck_controller.gps.getValues();
    coordinates = [gps_sensors[0], gps_sensors[2]]
    camera = epuck_controller.get_average_intensity_in_grids();
    row = [current_time] + dist_sensor_values + coordinates + speeds + camera
    #sensors.append(gps_sensors[0])
    #sensors.append(gps_sensors[2])
    #sensors.append(speeds[0])
    #sensors.append(speeds[1])
    
    # append current sensor data 
    if (config['data.record']):
        with open(config['data.file'], "ab") as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
            f.close()
    
    #epuck_controller.step(200)
    #print "Sensors:"
    #pprint.pprint(dist_sensor_values)
    #print epuck_controller.gps.getValues()
    #print epuck_controller
