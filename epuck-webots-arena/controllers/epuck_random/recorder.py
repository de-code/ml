import csv

class CsvRecorder:
    def __init__(self, file_name):
        self.file_name = file_name
        
    def clear(self):
        with open(self.file_name, "wb") as f:
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
