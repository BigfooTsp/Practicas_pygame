import pygame
from pygame.locals import *
from gamemanager.states import  gamestate
from utilidades.imagen import *

from mapa import *
from personaje import *
from mundo import *
 
class Mapa2State(gamestate.GameState):
 
 
    def __init__(self, parent):

        self.parent = parent
        
        self._mapa = Mapa('mapa2.tmx')       

        self.enemigo = Personaje('Enemigo1','data/imagenes/enemigo.png')
        self.enemigo.actualizar_posicion((4,4))                

        self.parent.jugador.actualizar_posicion((6,8))
        self.parent.jugador.cambiar_direccion(Personaje.OESTE)

        self._personajes = [self.parent.jugador, self.enemigo]

        self._mundo = Mundo(self._mapa, self._personajes)        


    def start(self):
        print "GameState Mapa2 Started"
 
    def cleanUp(self):
        print "GameState Mapa2 Cleaned"
        pass
 
    def pause(self):
        print "GameState Mapa2 Paused"
        pass
 
    def resume(self):
        print "GameState Mapa2 Resumed"
        pass

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_UP :
                    self._mundo.mover_jugador(Personaje.NORTE)
                elif event.key == pygame.K_DOWN :
                    self._mundo.mover_jugador(Personaje.SUR)
                elif event.key == pygame.K_RIGHT :
                    self._mundo.mover_jugador(Personaje.ESTE)
                elif event.key == pygame.K_LEFT :
                    self._mundo.mover_jugador(Personaje.OESTE)

    def update(self):
        self._mundo.update()
        if (self.parent.jugador.obtener_posicion() == (6,9)):
            self.parent.jugador.actualizar_posicion((6,1))
            self.parent.popState()
       
 
    def draw(self):
        self.parent.screen.blit(self.parent.background, (0,0))
        self._mundo.dibujar(self.parent.screen)        

                
        
