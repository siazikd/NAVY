import numpy as np

from Core.Functions import sigmoid

class Layer:
    def __init__(self, input_size, num_neurons):
        self.num_neurons = num_neurons
        self.weights = np.random.uniform(size=(input_size, num_neurons))
        self.bias = np.random.uniform(size=(1, num_neurons))

    def forward(self, inputs) -> float:
        self.inputs = inputs
        self.activation = sigmoid(np.dot(inputs, self.weights) + self.bias)
        return self.activation

    def backward(self, delta, lr) -> float:
        delta_weights = np.dot(self.inputs.T, delta)
        self.weights += lr * delta_weights
        self.bias += lr * np.sum(delta, axis=0, keepdims=True)
        return np.dot(delta, self.weights.T)