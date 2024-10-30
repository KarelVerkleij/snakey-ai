from snake.snake_bot import BotApp
from snake.utils import overrides
from snake_ml.feed_foreward_neural_network import nn_snake
from numpy.random import randint, rand
from random import randint, uniform
from math import atan2, pi

import numpy as np
import pygame

# sourced from https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm


# TODO combine into one class
class MLBotApp(BotApp):

    def __init__(self, bot_study_name='', log_file_path='../logs/bot_ml/test_log.log', weights=None):
        super().__init__()

        self.snake_speed = 100

        # TODO revise if this needs to be here
        # new_population is to be iterated over etc. probably should be in study with weights being given on initial run
        self.neural_network_snake = nn_snake()
        self.num_weights = self.neural_network_snake.n_x*self.neural_network_snake.n_h + self.neural_network_snake.n_h*self.neural_network_snake.n_h2 + self.neural_network_snake.n_h2*self.neural_network_snake.n_y
        self.sol_per_pop = 50
        self.pop_size = (self.sol_per_pop, self.num_weights)
        self.new_population = np.random.choice(np.arange(-1, 1, step = 0.01), size = self.pop_size, replace=True)
        self.weights = self.new_population[0]

        # nn set-up 
        self.count_same_direction = 0
        self.prev_direction = 0
        self.score1 = 0
        self.score2 = 0
        self.max_score = 0 

    @overrides(BotApp) 
    def bot_input(self):

        chosen_direction = self.direction_picker()

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

    @overrides(BotApp)
    def on_loop(self):
        
        self.game_loop()

        self.bot_next_move = self.bot_input()
        self.evaluate_choice_nn()
        pygame.event.post(self.bot_next_move)
        

    def evaluate_choice_nn(self):
        # Evaluate the next step of snake.
        self.next_snake_position = self.snake_position + self.new_direction
        
        # Check if snake collides with a boundary or with itself.
        if self.is_direction_blocked(self.next_snake_position):
            self.score1 -= 150 # Give a negative score to mention that its a wrong move.
        
        # check snake score vs max score so far
        if self.score > self.max_score:
            self.max_score = self.score
        
        # Checking condition for snake movement in loop.
        if self.count_same_direction > 8 and self.predicted_direction != 0:
            self.score2 -= 1 # Give a negative score to mention that its a wrong move. 
        else:
            self.score2 += 2 # Else give a positive score

    def direction_picker(self):

        self.blocked_directions()
        self.calculate_angle_with_fruit()
        
        self.predictions = []
        
        # Predict direction(Left,right,forward) based on output from neural network.
        self.predicted_direction = np.argmax(np.array(self.neural_network_snake.forward_propagation(X = np.array([
                                                                                        self.is_left_blocked, 
                                                                                        self.is_front_blocked, 
                                                                                        self.is_right_blocked, 
                                                                                        self.apple_direction_vector_normalized[0],
                                                                                        self.snake_direction_vector_normalized[0], 
                                                                                        self.apple_direction_vector_normalized[1],
                                                                                        self.snake_direction_vector_normalized[1]
                                                                                    ]).reshape(-1, 7), 
                                                                                    individual = self.weights))) - 1
        
        # Increment counter if predicted direction is same as past direction. 
        if self.predicted_direction == self.prev_direction:
            self.count_same_direction += 1
        else:
            self.count_same_direction = 0
            self.prev_direction = self.predicted_direction
        
        # Based on predicted direction, calculate snake direction.
        if self.predicted_direction == -1:
            self.new_direction = np.array([self.current_direction_vector[1], -self.current_direction_vector[0]])
        if self.predicted_direction == 1:
            self.new_direction = np.array([-self.current_direction_vector[1], self.current_direction_vector[0]])

        self.convert_nn_output_into_move()
        

    def convert_nn_output_into_move(self):
        
        self.change_in_x = self.new_direction[0]/10
        self.change_in_y = self.new_direction[1]/10

        # convert into commands 
        if self.change_in_x == -1 and change_in_y == 0:
            next_move = 'LEFT'
        elif self.change_in_x == 1 and self.change_in_y == 0:
            next_move = 'RIGHT'
        elif self.change_in_x == 0 and self.change_in_y == 1:
            next_move = 'DOWN'
        elif self.change_in_x == 0 and self.change_in_y == -1:
            next_move = 'UP'
        else:
            print("something went wrong - illegal move")

        return pygame.event.Event(pygame.KEYDOWN, key=self.dict_of_direction_and_events[next_move])

    def blocked_directions(self):
        
        self.calculate_direction_vector_calculation() # outputs self.current_direction_vector

        self.left_direction_vector = np.array([self.current_direction_vector[1], -self.current_direction_vector[0]])
        self.right_direction_vector = np.array([-self.current_direction_vector[1], self.current_direction_vector[0]])

        self.is_front_blocked = self.is_direction_blocked(self.current_direction_vector)
        self.is_right_blocked = self.is_direction_blocked(self.right_direction_vector)
        self.is_left_blocked = self.is_direction_blocked(self.left_direction_vector)
    
    def calculate_direction_vector_calculation(self):
        
        if self.direction == 'LEFT':
            self.current_direction_vector = np.array([-10,0])
        elif self.direction == 'RIGHT':
            self.current_direction_vector = np.array([10,0])
        elif self.direction == 'UP':
            self.current_direction_vector = np.array([0,10])
        elif self.direction == 'DOWN':
            self.current_direction_vector = np.array([0,-10])

    def is_direction_blocked(self, direction_vector):
        self.next_step = self.snake_position + direction_vector

        if self.boundary_collision(self.next_step) or (self.next_step.tolist() in self.snake_body):
            return 1
        return 0
    
    def calculate_angle_with_fruit(self):

        # to return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized


        # self.fruit_position = apple
        # self.snake_position = snake_position[0]

        self.apple_direction_vector = np.array(self.fruit_position) - np.array(self.snake_position)
        self.snake_direction_vector = self.current_direction_vector

        self.norm_of_apple_direction_vector = np.linalg.norm(self.apple_direction_vector)
        self.norm_of_snake_direction_vector = np.linalg.norm(self.snake_direction_vector)
        
        if self.norm_of_apple_direction_vector == 0:
            self.norm_of_apple_direction_vector = 10
        if self.norm_of_snake_direction_vector == 0:
            self.norm_of_snake_direction_vector = 10

        self.apple_direction_vector_normalized = self.apple_direction_vector / self.norm_of_apple_direction_vector
        self.snake_direction_vector_normalized = self.snake_direction_vector / self.norm_of_snake_direction_vector
        self.angle = atan2(
            self.apple_direction_vector_normalized[1] * self.snake_direction_vector_normalized[0] - self.apple_direction_vector_normalized[
                0] * self.snake_direction_vector_normalized[1],
            self.apple_direction_vector_normalized[1] * self.snake_direction_vector_normalized[1] + self.apple_direction_vector_normalized[
                0] * self.snake_direction_vector_normalized[0]) / pi
        

# https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm/blob/main/Run_Game.py


if __name__ == '__main__':

    theApp = MLBotApp(bot_study_name = '_1')
    theApp.on_execute()






# TODO move to study?

# def run_game_with_ML(display, clock, weights):
#     max_score = 0
#     avg_score = 0
#     test_games = 1
#     score1 = 0
#     steps_per_game = 2500
#     score2 = 0

#     MLBotApp 

#     # High weightage is given for maximum score of snake in its 2500 steps.
#     # return fitness value
#     return score1 + score2 + max_score * 5000







# https://github.com/ygutgutia/Snake-Game-Genetic-Algorithm/blob/main/Genetic_Algorithm.py




# # TODO fix to class & remove circular dependency
# def cal_pop_fitness(pop, filename):
#     # calculating the fitness value by playing a game with the given weights in chromosome
#     fitness = []
#     for i in range(pop.shape[0]):
#         fit = run_game_with_ML(display, clock, pop[i])
        
#         file1 = open(filename, "a+")
#         file1.write("fitness value of chromosome " + str(i) + " :  " + str(fit) + "\n")
#         file1.close()
#         # print('fitness value of chromosome '+ str(i) +' :  ', fit)
#         fitness.append(fit)
#     return np.array(fitness)

# def select_mating_pool(pop, fitness, num_parents):
#     # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
#     parents = np.empty((num_parents, pop.shape[1]))
#     for parent_num in range(num_parents):
#         max_fitness_idx = np.where(fitness == np.max(fitness))
#         max_fitness_idx = max_fitness_idx[0][0]
#         parents[parent_num, :] = pop[max_fitness_idx, :]
#         fitness[max_fitness_idx] = -99999999
#     return parents

# def crossover(parents, offspring_size):
#     # creating children for next generation 
#     offspring = np.empty(offspring_size)
    
#     for k in range(offspring_size[0]): 
  
#         while True:
#             parent1_idx = randint(0, parents.shape[0] - 1)
#             parent2_idx = randint(0, parents.shape[0] - 1)
#             # produce offspring from two parents if they are different
#             if parent1_idx != parent2_idx:
#                 for j in range(offspring_size[1]):
#                     if uniform(0, 1) < 0.5:
#                         offspring[k, j] = parents[parent1_idx, j]
#                     else:
#                         offspring[k, j] = parents[parent2_idx, j]
#                 break
#     return offspring

# # two results with 0.1 and 0.01
# def mutation(offspring_crossover, mutation_intensity):
#     # mutating the offsprings generated from crossover to maintain variation in the population
#     for idx in range(offspring_crossover.shape[0]):
#         for i in range(offspring_crossover.shape[1]):
#             if uniform(0, 1) < mutation_intensity:
#                 random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
#                 offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
#     return offspring_crossover

# # flat curve result
# # def mutation(offspring_crossover, mutation_intensity):
# #     # mutating the offsprings generated from crossover to maintain variation in the population
# #     num_genes_mutate = (int)(mutation_intensity*offspring_crossover.shape[1]/100)
# #     for idx in range(offspring_crossover.shape[0]):
# #         for _ in range(num_genes_mutate):
# #             i = randint(0, offspring_crossover.shape[1]-1)
# #             random_value = np.random.choice(np.arange(-1, 1, step = 0.001), size = (1), replace = False)
# #             offspring_crossover[idx, i] = offspring_crossover[idx, i] + random_value
# #     return offspring_crossover

# # /¡