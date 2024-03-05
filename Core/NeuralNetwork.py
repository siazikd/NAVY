from Core.Functions import sigmoid_derivative
from Core.Layer import Layer


class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.hidden_layer = Layer(input_size, hidden_size)
        self.output_layer = Layer(hidden_size, output_size)

    def train(self, inputs, expected_output, lr=0.1, epochs=10000):
        for _ in range(epochs):
            # Forward Propagation
            hidden_output = self.hidden_layer.forward(inputs)
            output = self.output_layer.forward(hidden_output)

            # Backpropagation
            output_error = expected_output - output
            output_delta = output_error * sigmoid_derivative(output)

            hidden_error = self.output_layer.backward(output_delta, lr)
            hidden_delta = hidden_error * sigmoid_derivative(hidden_output)

            self.hidden_layer.backward(hidden_delta, lr)

        return output