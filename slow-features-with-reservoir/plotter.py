import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def plot_features_graphs(title, trajectory, features, featureCount, input, inputCount):
    fig = plt.figure()
    plt.title(title)
    plotIndex = 1
    totalPlotNum = featureCount + 2 + inputCount
    #plt.ion()
    plt.subplot(totalPlotNum, 1, plotIndex)
    plt.plot(trajectory[:, 0])
    plotIndex = plotIndex + 1
    plt.subplot(totalPlotNum, 1, plotIndex)
    plt.plot(trajectory[:, 1])
    for i in range(inputCount):
        plotIndex = plotIndex + 1
        plt.subplot(totalPlotNum, 1, plotIndex)
        plt.plot(input[:, i])
        plt.ylim([-4,4])
    # plot the independent components
    for i in range(featureCount):
        plotIndex = plotIndex + 1
        plt.subplot(totalPlotNum, 1, plotIndex)
        plt.plot(features[:, i])
        plt.ylim([-4,4])
    plt.show()

def plot_features3d(title, trajectory, features, featureCount):
    fig = plt.figure()
    plt.title(title)
    ax = Axes3D(fig)
    ax.plot(trajectory[:,0], trajectory[:,1], 0, label='trajectory')
    #for i in range(features.shape[1]):
    for i in range(featureCount):
        ax.plot(trajectory[:,0], trajectory[:,1], features[:,i], label='ica feature '+str(i))
    ax.legend()
    #ax.set_xlim([0,10])
    #ax.set_ylim([0,10])
    #ax.set_zlim([0,10])
    plt.show()

def plot_feature_comparison(title, trajectory, features):
    plotCount = features.shape[1]
    pointCount = features.shape[0]
    fig = plt.figure()
    plt.title(title)
    #plt.ion()
    #plt.show()
    max = np.amax(features)
    min = np.amin(features)
    print "min=" + str(min) + ", max=" + str(max)
    for i in range(plotCount):
        #ax = fig.add_subplot(plotCount/10,10,1+i)
        plt.subplot(plotCount/2, 2, 1+i)
        f = features[:,i]
        
        for k in range(pointCount):
            color = ''
            if(f[k] > max * 0.6):
                color = 'r'
            elif(f[k] > max * 0.3):
                color = 'y'
            elif(f[k] < min * 0.3):
                color = 'b'
            elif(f[k] < min * 0.6):
                color = 'g'
                
            if (color != ''):
                #ax.plot(trajectory[k,0], trajectory[k,1], color+'.', markersize=20)
                plt.plot(trajectory[k,0], trajectory[k,1], color+'.', markersize=20)
                #plt.draw()
        #ax.plot(trajectory[:,0], trajectory[:,1], 'k')
        plt.plot(trajectory[:,0], trajectory[:,1], 'k')
    plt.show()
    #raw_input()
    return

def create_real_time_plot():
    plt.ion()
    plt.figure()
    plt.show()

def update_real_time_plot(trajectory, currentPos, activation):
    plt.clf()
    plt.plot(trajectory[:,0], trajectory[:,1], 'k')
    color = 'r'
    if(activation != ''):
        color = 'g'
    plt.plot(currentPos[0], currentPos[1], color+'.', markersize=20)
    plt.text(currentPos[0], currentPos[1], activation)
    plt.draw()
