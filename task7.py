import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Define the affine transformations for the first model
transformations1 = [
    [ 0.00, 0.00, 0.01, 0.00, 0.26, 0.00, 0.00, 0.00, 0.05, 0.00, 0.00, 0.00],
    [0.20, -0.26, -0.01, 0.23, 0.22, -0.07, 0.07, 0.00, 0.24, 0.00, 0.80, 0.00],
    [-0.25, 0.28, 0.01, 0.26, 0.24, -0.07, 0.07, 0.00, 0.24, 0.00, 0.22, 0.00],
    [0.85, 0.04, -0.01, -0.04, 0.85, 0.09, 0.00, 0.08, 0.84, 0.00, 0.80, 0.00]
]

# Define the affine transformations for the second model
transformations2 = [
    [0.05,0.00, 0.00, 0.00 ,0.60, 0.00, 0.00, 0.00, 0.05 ,0.00 ,0.00, 0.00],
    [0.45, -0.22 ,0.22 ,0.22 ,0.45, 0.22, -0.22, 0.22, -0.45, 0.00 ,1.00, 0.00],
    [-0.45 ,0.22, -0.22, 0.22, 0.45, 0.22, 0.22, -0.22, 0.45, 0.00, 1.25, 0.00],
    [0.49, -0.08, 0.08, 0.08, 0.49, 0.08, 0.08, -0.08, 0.49, 0.00, 2.00, 0.00]
]
# Initialize x, y, z coordinates
x, y, z = 0, 0, 0

# Initialize the history to store the points
history1 = []
history2 = []

transformations = [transformations1, transformations2]

# Number of iterations
iterations = 10000

for transformation in transformations:
    for _ in range(iterations):
        random_row = random.randint(0, 3)
        a,b,c,d,e,f,g,h,i,j,k,l = transformation[random_row]

        # Apply the transformation
        x_new = a * x + b * y + c * z + j
        y_new = d * x + e * y + f * z + k
        z_new = g * x + h * y + i * z + l

        # Update the coordinates
        x, y, z = x_new, y_new, z_new

        # Store the point into history for the corresponding model
        if transformation == transformations1:
            history1.append((x, y, z))
        else:
            history2.append((x, y, z))

# Extract x, y, z coordinates from history for both models
x_vals2, y_vals2, z_vals2 = zip(*history2)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.scatter(*zip(*history1), c='b', marker='.')
ax1.set_title('First Model')

# Plot the points for the second model
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(x_vals2, y_vals2, z_vals2, c='r', marker='.')
ax2.set_title('Second Model')
ax2.set_xlabel('X Label')
ax2.set_ylabel('Y Label')
ax2.set_zlabel('Z Label')

plt.show()