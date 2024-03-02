import numpy as np
import matplotlib.pyplot as plt

class Perceptron:
    def __init__(self, w=None, b=None, fn: function = np.sign):
        self.w = np.random.rand(2) if w is None else w # Inicializace vah
        self.b = np.random.rand()  if b is None else b # Inicializace biasu
        self.fn = fn # Aktivacni funkce

    def __calculateGuess(self, x) -> int:
        return self.fn(np.dot(x, self.w) + self.b) # Vypocet vystupu perceptronu

    def __calculateError(self, y, y_guess) -> float:
        return y - y_guess # Vypocet chyby

    def __calculateNewWeights(self, x, error, lr=0.1) -> np.ndarray:
        return self.w + lr * np.dot(error, x) # Vypocet novych vah

    def __calculateNewBias(self, error, lr=0.1) -> float:
        return self.b + lr * error # Vypocet noveho biasu

    def train(self, x, y, epochs=50, lr=0.1) -> None:
        for epoch in range(epochs):
            changed = False
            for i in range(len(x)):
                coordinates = x[i]  
                y_guess = self.__calculateGuess(coordinates)
                if y_guess == y[i]: # Pokud je predikce spravna, tak se vahy nemusí měnit
                    continue
                error = self.__calculateError(y[i], y_guess)
                w_new = self.__calculateNewWeights(coordinates, error, lr)
                self.b = self.__calculateNewBias(error, lr)
                if not np.array_equal(w_new, self.w): # Pokud se vahy zmenily, tak se zmenila i predikce
                    changed = True
                self.w = w_new
                
            if not changed:
                break
        print('Training finished after ', epoch + 1, ' epochs.')

    def plot(self, x, y) -> None:
        plt.scatter(x, y, c=np.where(self.predict(np.column_stack((x, y))) == 1, 'r', 'b')) # Vykresleni bodu
        plt.plot(x,3*x+2, 'grey') # Vykresleni oddelovaci primky
        plt.show() 
        
    def predict(self, x):
        return self.__calculateGuess(x) # Predikce vystupu perceptronu
    
    def accuracy(self, x, y):
        y_guess = np.array([self.predict(x) for x in x]) # Predikce vystupu perceptronu pro vsechny vstupy
        return np.sum(y_guess == y) / len(y) * 100 # Vypocet presnosti perceptronu
    
    
    
    
