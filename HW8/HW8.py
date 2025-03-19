import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

irisData = pd.read_csv('irisdata.csv')
X = irisData.iloc[:, :-1].values

def kMeansCluster(k, points, max_iters=100):
    # initialize vector mean to K random points
    means = points[np.random.choice(points.shape[0], k, replace=False)]
    
    # objective function value at each iteration
    objectiveValues = []

    for _ in range(max_iters):
        # initialize clusters list
        clusters = [[] for _ in range(k)]

        # assign each data point to nearest cluster based on euclidean distance
        labels = np.zeros(len(points))
        for i, point in enumerate(points):
            distances = [np.sum((point - mean) ** 2) for mean in means]
            clusterAssignment = np.argmin(distances)
            clusters[clusterAssignment].append(point)
            labels[i] = clusterAssignment

        # calculate/update means
        newMeans = [np.mean(cluster, axis=0) for cluster in clusters]

        # Calculate objective function
        objective = sum(np.sum((X[labels == k] - means[k]) ** 2) for k in range(len(means)))
        objectiveValues.append(objective)

        # converge
        if np.allclose(newMeans, means):
            break
        
        means = newMeans

    return np.array(means), labels, objectiveValues

# Apply k-means clustering with K=2 and K=3
K_values = [2, 3]
for K in K_values:
    print(f"\nRunning k-means with K={K}")
    means, labels, objectiveValues = kMeansCluster(K, X)

    # plot learning curve
    plt.figure()
    plt.plot(objectiveValues)
    plt.xlabel('Iteration')
    plt.ylabel('Objective Function Value')
    plt.title(f'Learning Curve for K={K}')
    plt.show()

    plt.figure()
    plt.scatter(X[:, 2], X[:, 3], c=labels, cmap='viridis', marker='o', edgecolor='k')
    plt.scatter(means[:, 2], means[:, 3], c='red', marker='x')  # Final means
    plt.xlabel("Petal Length")
    plt.ylabel("Petal Width")
    plt.title(f"K-means clustering with K={K}")
    plt.show()