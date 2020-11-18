import pickle

models_name = [
    'svc',
    'knn',
    'log',
    'random_forest',
    'gaussian',
    'perceptron',
    'sgd',
    'linear_svc',
    'decision_tree'
]

models = {}

# Load all models
for m in models_name:
    with open('model/{}.pkl'.format(m), 'rb') as f:
        models[m] = pickle.load(f)
