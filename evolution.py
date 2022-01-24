import copy

from player import Player
import numpy as np
import random
import pandas as pd

def top_k(x, num) :
    x= sorted(x, key= lambda i: i.fitness, reverse= True)
    return x[:num]

def roulette_wheel(x, num) :
    fits = list(np.cumsum(list(map(lambda i: i.fitness, x))))
    l = []
    for i in range(num):
        rnd = np.random.random() * fits[-1]
        index = fits.index(next(i for i in fits if rnd <= i))
        l.append(x[index])
    return l

def q_tournoment(x, num, q= 2) :
    l = []
    for i in range(num) :
        rnd = round(np.random.random() * (len(x)-1))
        max = x[rnd]
        for j in range(q - 1) :
            rnd = round(np.random.random() * (len(x)-1))
            temp = x[rnd]
            if temp.fitness > max.fitness :
                max = temp
        l.append(max)
    return l

def sus(x, num) :
    fits = list(np.cumsum(list(map(lambda i: i.fitness, x))))
    l = []
    length = fits[-1] / num
    rnd = np.random.random() * length
    for i in range(num) :
        index = fits.index(next(j for j in fits if (rnd + (i * length)) <= j))
        l.append(x[index])
    return l


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"
        self.accuracy = []
        self.mutate_num = 0

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        # TODO (Implement top-k algorithm here)
        # TODO (Additional: Implement roulette wheel here)
        # TODO (Additional: Implement SUS here)
        next_population = sus(players, num_players)
        # TODO (Additional: Learning curve)
        fits = list(map(lambda player: player.fitness, players))
        max = np.max(fits)
        min = np.min(fits)
        average = np.average(fits)
        var = np.var(fits)
        print([min, max, average, self.mutate_num])
        self.accuracy.append((min, max, average, self.mutate_num))
        return next_population

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )
            parents = sus(prev_players, num_players)
            random.shuffle(parents)
            children = []
            for i in range(0, len(parents), 2) :
                children += self.make_baby(parents[i], parents[i+1])
            return children

    def crossover(self, clayers1, clayers2, players1, players2):
        for i in range(len(players1)):
            layer1 = players1[i]
            layer2 = players2[i]
            length = len(layer1) * len(layer1[0])
            index = round(np.random.random() * length)
            layer3 = np.array(list(layer1.reshape(length)[:index]) + list(layer2.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            layer4 = np.array(list(layer2.reshape(length)[:index]) + list(layer1.reshape(length)[index:])).reshape([len(layer1), len(layer1[0])])
            clayers1[i] = layer3
            clayers2[i] = layer4

    def mutate(self, layers, threshold):
        for layer in layers:
            chance = np.random.random()
            if chance < threshold :
                self.mutate_num += 1
                length = len(layer) * len(layer[0])
                index = round(np.random.random() * (length-1))
                new_weight = np.random.normal(0, 1)
                layer.reshape(length)[index] = new_weight
                


    def make_baby(self, father, mother):
        mutate_thresh = 0.1
        baby_girl = self.clone_player(mother)
        baby_boy = self.clone_player(father)
        self.crossover(baby_boy.nn.layers, baby_girl.nn.layers, father.nn.layers, mother.nn.layers)
        self.crossover(baby_boy.nn.biases, baby_girl.nn.biases, father.nn.biases, mother.nn.biases)
        self.mutate(baby_boy.nn.layers, mutate_thresh)
        self.mutate(baby_girl.nn.layers, mutate_thresh)
        self.mutate(baby_girl.nn.biases, mutate_thresh)
        self.mutate(baby_boy.nn.biases, mutate_thresh)

        return [baby_girl, baby_boy]
        
        
    
    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
