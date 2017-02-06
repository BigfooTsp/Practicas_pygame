import pygame
from pygame.locals import *
from gamemanager.states import  gamestate
from utilidades.imagen import *

from mapa import *
from personaje import *
from mundo import *

import mapa2state
 
class Mapa1State(gamestate.GameState):
 
 
    def __init__(self, parent):

        self.parent = parent

        self._mapa = Mapa('mapa1.tmx')
        
        self.ordenador = Personaje('Ordenador1','data/imagenes/policia.png')
        self.ordenador.actualizar_posicion((5,7))                

        self.parent.jugador.actualizar_posicion((6,3))
        self.parent.jugador.cambiar_direccion(Personaje.ESTE)

        self._personajes = [self.parent.jugador, self.ordenador]

        self._mundo = Mundo(self._mapa, self._personajes)        


    def start(self):
        print "GameState Mapa1 Started"
 
    def cleanUp(self):
        print "GameState Mapa1 Cleaned"
        pass
 
    def pause(self):
        print "GameState Mapa1 Paused"
        pass
 
    def resume(self):
        print "GameState Mapa1 Resumed"
        pass

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    self.parent.popState()
                elif event.key == pygame.K_UP :
                    self._mundo.mover_jugador(Personaje.NORTE)
                elif event.key == pygame.K_DOWN :
                    self._mundo.mover_jugador(Personaje.SUR)
                elif event.key == pygame.K_RIGHT :
                    self._mundo.mover_jugador(Personaje.ESTE)
                elif event.key == pygame.K_LEFT :
                    self._mundo.mover_jugador(Personaje.OESTE)

    def update(self):
        self._mundo.update()
        # Si el jugador sale por la puerta cargamos el segundo mapa.
        if (self.parent.jugador.obtener_posicion() == (6,0)):
            self.parent.pushState(mapa2state.Mapa2State(self.parent))
 
    def draw(self):
        self.parent.screen.blit(self.parent.background, (0,0))
        self._mundo.dibujar(self.parent.screen)        

                
        
