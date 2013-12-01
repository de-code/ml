from __future__ import print_function
import numpy as np
from numpy import linalg as la

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

ACTIVATION_THRESHOLD = 4.5
NO_PREDICTION_PENALTY_COST = 2

def preprocess_activations(sigmoid_gradient, things):
    #return 1 /(1+np.exp(-sigmoid_gradient*things))
    return things


def get_activation_mean_locations(coords, place_cell_activations):
    
    n = place_cell_activations.shape[1]
    preprocessed_activations = preprocess_activations(0.05, place_cell_activations)    
    mean_activation_locations = np.zeros((n,2))
    
    for i in range(n):
        mean_activation_locations[i] = np.mean(coords[preprocessed_activations[:,i] > ACTIVATION_THRESHOLD, :], axis=0)

    return mean_activation_locations 
    
def average_cost(coords, place_cell_activations, activation_locations):
     
    cost = 0
    m = place_cell_activations.shape[0]    
    preprocessed_activations = preprocess_activations(0.1, place_cell_activations)
    predicted_locations = np.zeros((m,2))   
    
    prediction_count = 0
    for t in range(m):
        locations = activation_locations[preprocessed_activations[t,:] > ACTIVATION_THRESHOLD,:]
        if len(locations) > 0:
            predicted_locations[t,:] = np.mean(locations, axis=0)
            cost = cost + la.norm(coords[t,:] - predicted_locations[t,:])
            prediction_count = prediction_count + 1
        else:
            cost = cost + NO_PREDICTION_PENALTY_COST
          
    print('Prediction count: ', prediction_count, ' of ', m)
    return cost/m

def calculate_fitness(coords, place_cell_activations, activation_locations):
    cost = average_cost(coords, place_cell_activations, activation_locations)
    return 1/cost if cost > 0 else 0

def plot_activations(title, trajectory, features, single_plot):
    ''' Example plot:
     plot_activations('Place cells: ', self.coordinate_matrix, test_features, False) 
     '''

    n = features.shape[1]
    m = features.shape[0]
      
    if single_plot:  
        plots_per_fig = 1
        place_cells_per_plot = n
    else:
        plots_per_fig = 9
        place_cells_per_plot = 4
    
    fig_dim = np.sqrt(plots_per_fig)
        
    colormap = plt.cm.Set1
    colours = [colormap(i) for i in np.linspace(0, 0.9, place_cells_per_plot)]
    light_grey = '#DDDDDD'
    almost_black = '#262626'
        
    fig_index = 0
    for i in range(n):
        if (i % (plots_per_fig*place_cells_per_plot)) == 0:
            print('fig ' + str(i % plots_per_fig*place_cells_per_plot))
            fig = plt.figure()
            fig.patch.set_facecolor('black')
            fig.text

        if (i % place_cells_per_plot) == 0:
            print('subplot ' + str((i // place_cells_per_plot) % plots_per_fig))
            ax = fig.add_subplot(fig_dim, fig_dim, \
                                 1+(i // place_cells_per_plot) % plots_per_fig,\
                                 axisbg=almost_black)        
            plot_text = title + str(i+1) + '-' + str(i+place_cells_per_plot)
            ax.text(0.5, 1, plot_text, verticalalignment='top', 
                    horizontalalignment='center', transform=ax.transAxes, 
                    color='white', fontsize=8)
            plt.setp( ax.get_xticklabels(), visible=False)
            plt.setp( ax.get_yticklabels(), visible=False)
            ax.scatter(trajectory[1:m:17,0], trajectory[1:m:17,1], \
                       edgecolor=light_grey, \
                       facecolor=light_grey, \
                       s=0.01, alpha=0.5)
            
        activations = trajectory[features[:,i] > ACTIVATION_THRESHOLD, :]    
        ax.scatter(activations[:,0], activations[:,1], \
                   edgecolor=colours[i%place_cells_per_plot], \
                   facecolor=colours[i%place_cells_per_plot], \
                   s=30,
                   alpha=0.2)

    plt.show()
    print('Press enter to continue.')
    raw_input()
    
    return            
            
