from snake.snake_bot import BotApp
from snake.utils import overrides

import pygame
from random import choice

class LogicGreedyBotApp(BotApp):

    def __init__(self, bot_study_name='', log_file_path='../logs/bot_logic_greedy/test_log.log'):
        super().__init__()

        self.snake_speed = 100

        ## default configs for bot
        self.default_bot_name = 'BOT_GREEDY_LOGIC'
        self.bot_name = self.default_bot_name + bot_study_name
        
        self.log_file_path='../logs/bot_logic_greedy/test_log.log'
        self.logging_config="LOGFILE"

        self.list_of_opposite_directions = [[pygame.K_RIGHT, 'LEFT'],
                                            [pygame.K_LEFT, 'RIGHT'],
                                            [pygame.K_UP, 'DOWN'],
                                            [pygame.K_DOWN, 'UP']]

    @overrides(BotApp) 
    def bot_input(self):

        chosen_direction = self.direction_picker()

        return pygame.event.Event(pygame.KEYDOWN, key=chosen_direction)

    def direction_picker(self):
        
        list_of_proposed_direction = self.direction_calculator()
        proposed_direction = self.direction_handler(list_of_proposed_direction)
        return proposed_direction

    # greedy
    # follows the fastest path to the goal with no regard of self
    def direction_calculator(self):
        
        # list_of_proposed_directions
        list_of_proposed_directions = []

        self.calculate_future_position_snake()

        # calculate between fruit and snake
        self.distance_fruit_snake_x = self.fruit_position[0] - self.future_snake_position[0]
        self.distance_fruit_snake_y = self.fruit_position[1] - self.snake_position[1]

        if self.distance_fruit_snake_x > 0:
            list_of_proposed_directions.append(pygame.K_RIGHT)
        elif self.distance_fruit_snake_x < 0:
            list_of_proposed_directions.append(pygame.K_LEFT)

        if self.distance_fruit_snake_y < 0:
            list_of_proposed_directions.append(pygame.K_UP)
        elif self.distance_fruit_snake_y > 0:
            list_of_proposed_directions.append(pygame.K_DOWN)     

        while len(list_of_proposed_directions) < 2:
            list_of_directions = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT] 
            random_direction = choice(list_of_directions)
            if random_direction not in list_of_proposed_directions:  
                list_of_proposed_directions.append(random_direction)

        return list_of_proposed_directions

    def direction_handler(self, list_of_proposed_directions):
        
        if [list_of_proposed_directions[0], self.direction] in self.list_of_opposite_directions:
            return list_of_proposed_directions[1]
        else:
            return list_of_proposed_directions[0]
        
        
    def calculate_future_position_snake(self):

        self.future_snake_position = self.snake_position.copy()

        # Moving the snake
        if self.direction == 'UP':
            self.future_snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.future_snake_position[1] += 10
        if self.direction == 'LEFT':
            self.future_snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.future_snake_position[0] += 10

if __name__ == '__main__':

    theApp = LogicGreedyBotApp(bot_study_name = '_1')
    theApp.on_execute()
