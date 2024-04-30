import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Define the forest size
forest_size = 100

# Define the probability parameters
p = 0.05  # Probability of tree growth
f = 0.001  # Probability of tree catching fire

# Initialize the forest grid
forest = np.random.choice([0, 1], size=(forest_size, forest_size), p=[1-0.5, 0.5])
# 0 represents empty or burnt area, 1 represents a live tree, 2 represents a burning tree

# Define von Neumann neighborhood
def get_neighbors_von_neumann(x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < forest_size - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < forest_size - 1:
        neighbors.append((x, y + 1))
    return neighbors

# Function to update the forest state
def update_forest(frameNum, img, forest, forest_size):
    new_forest = np.zeros((forest_size, forest_size))
    for i in range(forest_size):
        for j in range(forest_size):
            if forest[i, j] == 0 or forest[i, j] == 3:  # Empty or burnt area
                if np.random.random() < p:
                    new_forest[i, j] = 1  # Regrow tree with probability p
            elif forest[i, j] == 1:  # Live tree
                neighbors = get_neighbors_von_neumann(i, j)
                for neighbor in neighbors:
                    if forest[neighbor[0], neighbor[1]] == 2:  # Neighbor is burning
                        new_forest[i, j] = 2  # Tree catches fire
                        break
                else:
                    if np.random.random() < f:  # Tree catches fire with probability f
                        new_forest[i, j] = 2
                    else:
                        new_forest[i, j] = 1
            elif forest[i, j] == 2:  # Burning tree
                new_forest[i, j] = 3  # Burnt area
    img.set_array(new_forest)
    forest[:] = new_forest[:]
    return img,

# Create a figure and axis
fig, ax = plt.subplots()
img = ax.imshow(forest, cmap='viridis', interpolation='nearest')

# Define custom colors for grass, trees, fire, and burnt areas
colors = [(0, 0.5, 0), (0.5, 0.25, 0), (1, 0.5, 0), (0, 0, 0)]
cmap = LinearSegmentedColormap.from_list('forest_colors', colors)

# Update the colormap
img.set_cmap(cmap)

# Update the forest state in each frame
ani = animation.FuncAnimation(fig, update_forest, fargs=(img, forest, forest_size),
                              frames=200, interval=50, blit=True)

plt.title('Forest Fire Simulation')
plt.show()
