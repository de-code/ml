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
from scipy.io.matlab.mio import loadmat
from scipy.signal.signaltools import resample
import Oger
import matplotlib.pyplot as plt
import mdp.nodes
import numpy as np
import data_utilities
import plotter
import os
import time
from config import config

def getPlaceCellActivation(currentFeatures, minSignal, maxSignal):
    #maxSignal = np.amax(trainingFeatures)
    #minSignal = np.amin(trainingFeatures)
    
    activation = []
    for i in range(len(currentFeatures)):
        f = currentFeatures[i]
        if (f > maxSignal * 0.3 or f < minSignal * 0.3):
            activation.append(i)
            print "activation " + str(i) + ", f=" + str(f) + ", minSignal=" + str(minSignal) + ", maxSignal=" + str(maxSignal)
    return activation


if __name__ == '__main__':
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
        sd = np.array(dictFile.get('sensors'))
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

    # these have time along the x axis
    #sensorData = np.array(sm)
    #sensorData = np.transpose(sm[1:1000, :]);
        
    resDims = config['analyse.reservoire.dim'] #dimensions in the reserv
    sfaNum = config['analyse.sfa.num'] #number of slow features to extract
    icaNum = config['analyse.ica.num'] # number of independent components to extract
    leakRate = config['analyse.leak.rate'] # leak rate of the reservoir
    specRadius = config['analyse.spectral.radius'] # spectral radius

    inputDims = len(sm[0])
    
    print "inputDims=", inputDims, ", rows=", len(sm)
    
    # define the reservoir and pass the spectrogram through it
    resNode = Oger.nodes.LeakyReservoirNode(input_dim=inputDims,
                  output_dim=resDims, spectral_radius=specRadius, leak_rate=leakRate, reset_states=True)

    # Creation of the input weight matrix according to paper
    # -0.2,0.2 and 0 with probabilities of 0.15,0.15 and 0.7 respectively 
    w_in = np.zeros((resDims, inputDims))
    for i in range(resDims):
        for j in range(inputDims):
            ran = np.random.rand()
            if ran < 0.15:
                w_in[i, j] = -0.2
            elif ran < 0.3:
                w_in[i, j] = 0.2
            else:
                w_in[i, j] = 0 
                
    # set the input weight matrix for reservoir                
    resNode.w_in = w_in
    resNode.initialize()

    # define the sfa node
    sfaNode = mdp.nodes.SFANode(output_dim=sfaNum)
    
    # define the ica node
    icaNode = mdp.nodes.FastICANode(input_dim=sfaNum)
    # icaNode.set_output_dim(icaNum)

    #define the flow
    flow = mdp.Flow(resNode + sfaNode + icaNode)
    #train the flow

    plotterConfig = config['plotter']

    if (plotterConfig == 'replay'):
        splitData = True
        if (splitData):
            trainingSize = len(sm) / 2
            testSize = len(sm) - trainingSize
            testDataOffset = trainingSize
            trainingData = sm[0:trainingSize]
            testData = sm[testDataOffset:(testSize + trainingSize)]
        else:
            testDataOffset = 0
            trainingData = sm
            testData = sm
    else:
        testDataOffset = 0
        trainingData = sm
        testData = sm
        
    flow.train(np.transpose(trainingData).T)
    # 
    trainingFeatures = flow.execute(np.transpose(trainingData).T)
    testFeatures = flow.execute(np.transpose(testData).T)
    #testFeatures = trainingFeatures
    resNode.reset_states = True
    testFeatures2 = []
    for timeIndex in range(0, len(testData), 1):
        testFeatures2.append(flow.execute(np.transpose([testData[timeIndex]]).T)[0])
        resNode.reset_states = False
    #testFeatures2 = flow.execute(np.transpose(testData).T)
    testFeaturesCombined = np.append(testFeatures, testFeatures2, 1)
    print "testFeaturesCombined: " + str(len(testFeaturesCombined.T)) + " x " + str(len(testFeaturesCombined.T[0]))
    #plotter.plot_features_graphs("dummy", coordm, testFeaturesCombined, 8, sm, 0)
    
    title = "Res: " + str(resDims) + ", SFA: " + str(sfaNum) + ", ICA: " + str(icaNum) + ", leak: " + str(leakRate) +\
        ", specR: " + str(specRadius) + ", data: " + str(len(sm)) + ", source: " + sourceDescription

#     plt.ion()
#     print "graph"
#     plotter.plot_features_graphs(title, coordm, trainingFeatures, 10, sm, 0)
#     plotter.plot_features_graphs(title, coordm[testDataOffset:len(coordm)], testData, 10, sm, 0)
    #print "comparison"
    #plotter.plot_feature_comparison(title, coordm, icaOutput)
    
    if (plotterConfig == '3d'):
        #for complete feature set
        #plotter.plot_features(coordm, icaOutput, icaOutput.shape[1])

        #for the first 3 features
        plotter.plot_features3d(title, coordm, testFeatures, 10)
    elif (plotterConfig == 'feature_comparison'):
        #for complete feature set
        #plotter.plot_features(coordm, icaOutput, icaOutput.shape[1])

        #for the first 3 features
        plotter.plot_feature_comparison(title, coordm, testFeatures)
    elif (plotterConfig == 'replay'):
        plt.ion()
        print "graph"
        #plotter.plot_features_graphs(title, coordm, trainingFeatures, 10, sm, 0)
        #plotter.plot_features_graphs(title, coordm[testDataOffset:len(coordm)], testData, 10, sm, 0)
        #print "comparison"
        plotter.plot_feature_comparison(title, coordm, trainingFeatures)
        print "replay"
        plotter.create_real_time_plot()
        #trainingFeatures = icaOutput
        maxSignal = np.amax(trainingFeatures)
        minSignal = np.amin(trainingFeatures)
        activationLifeSpan = 100
        activationCounters = []
        updatePlotInterval = 10
        print "feature count=" + str(len(testFeatures))
        for i in range(icaNum):
            activationCounters.append(0)
        for timeIndex in range(0, len(testData), 1):
            print "timeIndex=" + str(timeIndex)
            icaOutput = flow.execute(np.transpose([testData[timeIndex]]).T)
            #icaOutput = [testFeatures[timeIndex]]
#             if ((icaOutput - testFeatures[timeIndex]).any()):
#                 print "features not the same, timeIndex=" + str(timeIndex) +\
#                     ", expected: " + str(testFeatures[timeIndex]) + ", actual: " + str(icaOutput)
            activation = getPlaceCellActivation(icaOutput[0], minSignal, maxSignal)
            for i in range(len(activationCounters)):
                activationCounters[i] = max(0, activationCounters[i] - 1)
            for i in range(len(activation)):
                activationCounters[activation[i]] = activationLifeSpan
            if ((timeIndex % updatePlotInterval) == 0):
                previousActivation = []
                for i in range(len(activationCounters)):
                    if (activationCounters[i] > 0):
                        previousActivation.append(i);
                plotter.update_real_time_plot(coordm,
                    coordm[testDataOffset + timeIndex], str(activation) + "(" + str(previousActivation) + ")")
                time.sleep(0.1)
    else:
        #resample the ica layer output back to 50 times the length 
        # icaOutputLong = resample(icaOutput, location.shape[0])
        plotter.plot_features_graphs(title, coordm, testFeatures, 3, sm, 0)
    





