import csv
import os
import errno

class CsvRecorder:
    def __init__(self, file_name):
        self.file_name = file_name
        self.info_file_name = file_name + ".properties"

    def prepare(self):
        path = os.path.dirname(self.file_name)
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def clear(self):
        with open(self.file_name, "wb") as f:
            f.close()
        with open(self.info_file_name, "wb") as f:
            f.close()

    def info(self, description):
        with open(self.info_file_name, "ab") as f:
            f.write(description)
            f.close()

    def record(self, sensorData, motorSpeeds):
        current_time = sensorData['current_time']
        distance_sensor_values = sensorData['distance_sensor_values']
        coordinates = sensorData['coordinates']
        camera = sensorData['camera']
        row = [current_time] + distance_sensor_values + coordinates + motorSpeeds + camera
        with open(self.file_name, "ab") as f:
            writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
            f.close()
