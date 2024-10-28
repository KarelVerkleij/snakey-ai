#
# sourced from http://pygametutorials.wikidot.com/tutorials-basic
# sourced from https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/ 
#

import pygame
import time 
import random
import logging 
import os
import sys

class App:
    def __init__(self, 
                 _logging=True,
                 log_file_path = '../logs/test_log.log',
                 bot_study_name = ''
                 ):
    
        self._running = True
        self._display_surf = None
        
        # logging configs
        self._logging = _logging
        self.logging_config = "COMMANDLINE"
        self.log_file_path = log_file_path
        self.cycle_n = 0
        self.default_bot_name = 'HUMAN'
        self.bot_name =  self.default_bot_name + bot_study_name 

        # basic config to start game speed
        self.snake_speed = 15
        self.snake_position = [100, 50]
        self.score = 0
        self.game_over_check = False
        
        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.change_to = self.direction

        # defining first 4 blocks of snake
        self.snake_body = [self.snake_position]

        # window size
        self.size = self.window_x, self.window_y = 720, 480

        # colors
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)
        

    # initializes all pygame modules, then creates window 
    def on_init(self):
        
        if self._logging:
            self.logger_init()
            
        pygame.init()

        # Initialise game window
        pygame.display.set_caption('Snakey-ai')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

        # fruit position 
        self.generate_fruit()

        self._running = True

    # check if game was quit
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # do nothing
    def on_loop(self):
        self.game_loop()

    # do nothing
    def on_render(self):
        pass

    # generates fruit
    def generate_fruit(self):

        while(True):
            proposed_fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
                                       random.randrange(1, (self.window_y//10)) * 10]

            if self.empty_space(proposed_fruit_position):
                break

        self.fruit_position = proposed_fruit_position


    # check if x,y is not occupied by snake body
    def empty_space(self, fruit_position):

        if fruit_position not in self.snake_body:
            return True
        else:
            return False
    
    # quits all pygame modules
    def on_cleanup(self):
        pygame.quit()
    
    # initializes pygame & enters main loop where events are checked, exectued in a continuous cycle
    def on_execute(self):
        if self.on_init() == False:
            self._running = False 

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


    def show_score(self, choice, color, font, size):
        
        pygame.font.init()

        # creating font object score_font 
        score_font = pygame.font.SysFont(font, size)
        
        # create the display surface object
        # score_surface
        score_surface = score_font.render('Score : ' + str(self.score), True, color)
        
        # create a rectangular object for the 
        # text surface object
        score_rect = score_surface.get_rect()
        
        # displaying text
        self.game_window.blit(score_surface, score_rect)

    # game over function
    def game_over(self):
    
        self.game_over_check = True

        pygame.font.init()

        # log final loop
        self.logger()

        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 50)
        
        # creating a text surface on which text 
        # will be drawn
        game_over_surface = my_font.render('Your Score is : ' + str(self.score), True, self.red)
        
        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()
        
        # setting position of the text
        game_over_rect.midtop = (self.window_x/2, self.window_y/4)
        
        # blit will draw the text on screen
        self.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        self.print_results()
        
        self.game_exit()

    def print_results(self):
        bot_name = self.bot_name
        final_n_cylce = self.cycle_n
        final_score = self.score
        print(f"bot: {bot_name}, max_cycle: {final_n_cylce}, final_score {final_score}")


    def game_exit(self):
        # deactivating pygame library

        pygame.quit()
        sys.exit()
        
        time.sleep(1)

    def game_loop(self):

        # logging
        if self._logging:
            self.logger()

        # If two keys pressed simultaneously 
        # we don't want snake to move into two directions
        # simultaneously
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Moving the snake
        if self.direction == 'UP':
            self.snake_position[1] -= 10
        if self.direction == 'DOWN':
            self.snake_position[1] += 10
        if self.direction == 'LEFT':
            self.snake_position[0] -= 10
        if self.direction == 'RIGHT':
            self.snake_position[0] += 10


        # Snake body growing mechanism 
        # if fruits and snakes collide then scores will be 
        # incremented by 1
        self.snake_body.insert(0, list(self.snake_position))
        if self.snake_position[0] == self.fruit_position[0] and self.snake_position[1] == self.fruit_position[1]:
            self.score += 1
            self.generate_fruit()
        else:
            self.snake_body.pop()
            
        self.game_window.fill(self.black)
        
        for pos in self.snake_body:
            pygame.draw.rect(self.game_window, self.green, pygame.Rect(
                pos[0], pos[1], 10, 10)
        )
            
        pygame.draw.rect(self.game_window, self.white, pygame.Rect(
                self.fruit_position[0], 
                self.fruit_position[1], 10, 10)
        )

        # Game Over conditions
        if self.snake_position[0] < 0 or self.snake_position[0] > self.window_x-10:
            self.game_over()
        if self.snake_position[1] < 0 or self.snake_position[1] > self.window_y-10:
            self.game_over()
            
        
        # Touching the snake body
        for block in self.snake_body[1:]:
            if self.snake_position[0] == block[0] and self.snake_position[1] == block[1]:
                self.game_over()
        
        # displaying score continuously
        self.show_score(1, self.white, 'times new roman', 20)
        
        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        self.fps.tick(self.snake_speed)

    def logger_init(self):
        
        if self.logging_config == "COMMANDLINE":
            logging.basicConfig(
                                # filename=filename,
                                # filemode='a',
                                # force=True,
                                format='%(message)s,',
                                datefmt='%H:%M:%S',
                                level=logging.NOTSET)
        elif self.logging_config == "LOGFILE":
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.log_file_path)
            logging.basicConfig(
                                filename=filename,
                                filemode='a',
                                force=True,
                                format='%(message)s,',
                                datefmt='%H:%M:%S',
                                level=logging.NOTSET)
            
        logging.root.setLevel(logging.NOTSET)
        self.logger_module = logging.getLogger(__name__)
        # self.logger_module.info("logging enabled")

    def logger(self):
        # logger path
        self.logger_module.info(f"bot: {self.bot_name}, cycle: {self.cycle_n}, current_snake_position_x: {self.snake_position[0]}, current_snake_position_y: {self.snake_position[1]}, current_direction: {self.direction}, current_score:  {self.score}, fruit_position_x: {self.fruit_position[0]}, fruit_position_y: {self.fruit_position[1]}"
                               )

        # iterate cycle
        self.cycle_n = self.cycle_n + 1


if __name__ == '__main__':
    theApp = App(_logging=True)
    theApp.on_execute()


