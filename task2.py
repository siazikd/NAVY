import numpy as np
from Core.NeuralNetwork import NeuralNetwork


inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
expected_output = np.array([[0], [1], [1], [0]])

input_size = 2
hidden_size = 2
output_size = 1
network = NeuralNetwork(input_size, hidden_size, output_size)

# Train the neural network
predicted_output = network.train(inputs, expected_output, lr=0.1, epochs=10000)
print(*predicted_output)


# predict the output
print(network.predict(np.array([0, 0])))
print(network.predict(np.array([0, 1])))
print(network.predict(np.array([1, 0])))
print(network.predict(np.array([1, 1])))