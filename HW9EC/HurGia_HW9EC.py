import numpy as np
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier
from pandas import DataFrame as df
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from seaborn import set, heatmap
from sklearn.preprocessing import StandardScaler
import warnings
from sklearn.exceptions import ConvergenceWarning

def classify_iris(hidden_layer_sizes, activation, max_iter=500):
    # load data
    iris = load_iris()
    X = iris.data
    y = iris.target

    # scale data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=221)

    # mlp
    mlp = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, 
                        solver='adam', warm_start=True, early_stopping=True, validation_fraction=0.1)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    # learning curve
    train_errors = []
    test_errors = []

    for i in range(1, max_iter + 1):
        mlp.max_iter = i 
        mlp.fit(x_train, y_train)
        train_errors.append(1 - mlp.score(x_train, y_train))
        test_errors.append(1 - mlp.score(x_test, y_test))

    # plot training and testing error over iterations
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, max_iter + 1), train_errors, label="Training Error", linestyle='-')
    plt.plot(range(1, max_iter + 1), test_errors, label="Testing Error", linestyle='-')
    plt.title(f"Nonlinearity: {activation}, hidden layers: {hidden_layer_sizes}")
    plt.xlabel("Number of Iterations (Epochs)")
    plt.ylabel("Error Rate")
    plt.legend()
    plt.grid()
    plt.show()
    
    # confusion matrix
    pred = mlp.predict(X)
    class_names = iris.target_names
    cm = confusion_matrix(y, pred, labels=[0, 1, 2])
    df_cm = df(cm, index=class_names, columns=class_names)

    set(style="whitegrid", palette="muted")
    set(font_scale=1.2)
    plt.figure(figsize=(6, 5))
    heatmap(df_cm, annot=True, annot_kws={"size": 18}, cmap="PiYG")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix", fontsize=20)
    plt.show()

    test_accuracies(X, y, mlp)

def test_accuracies(X, y, mlp):
    train_accuracies = []
    test_accuracies = []
    for i in range(10):
        x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=i)
        mlp.fit(x_train, y_train)
        train_accuracies.append(mlp.score(x_train, y_train))
        test_accuracies.append(mlp.score(x_test, y_test))

    print(f"Average training accuracy: ", np.mean(train_accuracies))
    print(f"Average test accuracy: ", np.mean(test_accuracies))

classify_iris((50,), 'relu')
classify_iris((100,), 'relu')
classify_iris((50, 50), 'relu') 
classify_iris((100, 50), 'relu')

classify_iris((50,), 'tanh')
classify_iris((100,), 'tanh')
classify_iris((50, 50), 'tanh') 
classify_iris((100, 50), 'tanh')

classify_iris((50,), 'logistic')
classify_iris((100,), 'logistic')
classify_iris((50, 50), 'logistic') 
classify_iris((100, 50), 'logistic')