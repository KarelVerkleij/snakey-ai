import numpy as np

# sourced from https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm

# neural network configs

class nn_snake:

    def __init__(self):
        
        self.n_x = 7   # nodes in input layer
        self.n_h = 9   # nodes in hidden layer I
        self.n_h2 = 15 # nodes in hidden layer II
        self.n_y = 3   # nodes in output layer

        self.W1_shape = (self.n_h, self.n_x) # Weights between input and hidden layer I.
        self.W2_shape = (self.n_h2, self.n_h) # Weights between hidden layer I and hidden layer II.
        self.W3_shape = (self.n_y, self.n_h2) # Weights between hidden layer II and output layer.

    def forward_propagation(self, X, individual):
        self.W1, self.W2, self.W3 = self.get_weights_from_encoded(individual)
        
        self.Z1 = np.matmul(self.W1, X.T)
        self.A1 = np.tanh(self.Z1)
        self.Z2 = np.matmul(self.W2, self.A1)
        self.A2 = np.tanh(self.Z2)
        self.Z3 = np.matmul(self.W3, self.A2)
        
        self.A3 = self.softmax(self.Z3)
        
        return self.A3

    def get_weights_from_encoded(self, individual):
        self.W1 = individual[0:self.W1_shape[0] * self.W1_shape[1]]
        self.W2 = individual[self.W1_shape[0] * self.W1_shape[1]:self.W2_shape[0] * self.W2_shape[1] + self.W1_shape[0] * self.W1_shape[1]]
        self.W3 = individual[self.W2_shape[0] * self.W2_shape[1] + self.W1_shape[0] * self.W1_shape[1]:]
        return (self.W1.reshape(self.W1_shape[0], self.W1_shape[1]), 
                self.W2.reshape(self.W2_shape[0], self.W2_shape[1]), 
                self.W3.reshape(self.W3_shape[0], self.W3_shape[1]))

    def softmax(self, z):
        self.s = np.exp(z.T) / np.sum(np.exp(z.T), axis=1).reshape(-1, 1)
        return self.s

