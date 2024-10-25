"""
sourced from http://pygametutorials.wikidot.com/tutorials-basic
sourced from https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/ 
"""

import pygame

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    # initializes all pygame modules, then creates window 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    # check if game was quit
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    # do nothing
    def on_loop(self):
        pass

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
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

if __name__ == '__main__':
    theApp = App()
    theApp.on_execute()

