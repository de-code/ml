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
import matplotlib.pyplot as plt
import plotter
import numpy as np
import time
import data_loader
from analyzer import Analyzer
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
    
    inputDims = len(sm[0])
    
    print "inputDims=", inputDims, ", rows=", len(sm)
    
    analyzer = Analyzer(config, inputDims)
        
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

    analyzer.train(trainingData)
     
    trainingFeatures = analyzer.execute(trainingData)
    testFeatures = analyzer.execute(testData)
    #testFeatures = trainingFeatures
    analyzer.reset_states(True)
    testFeatures2 = []
    for timeIndex in range(0, len(testData), 1):
        testFeatures2.append(analyzer.execute([testData[timeIndex]])[0])
        analyzer.reset_states(False)
    #testFeatures2 = analyzer.execute(testData)
    testFeaturesCombined = np.append(testFeatures, testFeatures2, 1)
    print "testFeaturesCombined: " + str(len(testFeaturesCombined.T)) + " x " + str(len(testFeaturesCombined.T[0]))
    #plotter.plot_features_graphs("dummy", coordm, testFeaturesCombined, 8, sm, 0)
    
    title = analyzer.description + ", data: " + str(len(sm)) + ", source: " + sourceDescription

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
        for i in range(analyzer.output_count):
            activationCounters.append(0)
        for timeIndex in range(0, len(testData), 1):
            print "timeIndex=" + str(timeIndex)
            icaOutput = analyzer.execute([testData[timeIndex]])
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
    





