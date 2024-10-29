from snake.snake_bot import BotApp
from snake.utils import overrides
from feed_foreward_neural_network import nn_snake
from numpy.random import randint, rand

import pygame

# sourced from https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm


# TODO combine into one class
class MLBotApp(BotApp):

    def __init__(self, bot_study_name='', log_file_path='../logs/bot_logic_greedy/test_log.log'):
        super().__init__()

        self.snake_speed = 100





# https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm/blob/main/Run_Game.py


def run_game_with_ML(display, clock, weights):
    max_score = 0
    avg_score = 0
    test_games = 1
    score1 = 0
    steps_per_game = 2500
    score2 = 0

    for _ in range(test_games):
        # Initialising the game by setting snake position,apple position etc.
        snake_start, snake_position, apple_position, score = starting_positions()

        count_same_direction = 0
        prev_direction = 0

        for _ in range(steps_per_game): #running game for 2500 steps
            # Get current snake direction and blocked directions for snake.
            current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(snake_position)
            angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(
                snake_position, apple_position)
            predictions = []
            # Predict direction(Left,right,forward) based on output from neural network.
            predicted_direction = np.argmax(np.array(forward_propagation(np.array(
                [is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0],
                 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1],
                 snake_direction_vector_normalized[1]]).reshape(-1, 7), weights))) - 1
            # Increment counter if predicted direction is same as past direction.
            if predicted_direction == prev_direction:
                count_same_direction += 1
            else:
                count_same_direction = 0
                prev_direction = predicted_direction
            # Based on predicted direction, calculate snake direction.
            new_direction = np.array(snake_position[0]) - np.array(snake_position[1])
            if predicted_direction == -1:
                new_direction = np.array([new_direction[1], -new_direction[0]])
            if predicted_direction == 1:
                new_direction = np.array([-new_direction[1], new_direction[0]])

            button_direction = generate_button_direction(new_direction)
            # Evaluate the next step of snake.
            next_step = snake_position[0] + current_direction_vector
            # Check if snake collides with a boundary or with itself.
            if collision_with_boundaries(snake_position[0]) == 1 or collision_with_self(next_step.tolist(),
                                                                                        snake_position) == 1:
                score1 -= 150 # Give a negative score to mention that its a wrong move.
                break

            else:
                score1 += 0
            # Play game with current parameters
            snake_position, apple_position, score = play_game(snake_start, snake_position, apple_position,
                                                              button_direction, score, display, clock)

            if score > max_score:
                max_score = score
            # Checking condition for snake movement in loop.
            if count_same_direction > 8 and predicted_direction != 0:
                score2 -= 1 # Give a negative score to mention that its a wrong move. 
            else:
                score2 += 2 # Else give a positive score

    # High weightage is given for maximum score of snake in its 2500 steps.
    # return fitness value
    return score1 + score2 + max_score * 5000

# https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm/blob/main/Genetic_Algorithm.py


from Run_Game import *
from random import choice, randint, uniform
import numpy as np

# TODO fix to class & remove circular dependency
def cal_pop_fitness(pop, filename):
    # calculating the fitness value by playing a game with the given weights in chromosome
    fitness = []
    for i in range(pop.shape[0]):
        fit = run_game_with_ML(display, clock, pop[i])
        
        file1 = open(filename, "a+")
        file1.write("fitness value of chromosome " + str(i) + " :  " + str(fit) + "\n")
        file1.close()
        # print('fitness value of chromosome '+ str(i) +' :  ', fit)
        fitness.append(fit)
    return np.array(fitness)

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999
    return parents

def crossover(parents, offspring_size):
    # creating children for next generation 
    offspring = np.empty(offspring_size)
    
    for k in range(offspring_size[0]): 
  
        while True:
            parent1_idx = randint(0, parents.shape[0] - 1)
            parent2_idx = randint(0, parents.shape[0] - 1)
            # produce offspring from two parents if they are different
            if parent1_idx != parent2_idx:
                for j in range(offspring_size[1]):
                    if uniform(0, 1) < 0.5:
                        offspring[k, j] = parents[parent1_idx, j]
                    else:
                        offspring[k, j] = parents[parent2_idx, j]
                break
    return offspring

# two results with 0.1 and 0.01
def mutation(offspring_crossover, mutation_intensity):
    # mutating the offsprings generated from crossover to maintain variation in the population
    for idx in range(offspring_crossover.shape[0]):
        for i in range(offspring_crossover.shape[1]):
            if uniform(0, 1) < mutation_intensity:
                random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
                offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
    return offspring_crossover

# flat curve result
# def mutation(offspring_crossover, mutation_intensity):
#     # mutating the offsprings generated from crossover to maintain variation in the population
#     num_genes_mutate = (int)(mutation_intensity*offspring_crossover.shape[1]/100)
#     for idx in range(offspring_crossover.shape[0]):
#         for _ in range(num_genes_mutate):
#             i = randint(0, offspring_crossover.shape[1]-1)
#             random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
#             offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
#     return offspring_crossover