import data_utilities
from config import config

data = data_utilities.get_data(config['data.file'])
sm = data_utilities.normalise_data(data[:,0:8])
coordm = data[:,8:10]

print "Count: sm=", len(sm), "x", len(sm[0]), ", coordm=", len(coordm), "x", len(coordm[0])
