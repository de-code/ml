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
                plt.plot(trajectory[k,0], trajectory[k,1], color+'.', markersize=20)
                #plt.draw()
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
    
def plot_coverage(title, trajectory, features):
    featureCount = features.shape[1]
    pointCount = features.shape[0]
    fig = plt.figure()
    plt.title(title)
    #plt.ion()
    #plt.show()
    max = np.amax(features)
    min = np.amin(features)
    
    plt.plot(trajectory[:,0], trajectory[:,1], 'k')
    
    print "comparison max: " + str(max) + ", min: " + str(min)
    for i in range(featureCount):
        #plt.clf()
        f = features[:,i]
        
        maxIca = 0
        maxX = 0
        maxY = 0
        
        for k in range(pointCount):
            if(f[k] > 4.5):
                if f[k] > maxIca:
                    maxIca = f[k]
                    maxX = trajectory[k,0]
                    maxY = trajectory[k,1]
                #plt.plot(trajectory[k,0], trajectory[k,1], 'y.', markersize=20)
        
        if(maxIca > 0):
            plt.plot(maxX, maxY, 'r.', markersize=20)
            strMax = "%10.2f" % maxIca
            #plt.text(maxX, maxY, strMax, color='b')
                                       
        #ax.plot(trajectory[:,0], trajectory[:,1], 'k')
        
        
        #plt.savefig('/home/ronin/Documents/Hackademia 2013/plots/ica'+str(i)+'.png')
    
    plt.setp( plt.gca().xaxis.get_ticklabels(), visible=False)
    plt.setp( plt.gca().yaxis.get_ticklabels(), visible=False)
    plt.show()
    #raw_input()
    return

def plot_cell_activation(title, trajectory, features):
    featureCount = features.shape[1]
    pointCount = features.shape[0]
    plt.ion()
    plt.figure()
    plt.show()
    plt.title(title)
    max = np.amax(features)
    min = np.amin(features)
    
    activations = []
    locations = []
    
    for t in range(0, pointCount, 1):
        
        plt.clf()
    
        plt.plot(trajectory[:,0], trajectory[:,1], 'k')
        
        plt.plot(trajectory[t,0], trajectory[t,1], 'k.', markersize=20)
               
        activation = []
        for j in range(featureCount):
            f = features[:,j]
            if(f[t] > 4.5):
                activation.append(j)
                
        if(len(activation) > 0):
        
            new = True
            for k in range(len(activations)):
                if(activations[k] == activation 
                   and euclidean_distance(trajectory[locations[k],:], trajectory[t,:]) < 50):
                    new = False
            
            if(new):
                activations.append(activation)
                locations.append(t)                
                
        for l in range(len(locations)):
            plt.plot(trajectory[locations[l],0], trajectory[locations[l],1], 'r.', markersize=20)
            plt.text(trajectory[locations[l],0], trajectory[locations[l],1], activations[l])
        
        if t % 25 == 0:      
            plt.draw()
            
    #plt.draw()
        
    return
        
def euclidean_distance(x, y):
    return np.sqrt(np.sum((x-y)**2))

def plot_reliability(title, trajectory, features):
    featureCount = features.shape[1]
    pointCount = features.shape[0]
    #plt.ion()
    plt.figure()
    #plt.show()
    plt.title(title)
    locations = []
    activations = []
    hits = []
    misses = []
    inRange = []
    counted = []
    for i in range(featureCount):
        f = features[:,i]
              
        maxIca = 0
        for k in range(pointCount):
            if(f[k] > 4.5):
                if f[k] > maxIca:
                    maxIca = f[k]
                    locations.append(k)
                    activations.append(i)
                    hits.append(0)
                    misses.append(0)
                    inRange.append(False)
                    counted.append(False)
    
    plt.setp( plt.gca().xaxis.get_ticklabels(), visible=False)
    plt.setp( plt.gca().yaxis.get_ticklabels(), visible=False)
    
    for t in range(pointCount):
        
        if (t%10000 == 0):
            print "t="+str(t)
        
        #plt.clf()
    
        #plt.plot(trajectory[:,0], trajectory[:,1], 'k')
        
        for l in range(len(locations)):
            if (euclidean_distance(trajectory[locations[l],:], trajectory[t,:]) < 50):
                if(inRange[l] == False):
                    inRange[l] = True
                
                f = features[:,activations[l]]
                if(f[locations[l]] > 4.5):
                    if(counted[l] == False):
                        counted[l] = True
                        hits[l] = hits[l] + 1
                        
                #plt.plot(trajectory[locations[l],0], trajectory[locations[l],1], 'g.', markersize=20)
            else:
                if(inRange[l] == True):
                    inRange[l] = False
                    if(counted[l] == False):
                        misses[l] = misses[l] + 1
                    else:
                        counted[l] = False
                        
                #plt.plot(trajectory[locations[l],0], trajectory[locations[l],1], 'r.', markersize=20)
                
            #plt.text(trajectory[locations[l],0], trajectory[locations[l],1], str(hits[l])+"/"+str(misses[l]))
            
        #plt.plot(trajectory[t,0], trajectory[t,1], 'k.', markersize=20)
        
        #if t % 100 == 0:      
        #    plt.draw()
    
    plt.plot(trajectory[:,0], trajectory[:,1], 'k')
    for l in range(len(locations)):
        plt.plot(trajectory[locations[l],0], trajectory[locations[l],1], 'r.', markersize=20)
        plt.text(trajectory[locations[l],0], trajectory[locations[l],1], str(hits[l])+"/"+str(misses[l]))
        
    
    plt.show()
    raw_input()
    return