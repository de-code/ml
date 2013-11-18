import os,re,time,random,math,pprint
import numpy as np

def get_data(filename="data.dat",as_list=False):
    data = np.loadtxt(filename,delimiter=",")
    if as_list:
        list(data)
    return data

def remove_incomplete_data(data):
    result = data
    minLength = len(data[0]);
    maxLength = minLength;
    for row in sm:
        minLength = min(minLength, len(row))
        maxLength = max(maxLength, len(row))
    if (minLength != maxLength):
        print "Warning: min-length: ", minLength, ", max-length: ", maxLength
        previousLenght = len(data)
        result = filter(lambda x: len(x) == maxLength, data)
        #sm = [x in x in sm where len(x) == maxLength]
        print "Discarded entries: ", (previousLenght - len(sm)), " remaining: ", len(result)
    return data

def normalise_data_zero_means_std_deviation(data):
    return (data - np.mean(data, axis=0)) / np.std(data, axis=0)

def normalise_data_zero_to_one(data):
    t = data - np.min(data, axis=0)
    return t / np.max(t, axis=0)

def convert_to_place_data(data,indexes):
    new_data = []
    for i in indexes:
        new_data.append(data[0:1000,i].T)
    return new_data

class DataPool(object):
    """
    Our pool of data
    """
    def __init__(self, data):
        super(DataPool, self).__init__()
        self.data = data
        self.time_step = 100
        self.window = 100
        self.time=None
        self.update()
    def step(self,t=None):
        """
        Increases the timestep or sets
        it to the passed value
        """
        if t:
            self.time_step = t
        else:
            self.time_step += 1
    def update(self):
        """
        Updates all values from the current timestep
        """
        self.s_t=self.data[self.time_step][1:9]
        self.s_tminus1=self.data[self.time_step-1][1:9]
        self.s_tminus2=self.data[self.time_step-2][1:9]
        self.m_t=self.data[self.time_step][9:11]
        self.m_tminus1=self.data[self.time_step-1][9:11]
        self.m_tminus2=self.data[self.time_step-2][9:11]
        self.time=self.data[self.time_step][0]
    def get_curr_data_as_vec(self):
        """
        Returns data from s and m t, t-1 and t-2 as one vector
        """
        data = np.array([])
        t = 0
        while t < self.window:
            data = np.hstack((data,self.data[self.time_step-t][1:11]))
            t += 1
        return data

    def print_curr(self):
        print "simulation time:",self.time
        print "s_t:",self.s_t
        print "s_tminus1:",self.s_tminus1
        print "s_tminus12",self.s_tminus2
        print "m_t:",self.m_t
        print "m_tminus1:",self.m_tminus1
        print "m_tminus2",self.m_tminus2

def normalise_features(X):
    """
    Normalise our features by subtracting the mean
    and dividing by the standard deviation
    """
    columns = len(X[0])
    rows = len(X)
    N = copy.deepcopy(X)
    mean = []
    std = []
    for column in range(0,columns):
        x_column = get_columns_as_list(X,column)
        mean.append(np.mean(x_column))
        std.append(np.std(x_column))
        for i,value in enumerate(x_column):
            N[i][column]=(value-mean[column])/std[column]
    return [N,mean,std]

if __name__ == '__main__':
    data = get_data()
    pool = DataPool(data)
    pool.print_curr()
