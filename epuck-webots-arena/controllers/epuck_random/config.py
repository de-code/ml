config = {
    'data.record': True,
    'data.file': '{home}/../../datasets/sensor-data-{datetime}-{name}-{mode}.csv',
    'data.append': False,
    'time.step.size': 100,
    'time.step.count': 200000,
    'randomness': 0.0,
    'mode': 'path',
    'targets': [[-0.9, -0.9], [0.9, -0.9], [0.9, 0.9], [-0.9, 0.9]]}