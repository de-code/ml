
import data_loader
from analyzer import Analyzer
from place_cell_reliability import get_activation_mean_locations, average_cost
from config import config

class ParametersEvolver:
    def __init__(self, config):
        self.config = config
        
    def load_data(self):
        data = data_loader.load_data(config)
        sm = data['sensor.matrix']
        self.coordinate_matrix = data['coordinate.matrix']
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
        self.training_data = trainingData
        self.test_data = testData
        self.input_dimensions = len(sm[0])

    def calculate_cost(self):
        analyzer = Analyzer(config, self.input_dimensions)
        analyzer.train(self.training_data)
        #training_features = analyzer.execute(self.training_data)
        test_features = analyzer.execute(self.test_data)
        activation_locations = get_activation_mean_locations(self.coordinate_matrix, test_features)
        cost = average_cost(self.coordinate_matrix, test_features, activation_locations)
        return cost

    def evolve(self):
        cost = self.calculate_cost()
        print "cost: ", cost

if __name__ == '__main__':
    evolver = ParametersEvolver(config)
    evolver.load_data()
    evolver.evolve()
    