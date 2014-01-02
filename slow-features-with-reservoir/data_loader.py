'''
The following implements an example of the experiments run in: "Unsupervised Learning 
in Reservoir Computing: Modeling Hippocampal Place Cells for Small Mobile Robots" by
E. Antonelo and B. Schrauwen

It takes robot sensor data, runs it through a hierarchy of a reservoir, then slow 
feature analysis, then independent component analysis. Finally 20 of the outputs of
the ICA layer are plotted along with the numbered robot location (see paper).

It can be seen that certain outputs repeatedly produce a spike of activity at precise locations.

Location of the robot is the topmost plot.

'''
import data_utilities
import os
from scipy.io import loadmat
import numpy as np

def load_data(config):
    # take matlab file in as a dictionary
    # try:
    #     dictFile = loadmat("eric_robotsensors.mat", struct_as_record=True)
    # except:
    #     print '''The dataset for this task was not found. Please download it from http://organic.elis.ugent.be/oger 
    #     and put it in ../datasets/''' 
    #     exit()

    dataFile = config['data.file']
    fromIndex = config['data.from'];
    maxRows = config['data.max'];
    sourceDescription = os.path.basename(dataFile)
    if (dataFile.endswith(".mat")):    
        # the matlab file contains:
        # 'data_info' : holds xy position, location number, etc.
        # 'sensors' : the sensor information at each time step
        # 'sensors_resampled' : a downsampling of the sensor data with x50 less timesteps
        #data = du.convert_to_place_data(du.get_data(),[1,2,3,4,5,6,7,8])
        # take matlab file in as a dictionary
        try:
            dictFile = loadmat(dataFile, struct_as_record=True)
        except:
            print 'Data file not found:', dataFile 
            exit()
        # these have time along the x axis
        sd = np.array(dictFile.get('sensors_resampled'))
        sm = np.transpose(sd) 
        dataInfo = np.array(dictFile.get('data_info'))
        # 5th index contains the location number at each timestep
        coordm = np.transpose([dataInfo[1, :], dataInfo[2, :]])
        #pos = dataInfo[1:3, :]
    else:
        data = data_utilities.get_data(dataFile)
        dataColumns = len(data[0])
        print "Data columns: ", dataColumns
        distanceSensorIndex = 0
        timeStep = 200
        if (dataColumns >= 38):
            # time will now be in column 0
            distanceSensorIndex = 1
            timeStepIndex = 0
            if (fromIndex + 1 < len(data)):
                timeStep = data[fromIndex + 1][timeStepIndex] - data[fromIndex][timeStepIndex]
        distanceSensorIndices = range(distanceSensorIndex, 8)
        coordinatesIndices = range(distanceSensorIndex + 8, distanceSensorIndex + 10)
        motorIndices = range(distanceSensorIndex + 10, distanceSensorIndex + 12)
        cameraIndices = range(distanceSensorIndex + 12, dataColumns)
        selectedIndices = distanceSensorIndices + cameraIndices
        selectedIndicesDescription = "dist + camera"
        sm = data[:, selectedIndices]
        sm = data_utilities.normalise_data_zero_to_one(sm)
        coordm = data[:, coordinatesIndices]
        sourceDescription = sourceDescription + " (" + selectedIndicesDescription + ", step " + str(timeStep) + ")"
    
    dataLength = len(sm)
    if (fromIndex > dataLength):
        print 'Invalid from index, fromIndex:', fromIndex, ", dataLength: ", dataLength 
        exit()
    endIndex = min(dataLength, fromIndex + maxRows)
    sm = sm[fromIndex:endIndex, :]
    coordm = coordm[fromIndex:endIndex, :]
    return {
        'sensor.matrix': sm,
        'coordinate.matrix': coordm,
        'description': sourceDescription}
