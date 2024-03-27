import numpy as np
import tkinter as tk

class HopfieldNetwork2D:
    def __init__(self, pattern_size):
        self.pattern_size = pattern_size
        self.weights = np.zeros((pattern_size * pattern_size, pattern_size * pattern_size))

    def train(self, patterns):
        num_patterns = len(patterns) # počet trénovacích vzorů
        for pattern in patterns: # pro každý trénovací vzor
            pattern_vec = np.array(pattern).reshape(-1, 1) # převedeme vzor na vektor
            self.weights += np.dot(pattern_vec, pattern_vec.T) # vynásobíme ho samotným sebou a přičteme k váhám
        np.fill_diagonal(self.weights, 0) # diagonálu váh nastavíme na 0
        self.weights /= num_patterns # vydělíme počtem vzorů
        

    def update_sync(self, input_pattern, max_iters=100):
        pattern_vec = np.array(input_pattern).flatten() # převedeme vzor na vektor
        for _ in range(max_iters):
            new_pattern_vec = np.sign(np.dot(self.weights, pattern_vec)) # vynásobíme váhy a vektor a aplikujeme signum
            if np.array_equal(new_pattern_vec, pattern_vec): # pokud se nic nezměnilo, vrátíme vzor
                return new_pattern_vec.reshape(self.pattern_size, self.pattern_size) # převedeme vektor na matici
            pattern_vec = new_pattern_vec # jinak přepíšeme vzor novým vzorem
        return pattern_vec.reshape(self.pattern_size, self.pattern_size) # vrátíme nový vzor

    def update_async(self, input_pattern, max_iters=1000):
        pattern_vec = np.array(input_pattern).flatten()
        num_neurons = self.pattern_size * self.pattern_size # počet neuronů
        indices = np.arange(num_neurons) # pole indexů
        accumulated_weights = np.zeros((num_neurons, num_neurons)) # inicializace matice pro akumulaci váh

        for _ in range(max_iters):
            np.random.shuffle(indices) # zamícháme indexy
            for i in indices: 
                new_pattern_vec = np.sign(np.dot(self.weights[i], pattern_vec)) # vynásobíme váhy a vektor a aplikujeme signum
                
                new_pattern_vec = np.where(np.dot(self.weights[i], pattern_vec) >= 0, 1, -1) # pokud je váha větší než 0, nastavíme 1, jinak -1
                
                pattern_vec[i] = new_pattern_vec # přepíšeme vzor novým vzorem
                
                weighted_matrix = np.outer(new_pattern_vec, pattern_vec) # vynásobíme nový vzor a vektor a uložíme do matice
                
                accumulated_weights += weighted_matrix # přičteme váhy do akumulovaných vah

        self.weights += accumulated_weights
        
        if pattern_vec.size != self.pattern_size * self.pattern_size:
            print(f"Error: The size of the new pattern vector is not {self.pattern_size * self.pattern_size}, but {pattern_vec.size}.")
            return None
        
        return pattern_vec.reshape(self.pattern_size, self.pattern_size)


    



def draw_pattern(canvas, pattern, x_offset, y_offset, cell_size):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            color = "black" if pattern[i][j] == 1 else "white"
            canvas.create_rectangle(x_offset + j * cell_size, y_offset + i * cell_size,
                                    x_offset + (j + 1) * cell_size, y_offset + (i + 1) * cell_size,
                                    fill=color)

def visualize(pattern_original,pattern_x, pattern_noisy, pattern_recovered_sync, pattern_recovered_async):
    root = tk.Tk()
    root.title("Hopfield Network Visualization")

    cell_size = 30
    canvas_width = max(len(pattern_original[0]), len(pattern_noisy[0]))
    canvas_height = max(len(pattern_original), len(pattern_noisy))

    if pattern_recovered_sync is not None:
        canvas_width = max(canvas_width, len(pattern_recovered_sync[0]))
        canvas_height = max(canvas_height, len(pattern_recovered_sync))

    if pattern_recovered_async is not None:
        canvas_width = max(canvas_width, len(pattern_recovered_async[0]))
        canvas_height = max(canvas_height, len(pattern_recovered_async))

    canvas_width = 1500
    canvas_height = 400

    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()

    draw_pattern(canvas, pattern_original, 10, 10, cell_size)
    draw_pattern(canvas, pattern_x, 10 + canvas_width / 4, 10, cell_size)
    draw_pattern(canvas, pattern_noisy, 10 + 2 * canvas_width / 4, 10, cell_size)     
    draw_pattern(canvas, pattern_recovered_sync, 10, 10 + canvas_height / 2, cell_size)
    draw_pattern(canvas, pattern_recovered_async, 10 + canvas_width / 4, 10 + canvas_height / 2, cell_size)
    root.mainloop()


# Define patterns (representation of the digit "2")
pattern_2 = [
    [-1, 1, 1, 1, -1],
    [1, -1, -1, -1, 1],
    [-1, -1, 1, 1, -1],
    [-1, 1, -1, -1, -1],
    [1, 1, 1, 1, 1]
]
pattern_x = [
    [1, -1, -1, -1, 1],
    [-1, 1, -1, 1, -1],
    [-1, -1, 1, -1, -1],
    [-1, 1, -1, 1, -1],
    [1, -1, -1, -1, 1]
]


# Create Hopfield Network
hopfield_net = HopfieldNetwork2D(pattern_size=len(pattern_2))

# Train the network with patterns
hopfield_net.train([np.array(pattern_2), np.array(pattern_x)])

# Noisy Pattern 2 (introducing noise to the digit "2")
noisy_pattern_2 = [
    [-1,- 1, -1, -1, -1],
    [-1, -1, -1, -1, -1],
    [-1, -1, 1, -1, 1],
    [-1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 1]
]

# Recover using synchronous update
recovered_sync = hopfield_net.update_sync(noisy_pattern_2)

# Recover using asynchronous update
recovered_async = hopfield_net.update_async(noisy_pattern_2)


visualize(pattern_2, pattern_x, noisy_pattern_2, recovered_sync, recovered_async)
