import numpy as np

import matplotlib.pyplot as plt

def fractal_landscape(iterations, length, height_variation, start_y):
    landscape = [(0, start_y), (length, start_y)]  # rovná čára
    
    for _ in range(iterations):  # Provede se tolikrát, kolik je iterací
        new_landscape = [] 
        for i in range(len(landscape) - 1):
            start_x, start_y = landscape[i] 
            end_x, end_y = landscape[i + 1] 
            
            mid_x = (start_x + end_x) / 2  
            mid_y = (start_y + end_y) / 2
            
            if np.random.rand() < 0.5: 
                mid_y += np.random.uniform(-height_variation, height_variation)
            else:
                mid_y -= np.random.uniform(-height_variation, height_variation)
            
            new_landscape.append((start_x, start_y)) 
            new_landscape.append((mid_x, mid_y))
            
            if i == len(landscape) - 2:  
                new_landscape.append((end_x, end_y))
        
        landscape = new_landscape
    
    return landscape

def plot_landscapes(landscapes):
    plt.figure(figsize=(10, 6))
    for i, (landscape, color) in enumerate(landscapes, 1):
        x = [point[0] for point in landscape]
        y = [point[1] for point in landscape]
        plt.plot(x, y, color=color)
        plt.fill_between(x, y, -10, color=color, alpha=1)

    plt.title("Fractal Landscapes")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.xlim(0, 10)
    plt.ylim(-10, 10)
    plt.show()

# Define landscapes
landscapes = [
    (fractal_landscape(4, 10, 2, 6), 'brown'),
    (fractal_landscape(8, 10, 0.5, 0), 'yellow'),
    (fractal_landscape(12, 10, 1, -7), 'green')
]

# Plot all landscapes
plot_landscapes(landscapes)
