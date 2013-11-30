from __future__ import print_function
import numpy as np
from numpy import linalg as la

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



