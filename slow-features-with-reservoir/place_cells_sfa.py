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
import plotter
import time
import data_loader
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
    data = data_loader.load_data(config)
    sm = data['sensor.matrix']
    coordm = data['coordinate.matrix']
    sourceDescription = data['description']

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
    elif (plotterConfig == 'coverage'):
        plotter.plot_coverage(title, coordm, testFeatures)
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
    





