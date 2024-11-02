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

    def __init__(self, 
                 bot_study_name='', 
                 log_file_path='../logs/bot_ml/test_log.log', 
                 weights=None,
                 neural_network_snake=nn_snake(),
                 steps_per_game=2500,
                 bot_name='BOT_ML'
                 ):
        super().__init__()

        self.bot_name = bot_name
        self.snake_speed = 100
        self.max_count_same_direction = 0

        self.predictions = []

        # TODO revise if this needs to be here
        # new_population is to be iterated over etc. probably should be in study with weights being given on initial run
        self.neural_network_snake = neural_network_snake
        self.log_file_path = log_file_path
        
        if type(weights) == type(None):
            self.num_weights = self.neural_network_snake.n_x*self.neural_network_snake.n_h + self.neural_network_snake.n_h*self.neural_network_snake.n_h2 + self.neural_network_snake.n_h2*self.neural_network_snake.n_y
            self.sol_per_pop = 50
            self.pop_size = (self.sol_per_pop, self.num_weights)
            self.new_population = np.random.choice(np.arange(-1, 1, step = 0.01), size = self.pop_size, replace=True)
            self.weights = self.new_population[0]
        else:
            self.weights = weights

        self.steps_per_game = steps_per_game

        # nn set-up 
        self.count_same_direction = 0
        self.prev_direction = 0
        self.score1 = 0
        self.score2 = 0
        self.max_score = 0 

    @overrides(BotApp) 
    # initializes pygame & enters main loop where events are checked, exectued in a continuous cycle
    def on_execute(self, conn=None):
        if self.on_init() == False:
            self._running = False 

        if conn != None:
            self.conn = conn

        while( self._running ):
            # handling key events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'

            self.on_loop()
            self.on_render()



      

        self.on_cleanup()

    
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

    @overrides(BotApp)
    def print_results(self):
        bot_name = self.bot_name
        final_n_cylce = self.cycle_n
        final_score = self.score
        if self.conn != None:        
            self.collected_data = {
                "score1" : self.score1,
                "score2" : self.score2,
                "max_score" : self.max_score,
                "max_same_direction" : self.max_count_same_direction,
                "n_cycles" : self.cycle_n,
                "predictions" : self.predictions

            } 
            self.conn.send(self.collected_data)
        
        print(f"bot: {bot_name}, max_cycle: {final_n_cylce}, final_score {final_score}, score_1: {self.score1}, score_2: {self.score2}, max_score: {self.max_score}, ")

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
        self.predictions.append(self.predicted_direction)
        
        # Increment counter if predicted direction is same as past direction. 
        if self.predicted_direction == self.prev_direction:
            self.count_same_direction += 1
            if self.count_same_direction > self.max_count_same_direction:
                    self.max_count_same_direction = self.count_same_direction
        else:
            self.count_same_direction = 0
            self.prev_direction = self.predicted_direction
        
        # Based on predicted direction, calculate snake direction.
        if self.predicted_direction == -1:
            self.new_direction = np.array([self.current_direction_vector[1], -self.current_direction_vector[0]])
        if self.predicted_direction == 1:
            self.new_direction = np.array([-self.current_direction_vector[1], self.current_direction_vector[0]])
        else:
            self.new_direction = np.array(self.current_direction_vector)

        return self.convert_nn_output_into_move()
        

    def convert_nn_output_into_move(self):
        
        self.change_in_x = self.new_direction[0]/10
        self.change_in_y = self.new_direction[1]/10

        # convert into commands 
        if self.change_in_x == -1 and self.change_in_y == 0:
            next_move = 'LEFT'
        elif self.change_in_x == 1 and self.change_in_y == 0:
            next_move = 'RIGHT'
        elif self.change_in_x == 0 and self.change_in_y == 1:
            next_move = 'DOWN'
        elif self.change_in_x == 0 and self.change_in_y == -1:
            next_move = 'UP'
        else:
            print("something went wrong - illegal move")

        return self.dict_of_direction_and_events[next_move]

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


# simple running logic

if __name__ == '__main__':

    theApp = MLBotApp(bot_study_name = '_1')
    theApp.on_execute()
    print(theApp.max_score)


