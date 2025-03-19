import numpy as np
import matplotlib.pyplot as plt

def posteriorProb(flavors, hRatios, hProbs, candies):
    likelihoods = {}
    for i in range(len(flavors)):
        temp = []
        for j in range(len(hRatios)):
            temp.append(hRatios[j][i])
        likelihoods[flavors[i]] = np.array(temp)
    priors = np.array(hProbs)
    posteriors = [priors]
    for flavor in candies:
        likelihood = likelihoods[flavor]
        newPosteriors = priors * likelihood
        priors = newPosteriors / newPosteriors.sum()
        posteriors.append(priors)
    
    posteriors = np.array(posteriors)
    numCandies = np.arange(len(candies) + 1)

    plt.figure(figsize=(10,5))
    for ind in range(len(hRatios)):
        plt.plot(numCandies, posteriors[:,ind], label=f"h{ind+1}")
    plt.title("Candy Bags O' Surprise")
    plt.xlabel("Number of observations in d")
    plt.ylabel("Posterior probability of hypothesis")
    plt.legend()
    plt.grid(True)

    ax = plt.gca()
    ax.set_xlim([0, len(candies)])
    ax.set_ylim([0, 1.0])
    plt.show()

def main():
    flavors = ['cherry', 'lime']
    hRatios = [[1.0, 0.0], [0.75, 0.25], [0.5, 0.5], [0.25, 0.75], [0.0, 1.0]]
    hProbs = [0.1, 0.2, 0.4, 0.2, 0.1]
    candiesH1 = ['cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry']
    candiesH1b = ['cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry','cherry']
    candiesH2 = ['lime','cherry','cherry','cherry','lime','cherry','cherry','cherry','lime','cherry','cherry','cherry']
    posteriorProb(flavors, hRatios, hProbs, candiesH1)
    posteriorProb(flavors, hRatios, hProbs, candiesH1b)
    posteriorProb(flavors, hRatios, hProbs, candiesH2)

if __name__=="__main__":
    main()