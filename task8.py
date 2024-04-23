import numpy as np

import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    z = 0
    for i in range(max_iter):
        z = z**2 + c
        if abs(z) > 2:
            return i
    return max_iter

def plot_mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter):
    image = np.zeros((height, width, 4)) 
    for i, x in enumerate(np.linspace(x_min, x_max, width)): 
        for j, y in enumerate(np.linspace(y_min, y_max, height)): 
            c = x + y * 1j  
            iteration = mandelbrot(c, max_iter)
            hue = iteration / max_iter
            color = plt.cm.plasma(hue)
            image[j, i] = color 
    plt.imshow(image)
    plt.show()

x_min, x_max = -2, 1
y_min, y_max = -1, 1
width, height = 300, 300
max_iter = 40


plot_mandelbrot(x_min, x_max, y_min, y_max, width, height, max_iter)


