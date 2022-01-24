import copy

from player import Player
import numpy as np

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

            new_players = prev_players  # DELETE THIS AFTER YOUR IMPLEMENTATION
            return new_players

    def crossover(self, layers1, layers2):
        pass
    
    def make_baby(self, father, mother):
        baby_girl = Player(self.game_mode)
        baby_boy = Player(self.game_mode)
        baby_girl.fitness = father.fitness
        baby_boy.fitness = mother.fitness

        
    
    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
