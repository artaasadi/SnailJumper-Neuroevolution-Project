import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes):
        """
        Neural Network initialization.
        Given layer_sizes as an input, you have to design a Fully Connected Neural Network architecture here.
        :param layer_sizes: A list containing neuron numbers in each layers. For example [3, 10, 2] means that there are
        3 neurons in the input layer, 10 neurons in the hidden layer, and 2 neurons in the output layer.
        """
        # TODO (Implement FCNNs architecture here)
        layers = []
        biases = []
        for i in range((len(layer_sizes) - 1)) :
            layer = np.random.normal(0, 1, [layer_sizes[i+1], layer_sizes[i]])
            bias = np.zeros([layer_sizes[i+1], ])
            layers.append(layer)
            biases.append(bias)
        self.layers = layers
        self.biases = biases

    def activation(self, x, function= "sigmoid"):
        """
        The activation function of our neural network, e.g., Sigmoid, ReLU.
        :param x: Vector of a layer in our network.
        :return: Vector after applying activation function.
        """
        # TODO (Implement activation function here)
        if function == "sigmoid" :
            return 1/(1 + np.exp(-x))
        elif function == "softmax" :
            e = np.exp(x)
            return e / e.sum()
        elif function == "ReLU" :
            return np.maximum(x,0)

    def batch_normalization(self, x, eps=1e-5):
        mean = x.mean(axis= 0)
        var = x.var(axis= 0)
        std = np.sqrt(var + eps)
        return list(map(lambda i: (i - mean) / std, x))

    def forward(self, x):
        """
        Receives input vector as a parameter and calculates the output vector based on weights and biases.
        :param x: Input vector which is a numpy array.
        :return: Output vector
        """
        # TODO (Implement forward function here)
        # not using batch_normalization had better result
        #answer = self.batch_normalization(x)
        answer = x
        for i in range(len(self.layers)) :
            answer = self.activation(((self.layers[i] @ answer) + self.biases[i]), "sigmoid")

        return answer
