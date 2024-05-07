import numpy as np
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt

# 1. Implement logistic map
def logistic_map(x, a):
    return a * x * (1 - x)

# 2. Visualize the bifurcation diagram for different values of the parameter a
a_values = np.linspace(0, 4.0, 1000)
iterations = 1000
transitions = 100

x = np.zeros(iterations)
for a in a_values:
    x[0] = 0.5
    for i in range(1, iterations):
        x[i] = logistic_map(x[i-1], a)
    plt.plot([a] * (iterations - transitions), x[transitions:], ',k', alpha=0.2)

plt.xlabel('Parameter a')
plt.ylabel('x')
plt.title('Bifurcation Diagram')

# 3. Use a different model architecture
model = keras.Sequential([
    keras.layers.Dense(32, activation='tanh', input_shape=(1,)),
    keras.layers.Reshape((32, 1)),  # Add a reshape layer to convert input to 3D
    keras.layers.Conv1D(filters=32, kernel_size=3, activation='tanh'),
    keras.layers.MaxPooling1D(pool_size=2),
    keras.layers.Conv1D(filters=64, kernel_size=3, activation='tanh'),
    keras.layers.MaxPooling1D(pool_size=2),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='tanh'),
    keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mean_squared_error')

# Prepare the training data
x_train = a_values.reshape(-1, 1)
y_train = np.zeros((len(a_values), iterations - transitions, 1))

for i, a in enumerate(a_values):
    x[0] = 0.5
    for j in range(1, iterations):
        x[j] = logistic_map(x[j-1], a)
    y_train[i, :, 0] = x[transitions:]

# Train the model
model.fit(x_train, y_train, epochs=5, verbose=1, batch_size=32, validation_split=0.2)

# 4. Predict the logistic map point by point
x_pred = np.linspace(0, 4.0, 1000)  # Values of 'a' for prediction
x_init = 0.5  # Initial value of x for prediction
predictions = np.zeros_like(x_pred)

for i, a in enumerate(x_pred):
    x_curr = x_init
    for _ in range(transitions):
        x_curr = logistic_map(x_curr, a)
    predictions[i] = x_curr

# Visualize the predicted bifurcation map
plt.plot(x_pred, predictions, 'r')
plt.xlabel('Parameter a')
plt.ylabel('x')
plt.title('Predicted Bifurcation Diagram')
plt.show()
