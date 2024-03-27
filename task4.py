import random
import time
import tkinter as tk

class QLearn:
    def __init__(self, actions, epsilon=0.05, alpha=0.2, gamma=0.9):
        self.q = {} # slovnik pro ukladani hodnot Q
        self.epsilon = epsilon # exploration constant
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.actions = actions  # akce, ktere muze agent provest

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)  # pokud neexistuje, tak se vrati 0 

    def learnQ(self, state, action, reward, value): 
        oldv = self.q.get((state, action), None) # hodnota Q pro stav a akci
        if oldv is None: # pokud neexistuje, tak se vytvori
            self.q[(state, action)] = reward
        else: # jinak se upravi hodnota Q
            self.q[(state, action)] = oldv + self.alpha * (value - oldv) # vypočita se jako stará hodnota + learning rate * (nová hodnota - stará hodnota)

    def chooseAction(self, state):
        if random.random() < self.epsilon: # pokud je nahodne cislo mensi nez epsilon, tak se vybere nahodna akce
            action = random.choice(self.actions)
        else: # jinak se vybere akce s nejvetsi hodnotou Q
            q = [self.getQ(state, a) for a in self.actions] # najde se hodnota Q pro kazdou akci
            maxQ = max(q) 
            count = q.count(maxQ) 
            if count > 1:  # pokud je vice akci s nejvetsi hodnotou Q, tak se vybere nahodna z techto akci
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else: # jinak se vybere akce s nejvetsi hodnotou Q
                i = q.index(maxQ)
            action = self.actions[i]
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])  # maximalni hodnota Q pro stav2
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)  # uprava hodnoty Q pro stav1
        

def print_maze(canvas, maze, mouse_position):
    canvas.delete("all")
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            x1, y1 = j * 20, i * 20
            x2, y2 = x1 + 20, y1 + 20
            if (i, j) == mouse_position:
                canvas.create_rectangle(x1, y1, x2, y2, fill='gray') 
            elif cell == -1: 
                canvas.create_rectangle(x1, y1, x2, y2, fill='white') 
            elif cell == 1: 
                canvas.create_rectangle(x1, y1, x2, y2, fill='yellow') 
            elif cell == -2: 
                canvas.create_rectangle(x1, y1, x2, y2, fill='black') 

def main():
    actions = ['up', 'down', 'left', 'right']
    agent = QLearn(actions)

    maze_size = 15
    trap_size = 15
    maze = [[-1 for _ in range(maze_size)] for _ in range(maze_size)]
    cheese_location = (random.randint(0, maze_size-1), random.randint(0, maze_size-1))
    trap_locations = []
    for _ in range(trap_size):  
        trap_location = (random.randint(0, maze_size-1), random.randint(0, maze_size-1))
        while trap_location == cheese_location or trap_location in trap_locations:
            trap_location = (random.randint(0, maze_size-1), random.randint(0, maze_size-1))
        trap_locations.append(trap_location)
        maze[trap_location[0]][trap_location[1]] = -2
    maze[cheese_location[0]][cheese_location[1]] = 1

    root = tk.Tk()
    canvas = tk.Canvas(root, width=maze_size*20, height=maze_size*20)
    canvas.pack()

    num_episodes = 5_000
    for episode in range(num_episodes):
        mouse_position = (random.randint(0, maze_size-1), random.randint(0, maze_size-1)) 

        while True:
            action = agent.chooseAction(mouse_position) 

            if action == 'up' and mouse_position[0] > 0:
                next_position = (mouse_position[0] - 1, mouse_position[1])
            elif action == 'down' and mouse_position[0] < maze_size - 1:
                next_position = (mouse_position[0] + 1, mouse_position[1])
            elif action == 'left' and mouse_position[1] > 0:
                next_position = (mouse_position[0], mouse_position[1] - 1)
            elif action == 'right' and mouse_position[1] < maze_size - 1:
                next_position = (mouse_position[0], mouse_position[1] + 1)
            else:
                next_position = mouse_position

            if next_position == cheese_location:
                reward = 1
            elif next_position in trap_locations:
                reward = -1
            else:
                reward = 0

            agent.learn(mouse_position, action, reward, next_position)

            if next_position == cheese_location or next_position in trap_locations:
                break

            mouse_position = next_position
            
    print('Training done!')
    print('Testing...')
    mouse_position = (random.randint(0, maze_size-1), random.randint(0, maze_size-1))
    print_maze(canvas, maze, mouse_position)
    root.update()
    time.sleep(3)    
    while True:
        action = agent.chooseAction(mouse_position)
        if action == 'up' and mouse_position[0] > 0:
            next_position = (mouse_position[0] - 1, mouse_position[1])
        elif action == 'down' and mouse_position[0] < maze_size - 1:
            next_position = (mouse_position[0] + 1, mouse_position[1])
        elif action == 'left' and mouse_position[1] > 0:
            next_position = (mouse_position[0], mouse_position[1] - 1)
        elif action == 'right' and mouse_position[1] < maze_size - 1:
            next_position = (mouse_position[0], mouse_position[1] + 1)
        else:
            next_position = mouse_position
        if next_position == cheese_location:
            print('Cheese found!')
            break
        elif next_position in trap_locations:
            print('Trap found!')
            break
        mouse_position = next_position
        print_maze(canvas, maze, mouse_position)
        root.update()
        time.sleep(0.5)

    root.mainloop()

if __name__ == "__main__":
    main()
