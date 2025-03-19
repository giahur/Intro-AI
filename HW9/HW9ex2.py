import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# columns: sepal length, sepal width, petal length, petal width, species
irisData = pd.read_csv('irisdata.csv')
# 2nd and 3rd classes (versicolor and virginica)
data23 = irisData[irisData['species'].isin(['versicolor', 'virginica'])]

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# 0 for versicolor, 1 for virginica
def neuralNetworkOutput(x1, x2, w1, w2, b):
    return sigmoid(w1 * x1 + w2 * x2 + b)

# plot classes using petal width and length
def plotClasses():
    for species, group in data23.groupby('species'):
        plt.scatter(group['petal_length'], group['petal_width'], label=species)
    plt.title(f'Versicolor vs Virginica')
    plt.xlabel('Petal Length')
    plt.ylabel('Petal Width')
    plt.legend()
    plt.xlim(data23['petal_length'].min() - 0.5, data23['petal_length'].max() + 0.5)
    plt.ylim(data23['petal_width'].min() - 0.5, data23['petal_width'].max() + 0.5)

# weight parameters set by hand
def plotDecisionBoundary(w1, w2, b):
    x1 = data23['petal_length']
    # for given x1, find x2 where sigmoid = 0.5
    x2 = -(w1 * x1 + b) / w2
    plt.plot(x1, x2)

# calculates mean-squared error of iris data for neural network
# should take: data vectors, parameters defining neural network, pattern classes
def calculateMSE(dataVectors, params, patternClasses):
    x1 = dataVectors['petal_length']
    x2 = dataVectors['petal_width']
    w1, w2, b = params

    NNO = neuralNetworkOutput(x1, x2, w1, w2, b)
    mse = np.mean((NNO - patternClasses)**2)
    print("MSE: ", mse)

def computeGradient(x1, x2, w1, w2, w0, patternClasses):
    N = patternClasses.size
    NNO = neuralNetworkOutput(x1, x2, w1, w2, w0)
    current = (NNO - patternClasses) * NNO * (1 - NNO)
    gradw1 = (2/N) * np.sum(current * x1)
    gradw2 = (2/N) * np.sum(current * x2)
    gradw0 = (2/N) * np.sum(current)

    print("gradient:", gradw1,gradw2,gradw0)

    w1 = w1 - (10/N) * gradw1
    w2 = w2 - (10/N) * gradw2
    w0 = w0 - (10/N) * gradw0

    print("Updated weights: ", w1, w2, w0)
    return w1, w2, w0

# calculate MSE 2a
dataVectors = data23[['petal_length', 'petal_width']]
params = (0.87, 0.93, -5.7)
patternClasses = np.where(data23['species'] =='versicolor', 0, 1)
calculateMSE(dataVectors, params, patternClasses)

# plot boundary with small and large errors 2b
plt.figure()
plotClasses()
plotDecisionBoundary(0.29, 0.31, -1.9)
params = (0.29, 0.31, -1.9)
calculateMSE(dataVectors, params, patternClasses)

plotDecisionBoundary(0.5, 0.5, -1.8)
params = (0.5, 0.5, -1.8)
calculateMSE(dataVectors, params, patternClasses)

plt.show()

# compute gradient wrt weights 2d
plt.figure()
plotClasses()

plotDecisionBoundary(0.87, 0.93, -6.5)
w1, w2, w0 = computeGradient(data23['petal_length'], data23['petal_width'], 0.87, 0.93, -6.5, patternClasses)
plotDecisionBoundary(w1, w2, w0)
plt.show()