import pygame
from pygame.locals import *
from gamemanager.states import  gamestate
from utilidades.imagen import *
from personajes.personajes import *

from mapa import *
from personaje import *
from mundo import *
 
class Mapa2State(gamestate.GameState):
 
 
    def __init__(self, parent):

        self.parent = parent
        
        self._mapa = Mapa('mapa2.tmx')       

        self._preso1 = NPC_Preso_1()
        self._preso1.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((3, 0),self._mapa.CENTER))                

        self._preso2 = NPC_Preso_2()
        self._preso2.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((8, 4),self._mapa.CENTER))                
        self._preso2.actualizar_direccion(Personaje.NORTE)

        self._jugador = self.parent.jugador
        
        self._jugador.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((6, 8),self._mapa.CENTER))
        self._jugador.actualizar_direccion(Personaje.OESTE)
        

        self._personajes = [self._jugador, self._preso1, self._preso2]

        self._mundo = Mundo(self._mapa, self._personajes)        

    def start(self):
        print "GameState Mapa2 Started"
        self._jugador.parar()
 
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
        teclas_pulsadas = pygame.key.get_pressed()
        
        if teclas_pulsadas[K_UP]:
            self._mundo.mover_jugador(Personaje.NORTE)
        elif teclas_pulsadas[K_DOWN]:
            self._mundo.mover_jugador(Personaje.SUR)
        elif teclas_pulsadas[K_RIGHT]:
            self._mundo.mover_jugador(Personaje.ESTE)
        elif teclas_pulsadas[K_LEFT]:
            self._mundo.mover_jugador(Personaje.OESTE)

    def update(self):
        self._mundo.update()
        if (self._mundo.esta_personaje_en_posicion(self._jugador, (6, 9))):
            self._jugador.actualizar_posicion(self._mapa.obtener_centro_celda(6, 1))
            self._jugador.parar()
            self.parent.popState()
       
 
    def draw(self):
        self.parent.screen.blit(self.parent.background, (0, 0))
        self._mundo.dibujar(self.parent.screen)        

                
        
