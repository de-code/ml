import csv
from scipy.io.matlab.mio import loadmat

try:
    dictFile = loadmat("/data_linux/public/downloads/_development_/machine-learning/eric_robotsensors.mat", struct_as_record=True)
except:
    print '''The dataset for this task was not found. Please download it from http://organic.elis.ugent.be/oger 
    and put it in ../datasets/''' 
    exit()

# the matlab file contains:
# 'data_info' : holds xy position, location number, etc.
# 'sensors' : the sensor information at each time step
# 'sensors_resampled' : a downsampling of the sensor data with x50 less timesteps

# these have time along the x axis
sensorData = np.array(dictFile.get('sensors_resampled')) 

with open("test2.csv", "ab") as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Spam'] * 5 + ['Baked Beans'])
    writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
    #f.write("appended text")
    f.close()

#with open("test.csv", "rb") as f:
#    reader = csv.reader(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#    for row in reader:
#        print ', '.join(row)
#    f.close()

