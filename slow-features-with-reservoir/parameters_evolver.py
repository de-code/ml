
import data_loader
from analyzer import Analyzer
from place_cell_reliability import get_activation_mean_locations, average_cost
import random
import copy
from config import config

class ParameterDescriptor(object):
    def __init__(self, name, min, max, mutation_distribution):
        super(ParameterDescriptor, self).__init__()
        self.name = name
        self.min = min
        self.max = max
        self.mutation_distribution = mutation_distribution
        
    def random_value(self):
        print "Not implemented"
    
    def mutate_value(self, value, mutation_rate):
        print "Not implemented"

class IntParameterDescriptor (ParameterDescriptor):
    def __init__(self, name, min, max, mutation_distribution):
        super(IntParameterDescriptor, self).__init__(name, min, max, mutation_distribution)
        
    def random_value(self):
        return random.randint(self.min, self.max)
    
    def mutate_value(self, value):
        return max(self.min, min(self.max, value + random.randint(-self.mutation_distribution, self.mutation_distribution)))

class FloatParameterDescriptor (ParameterDescriptor):
    def __init__(self, name, min, max, mutation_distribution):
        super(FloatParameterDescriptor, self).__init__(name, min, max, mutation_distribution)
        
    def random_value(self):
        return self.min + random.random() * (self.max - self.min)
    
    def mutate_value(self, value):
        return max(self.min, min(self.max, value + (random.random() * (self.mutation_distribution * 2) - self.mutation_distribution)))
    

class ParametersEvolver:
    def __init__(self, config):
        self.config = config
        self.population_count = 10
        self.parameters_descriptors = [
            IntParameterDescriptor('analyse.reservoire.dim', 300, 400, 5),
            IntParameterDescriptor('analyse.sfa.num', 1, 400, 5),
#            IntParameterDescriptor('analyse.ica.num', 1, 400, 5),
            FloatParameterDescriptor('analyse.leak.rate', 0, 1, 0.1),
            FloatParameterDescriptor('analyse.spectral.radius', 0, 1, 0.1)]
        self.parameters_count = len(self.parameters_descriptors)
        self.dummy = False
        parameters_matrix = []
        for i in range(self.population_count):
            parameters_matrix.append(self.random_parameters())
        self.parameters_matrix = parameters_matrix
        self.mutation_rate = 1
        
    def random_parameters(self):
        parameters = []
        for i in range(self.parameters_count):
            parameters.append(self.parameters_descriptors[i].random_value())
        return parameters
        
    def load_data(self):
        if (self.dummy):
            return
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

    def calculate_cost(self, parameters):
        if (self.dummy):
            return self.calculate_cost_dummy(parameters)
        else:
            return self.calculate_cost_using_analyzer(parameters)

    def calculate_cost_dummy(self, parameters):
        cost = 0
        for i in range(self.parameters_count):
            cost = cost + parameters[i]
        return cost

    def calculate_cost_using_analyzer(self, parameters):
        config = {}
        for i in range(self.parameters_count):
            config[self.parameters_descriptors[i].name] = parameters[i]
        config['analyse.ica.num'] = config['analyse.sfa.num'] 
        print "calculating cost for: ", config
        analyzer = Analyzer(config, self.input_dimensions)
        analyzer.train(self.training_data)
        #training_features = analyzer.execute(self.training_data)
        test_features = analyzer.execute(self.test_data)
        activation_locations = get_activation_mean_locations(self.coordinate_matrix, test_features)
        cost = average_cost(self.coordinate_matrix, test_features, activation_locations)
        return cost

    def get_parameters(self, individual_index):
        return self.parameters_matrix[individual_index]

    def set_parameters(self, individual_index, parameters):
        self.parameters_matrix[individual_index] = parameters

    def get_cost(self, individual_index):
        return self.calculate_cost(self.get_parameters(individual_index))

    def random_individual(self, exclude_index=-1):
        index = random.randint(0, self.population_count - 1)
        if (index == exclude_index):
            index = self.random_individual(exclude_index)
        return index

    def random_two_distinct(self):
        index1 = self.random_individual(-1)
        index2 = self.random_individual(index1)
        return index1, index2

    def compare_individuals_by_cost(self, index1, index2):
        index1, index2 = self.random_two_distinct()
        cost1 = self.get_cost(index1)
        cost2 = self.get_cost(index2)
        result = (cost2 - cost1)
        print "cost1: ", cost1, ", cost2: ", cost2, ", result: ", result
        return result
    
    def mutate_parameters(self, parameters, mutation_rate):
        parameters = copy.copy(parameters)
        for i in range(self.parameters_count):
            r = random.random()
            if (r <= mutation_rate):
                parameters[i] = self.parameters_descriptors[i].mutate_value(parameters[i])
        return parameters

    def evolve_next(self):
        index1, index2 = self.random_two_distinct()
        result = self.compare_individuals_by_cost(index1, index2)
        if (result < 0):
            winner_index = index1
            looser_index = index2
        else:
            winner_index = index2
            looser_index = index1
        parameters = self.get_parameters(winner_index)
        print "winning parameters (non-mutated): ", parameters
        print "loosing parameters (non-mutated): ", self.get_parameters(looser_index)
        parameters = self.mutate_parameters(parameters, self.mutation_rate)
        self.set_parameters(looser_index, parameters)
        print "winning parameters (mutated): ", parameters

    def evolve(self):
        for i in range(100000):
            self.evolve_next()

if __name__ == '__main__':
    evolver = ParametersEvolver(config)
    evolver.load_data()
    evolver.evolve()
    