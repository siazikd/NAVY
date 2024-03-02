from Core.Perceptron import Perceptron 
import numpy as np

x_train = np.random.uniform(-15, 15, size=(100, 2))
y_train = np.where(x_train[:, 1] > 3 * x_train[:, 0] + 2, 1, -1)

perceptron = Perceptron()
perceptron.train(x_train, y_train)
perceptron.plot(x_train[:, 0], x_train[:, 1])

x_test = np.random.uniform(-2,2, size=(1000, 2))
y_test = np.where(x_test[:, 1] > 3 * x_test[:, 0] + 2, 1, -1)
print('accuracy: ', perceptron.accuracy(x_test, y_test), '%')
perceptron.plot(x_test[:, 0], x_test[:, 1])
