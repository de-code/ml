
def get_place_cell_activation(current_features, min_signal, max_signal):   
    activation = []
    for i in range(len(current_features)):
        f = current_features[i]
        if (f > max_signal * 0.3 or f < min_signal * 0.3):
            activation.append(i)
            #print "activation " + str(i) + ", f=" + str(f) + ", min_signal=" + str(min_signal) + ", maxSignal=" + str(max_signal)
    return activation
