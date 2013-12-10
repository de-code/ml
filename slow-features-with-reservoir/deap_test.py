#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

import random

from deap import base
from deap import creator
from deap import tools
from scoop import futures
import copy
from parameters_evolver import *
from analyzer import Analyzer
from config import config
import time,math

class AnalyzerHelper:
    def __init__(self, config):
        self.config = config
        self.dummy = False
        
    def load_data(self):
        if (self.dummy):
            return
        data = data_loader.load_data(self.config)
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

    def calculate_cost_using_analyzer(self, parameters, parameters_descriptors):
        config = {}
        for i in range(len(parameters)):
            config[parameters_descriptors[i].name] = parameters[i]
        config['analyse.ica.num'] = config['analyse.sfa.num'] 
        print "calculating cost for: ", config
        start = time.time()
        analyzer = Analyzer(config, self.input_dimensions)
        analyzer.train(self.training_data)
        #training_features = analyzer.execute(self.training_data)
        test_features = analyzer.execute(self.test_data)
        activation_locations = get_activation_mean_locations(self.coordinate_matrix, test_features)
        cost = average_cost(self.coordinate_matrix, test_features, activation_locations)
        end = time.time()
        print "calculating cost done, took ", (end - start), ", config: ", config
        return cost

parameters_descriptors = [
    IntParameterDescriptor('analyse.reservoire.dim', 300, 400, 5),
    IntParameterDescriptor('analyse.sfa.num', 1, 400, 5),
#            IntParameterDescriptor('analyse.ica.num', 1, 400, 5),
    FloatParameterDescriptor('analyse.leak.rate', 0, 1, 0.1),
    FloatParameterDescriptor('analyse.spectral.radius', 0, 1, 0.1)]

analyzerHelper = AnalyzerHelper(config)
analyzerHelper.load_data()

def random_parameters():
    parameters = []
    for i in range(len(parameters_descriptors)):
        parameters.append(parameters_descriptors[i].random_value())
    return parameters

def mutate_parameters1(parameters):
    mutation_rate = 0.5
    parameters = copy.copy(parameters)
    for i in range(len(parameters)):
        r = random.random()
        if (r <= mutation_rate):
            parameters[i] = parameters_descriptors[i].mutate_value(parameters[i])
    return parameters

def mutate_parameters(parameters):
    return mutate_parameters1(parameters[0])

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("attr", random_parameters)
# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr, 1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("map", futures.map)

def evalOneMax1(individual):
#    a = [math.sqrt(random.random()) for k in range(10000)]
    return sum(individual[0]),

def evalOneMax(individual):
    return analyzerHelper.calculate_cost_using_analyzer(individual[0], parameters_descriptors),

# Operator registering
toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoints)
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("mutate", mutate_parameters)
toolbox.register("select", tools.selTournament, tournsize=2)

def main():
    start = time.time()
    random.seed(64)
    
    pop = toolbox.population(n=5)
    CXPB, MUTPB, NGEN = 0.5, 0.5, 50
    
    print("Start of evolution")
    
    # Evaluate the entire population
    fitnesses = list(toolbox.map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(pop))
    
    # Begin the evolution
    for g in range(NGEN):
        print("-- Generation %i --" % g)
        
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
#         Apply crossover and mutation on the offspring
#         for child1, child2 in zip(offspring[::2], offspring[1::2]):
#             if random.random() < CXPB:
#                 toolbox.mate(child1, child2)
#                 del child1.fitness.values
#                 del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
    
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        print("  Evaluated %i individuals" % len(invalid_ind))
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        
        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)
    
    print("-- End of (successful) evolution --")
    
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    print "time:",time.time()-start
    return best_ind

if __name__ == "__main__":
    b = main()