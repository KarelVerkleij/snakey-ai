#
# sourced from http://pygametutorials.wikidot.com/tutorials-basic
# sourced from https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/ 
#

import pygame
import time 
import random
import logging 

class App:
    def __init__(self, _logging=False):
        self._running = True
        self._display_surf = None
        
        # logging configs
        self._logging = _logging
        self.cycle_n = 0
        if self._logging:
            pass
            logging.root.setLevel(logging.NOTSET)
            self.logger_module = logging.getLogger(__name__)
            # self.logger_module.info("logging enabled")

        # basic config speed
        self.snake_speed = 15
        
        # defining snake default position 
        self.snake_position = [100, 50]

        # defining first 4 blocks of snake
        self.snake_body = [  [100, 50],
                             [90, 50],
                             [80, 50],
                             [70, 50]
                          ]
        
        # score
        self.score = 0

        # setting default snake direction towards right
        self.direction = 'RIGHT'
        self.change_to = self.direction

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
        pygame.init()

        # Initialise game window
        pygame.display.set_caption('GeeksforGeeks Snakes')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))
        
        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()

        # fruit position 
        self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10,
                               random.randrange(1, (self.window_y//10)) * 10]
        self.fruit_spawn = True

        self._running = True

    # check if game was quit
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # do nothing
    def on_loop(self):
        self.game_loop()
        if self._logging:
            self.logger()

    # do nothing
    def on_render(self):
        pass
    
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
        
        # after 2 seconds we will quit the 
        # program
        time.sleep(2)
        
        # deactivating pygame library
        pygame.quit()

        quit()

    def game_loop(self):

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
            self.fruit_spawn = False
        else:
            self.snake_body.pop()
            
        if not self.fruit_spawn:
            self.fruit_position = [random.randrange(1, (self.window_x//10)) * 10, 
                                   random.randrange(1, (self.window_y//10)) * 10]            
            self.fruit_spawn = True
            
        
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

    def logger(self):
        self.logger_module.info({"cycle": self.cycle_n, 
                                "current_snake_position_x": self.snake_position[0],
                                "current_snake_position_y": self.snake_position[1],
                                "current_direction": self.direction, 
                                "current_score":  self.score,
                                "fruit_position_x": self.fruit_position[0], 
                                "fruit_position_y": self.fruit_position[1]
                            })
        
        # iterate cycle
        self.cycle_n = self.cycle_n + 1


if __name__ == '__main__':
    logging.basicConfig(
                        # filename='../logs/test_log.log',
                        # filemode='w',
                        # force=True,
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.NOTSET)

    theApp = App(_logging=True)
    theApp.on_execute()


