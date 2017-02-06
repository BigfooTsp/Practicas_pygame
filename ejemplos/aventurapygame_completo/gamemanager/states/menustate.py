import pygame
from pygame.locals import *
from gamemanager.states import  gamestate
import opcionesstate
import mapa1state
 
class MenuState(gamestate.GameState):
 
 
   def __init__(self, parent):
       self.parent = parent
       self.background = pygame.Surface(self.parent.screen.get_size())
       self.background = self.background.convert()
       self.background.fill((255, 0, 0))
       letra = pygame.font.Font(None, 14)
       self.escribir = letra.render(u"Pulsa \"J\" para JUGAR",
               1, (250,250,250))
 
   def start(self):
       print "GameState Menu Started"
 
   def cleanUp(self):
       print "GameState Menu Cleaned"
       pass
 
   def pause(self):
       print "GameState Menu Paused"
       pass
 
   def resume(self):
       print "GameState Menu Resumed"
       pass
 
   def handleEvents(self, events):
       for event in events:
           if event.type == pygame.KEYDOWN :
               if event.key == pygame.K_ESCAPE :
                   self.parent.quit()
               elif  event.key == pygame.K_o:
                   self.parent.pushState(opcionesstate.OpcionesState(self.parent))
               elif  event.key == pygame.K_j:
                   self.parent.pushState(mapa1state.Mapa1State(self.parent))
 
   def update(self):
       pass
 
   def draw(self):
       self.parent.screen.blit(self.background, (0,0))
       self.parent.screen.blit(self.escribir, (10,10))
