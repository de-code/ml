import Oger
import mdp.nodes
import numpy as np

class Analyzer:
    def __init__(self, config, inputDims):
        resDims = config['analyse.reservoire.dim'] #dimensions in the reserv
        sfaNum = config['analyse.sfa.num'] #number of slow features to extract
        icaNum = config['analyse.ica.num'] # number of independent components to extract
        leakRate = config['analyse.leak.rate'] # leak rate of the reservoir
        specRadius = config['analyse.spectral.radius'] # spectral radius
        
        # make sure that reservoir size is matching
        if resDims < sfaNum:
            resDims = sfaNum
            print "Adjusting reservoir size to feature count!!!"
        
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
        
        self.resNode = resNode
        self.flow = flow
        self.description = "Res: " + str(resDims) + ", SFA: " + str(sfaNum) + ", ICA: " + str(icaNum) + ", leak: " + str(leakRate) +\
            ", specR: " + str(specRadius)
        self.output_count = icaNum

    def reset_states(self, reset_states):
        self.resNode.reset_states = reset_states
        
    def train(self, data):
        self.flow.train(np.transpose(data).T)
        
    def execute(self, data):
        return self.flow.execute(np.transpose(data).T)

