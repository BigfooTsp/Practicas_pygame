# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from gamemanager.states.gamestate import GameState
#from utilidades.imagen import *
from personajes.personajes import *

from mapa import Mapa
from personaje import Personaje
from mundo import Mundo
from conversacionstate import ConversacionState
from objeto_mundo import Objeto_Vacio, Objeto_Mundo

from inventario import Inventario

import mapa2state
 
class Mapa1State(GameState):
 
    def __init__(self, parent):

        self.parent = parent

        self._mapa = Mapa('mapa1.tmx')
        
        self._jugador = self.parent.jugador
        
        self.npc_policia = NPC_Policia_1()
        self.npc_policia.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((4, 0),self._mapa.CENTER))  
        self.npc_policia.actualizar_direccion(Personaje.NORTE)

        self._jugador.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((7, 3),self._mapa.CENTER))
        self._jugador.actualizar_direccion(Personaje.OESTE)        
        
        self._personajes = [self._jugador, self.npc_policia]

        self._taza = Objeto_Mundo('Taza de cafe','data/imagenes/taza.png',16,16)
        self._taza.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((3, 8),self._mapa.CENTER))

        self._plato = Objeto_Mundo('Plato','data/imagenes/plato.png',16,16)
        self._plato.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((5, 8),self._mapa.CENTER))
        
        self._ordenador = Objeto_Vacio('Ordenador')
        self._ordenador.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((3, 0),self._mapa.CENTER))
        
        self._objetos = [self._taza, self._plato, self._ordenador]
        

        self._mundo = Mundo(self._mapa, self._personajes, self._objetos)        
        
        self.inventario_surface = Inventario()
        
    def start(self):
        print "GameState Mapa1 Started"
        self._jugador.parar()
                
 
    def cleanUp(self):
        print "GameState Mapa1 Cleaned"
        pass
 
    def pause(self):
        print "GameState Mapa1 Paused"
        pass
 
    def resume(self):
        print "GameState Mapa1 Resumed"
        #if (not self.npc_policia.LEYENDO) and (self.npc_policia.APARTARSE_PUERTA):
        #    self.npc_policia.LEYENDO = True
        #    self._mundo.ir_a_y_accion(self._jugador, (7, 1), Personaje.NORTE, self._npc_policia_ir_a_leer)            
        if (self.parent.respuesta == "SI_CAFE"):
            self._mundo.ir_a(self.npc_policia, (4, 6), Personaje.NORTE)
            self._jugador.inventario.remove(self._taza)
            self.parent.respuesta = None
        pass
                
    def handleEvents(self, events):
    
        teclas_pulsadas = pygame.key.get_pressed()
        
        if teclas_pulsadas[K_ESCAPE]:
            self.parent.popState()
        elif teclas_pulsadas[K_a]:
            self._mundo.ir_a(self.npc_policia, (3, 3), Personaje.NORTE)
        elif teclas_pulsadas[K_UP]:
            self._mundo.mover_jugador(Personaje.NORTE)
        elif teclas_pulsadas[K_DOWN]:
            self._mundo.mover_jugador(Personaje.SUR)
        elif teclas_pulsadas[K_RIGHT]:
            self._mundo.mover_jugador(Personaje.ESTE)
        elif teclas_pulsadas[K_LEFT]:
            self._mundo.mover_jugador(Personaje.OESTE)
        elif teclas_pulsadas[K_s]:
            self.parent.salvar_partida()
        elif teclas_pulsadas[K_c]:
            self.parent.cargar_partida()
        elif (teclas_pulsadas[K_SPACE] and (not self._jugador.andando)):            
            # Accion de registro en el ordenador.
            objeto = self._mundo.obtener_objeto_de(self._mundo.obtener_celda_delantera_personaje())
            if (objeto != None):
                self._accion_con_objeto(objeto)
            
    def _accion_con_objeto(self, objeto):
    
        # Personaje
        if (objeto.tipo == "Personaje"):
            if (objeto.nombre == "Ordenador1"):
                if (not objeto.andando): # Si no est� andando podemos hablar con el.
                    if self._mundo.jugador_tiene(self._taza):
                        self.parent.pushState(ConversacionState(self.parent, 'conversacion1.xml', 2, objeto))
                    else:
                        if (self._mundo.esta_personaje_en_posicion(self.npc_policia,(4,6))):
                            self.parent.pushState(ConversacionState(self.parent, 'conversacion1.xml', 5, objeto))
                        else:
                            self.parent.pushState(ConversacionState(self.parent, 'conversacion1.xml', 0, objeto))
        # Objeto                
        elif (objeto.tipo == "Objeto"):
            if (objeto.nombre == "Taza de cafe"):
                self._objetos.remove(objeto)
                self._jugador.inventario.append(objeto)
                self.parent.pushState(ConversacionState(self.parent, 'conversacion1.xml', 3, self._jugador))
            elif (objeto.nombre == "Plato"):
                self._objetos.remove(objeto)
                self._jugador.inventario.append(objeto)
            elif (objeto.nombre == "Ordenador"):
                self.parent.pushState(ConversacionState(self.parent, 'conversacion1.xml', 6, objeto))
                
    def update(self):
        self._mundo.update()
        
        # Si el jugador sale por la puerta cargamos el segundo mapa.
        #if (self._mundo.esta_personaje_en_posicion(self._jugador, (6, 0))):
        #    self.parent.pushState(mapa2state.Mapa2State(self.parent))
 
                
    def _npc_policia_ir_a_leer(self):        
        self._mundo.ir_a(self.npc_policia, (3, 3), Personaje.NORTE)
        
    def draw(self):        
        self.parent.screen.blit(self.parent.background, (0, 0))
        self.parent.screen.blit(self._mundo.obtener_viewport_jugador((200,200)), (10,10))
        self.parent.screen.blit(self.inventario_surface.get_surface(self._jugador.inventario), (300,10))

        
