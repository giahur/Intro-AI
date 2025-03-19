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
    plt.figure()
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
    plotClasses()
    x1 = data23['petal_length']
    # for given x1, find x2 where sigmoid = 0.5
    x2 = -(w1 * x1 + b) / w2
    plt.plot(x1, x2)
    plt.show()

# plot neural network output over input space
def plotNNO(w1, w2, b):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    # grid of x1, x2 values
    x1 = data23['petal_length']
    x2 = data23['petal_width']
    x1Grid, x2Grid = np.meshgrid(x1, x2)

    # neural network output for each value in grid
    z = neuralNetworkOutput(x1Grid, x2Grid, w1, w2, b)
    # surface
    surf = ax.plot_surface(x1Grid, x2Grid, z, cmap='coolwarm', antialiased=False)

    # x1, x2 values
    for species, group in data23.groupby('species'):
        ax.scatter(group['petal_length'], group['petal_width'], label=species)

    # Set labels and title
    ax.set_title('Neural Network Output')
    ax.set_xlabel('Petal Length')
    ax.set_ylabel('Petal Width')
    ax.set_zlabel('Neural Network Output')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.legend()

    # Show the plot
    plt.show()

# examples of 2nd and 3rd classes
def outputExamples():
    print("unambiguous versicolor: ")
    print(neuralNetworkOutput(3.3, 1, 0.87, 0.93, -5.7))
    print(neuralNetworkOutput(3.9, 1.4, 0.87, 0.93, -5.7))
    print("unambiguous virginica: ")
    print(neuralNetworkOutput(6, 2.5, 0.87, 0.93, -5.7))
    print(neuralNetworkOutput(6.7, 2.2, 0.87, 0.93, -5.7))
    print("ambiguous versicolor: ")
    print(neuralNetworkOutput(4.9, 1.5, 0.87, 0.93, -5.7))
    print(neuralNetworkOutput(4.7, 1.6, 0.87, 0.93, -5.7))
    print("ambiguous virginica: ")
    print(neuralNetworkOutput(5, 1.5, 0.87, 0.93, -5.7))
    print(neuralNetworkOutput(4.8, 1.8, 0.87, 0.93, -5.7))
    print("wrong side of boundary: ")
    print(neuralNetworkOutput(4.5, 1.7, 0.87, 0.93, -5.7))
    print(neuralNetworkOutput(5, 1.7, 0.87, 0.93, -5.7))

# show graphs 1a
plotClasses()
plt.show()
# plot the decision boundary 1c
plotDecisionBoundary(0.87, 0.93, -5.7)
# plot the output of neural network 1d
plotNNO(0.87, 0.93, -5.7)
# plot output of simple classifier 1e
outputExamples()