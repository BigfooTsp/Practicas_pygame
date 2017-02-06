import sys
import os

import pygame
from pygame.locals import *
from singleton import *

from personaje import *

class GameManager(object):

    __metaclass__ = Singleton
    
    def __init__(self, titulo, size=(320, 200), fullscreen=False):
        print "Inicilizado el GameManager"
        self.states = []
        self.running = True
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init();
        self.screen = pygame.display.set_mode(size)
        
        pygame.display.set_caption(titulo)

        self.jugador = Personaje('Jugador','data/imagenes/jugador.png')

        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))        
        
        
    def cleanUp (self):
        print "cleanUp del GameManager"
        while len(self.states) > 0:
            state = self.states.pop()
            state.cleanUp()

        sys.exit(0)

    def changeState (self, gameState):
        print "Cambio de estado"
        if len(self.states) > 0:
            state = self.states.pop()
            state.cleanUp()
        
        self.states.append(gameState)
        self.states[-1].start()

    def pushState(self, gameState):
        if len(self.states) > 0:
            self.states[-1].pause()

        self.states.append(gameState)
        self.states[-1].start()

    def popState(self):
        if len(self.states) > 0:
            state = self.states.pop()
            state.cleanUp()

        if len(self.states) > 0:
            self.states[-1].resume()

    def handleEvents(self, events):
        self.states[-1].handleEvents(events)

    def update(self):
        self.states[-1].update()

    def draw(self):
        self.states[-1].draw()
        pygame.display.flip()

    def quit(self):
        print "Quit"
        self.running = False
