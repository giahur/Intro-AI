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
    return float(mse)

def computeGradient(x1, x2, w1, w2, w0, patternClasses):
    N = patternClasses.size
    NNO = neuralNetworkOutput(x1, x2, w1, w2, w0)
    current = (NNO - patternClasses) * NNO * (1 - NNO)
    gradw1 = (2/N) * np.sum(current * x1)
    gradw2 = (2/N) * np.sum(current * x2)
    gradw0 = (2/N) * np.sum(current)

    return gradw1, gradw2, gradw0

def updateWeight(w1, w2, w0):
    gradw1, gradw2, gradw0 = computeGradient(x1, x2, w1, w2, w0, patternClasses)
    w1 = w1 - (1/10) * gradw1
    w2 = w2 - (1/10) * gradw2
    w0 = w0 - (1/10) * gradw0

    return w1, w2, w0

def gradientDescent(x1, x2, w1, w2, w0, patternClasses):
    ax = plt.axes()
    ax.set_title("Learning Curve")
    ax.set_xlabel("Iterations")
    ax.set_ylabel("MSE")

    mse = calculateMSE(data23[['petal_length', 'petal_width']], (w1, w2, w0), patternClasses)
    mseCurve = [mse]
    for i in range(1000):
        w1new, w2new, w0new = updateWeight(w1, w2, w0)
        newMSE = calculateMSE(data23[['petal_length', 'petal_width']], (w1new, w2new, w0new), patternClasses)
        mseCurve.append(newMSE)

        if abs(newMSE - mse) < 1:
            break
        w1, w2, w0 = w1new, w2new, w0new
        mse = newMSE

    ax.plot(mseCurve)
    plt.show()


x1 = data23['petal_length']
x2 = data23['petal_width']
patternClasses = np.where(data23['species'] =='versicolor', 0, 1)
gradientDescent(x1, x2, 0.5, 0.5, -2, patternClasses)