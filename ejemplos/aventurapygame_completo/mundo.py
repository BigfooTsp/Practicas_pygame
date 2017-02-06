# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *

from mapa import *
from personaje import *

class Mundo:
    ''' Clase para controlar todo lo que ocurre durante el juego:
        Colisiones, Dibujar personajes, control del jugador, etc ...
    '''

    def __init__(self, mapa, personajes):
        ''' Constructor de la Clase que obtiene el mapa y los personajes que intervendrán en esta pantalla'''

        self._personajes = personajes # Array con los personajes que intervienen en este mundo.

        # En la lista que pasemos de los personajes, el primero debe ser siempre el Jugador.
        self._jugador = personajes[0]

        self._mapa = mapa

        # Variable para saber hacia donde quiere mover el jugador.
        self._direccion_movimiento_jugador = None

    def dibujar (self, surface):
        ''' Dibuja las capas del mapa y TODOS los personajes del juego'''
        self._mapa.dibujar(Mapa.LAYER_SUELO, surface,0,0)
        self._mapa.dibujar(Mapa.LAYER_OBJETOS, surface,0,0)
        self._mapa.dibujar(Mapa.LAYER_OBJETOS_SUPERPUESTOS, surface,0,0)
        # Dibujamos los personajes
        for personaje in self._personajes:
            personaje.dibujar(surface, self._mapa.obtener_centro_celda(personaje.fila,personaje.columna))
        self._mapa.dibujar(Mapa.LAYER_CIELO, surface,0,0)
        
    def update(self):
        ''' Mueve y actualiza las posiciones de los personajes '''
        # Si se ha intentado mover al personaje
        if (self._direccion_movimiento_jugador != None):
            
            # Calculamos donde va a mover el Jugador
            posicion_a_mover = (self._jugador.fila + self._jugador.direcciones[self._direccion_movimiento_jugador][0], self._jugador.columna + self._jugador.direcciones[self._direccion_movimiento_jugador][1])
            
            # Si no hay colision ...
            if (not self._hay_colision(self._jugador,posicion_a_mover)):
                self._jugador.mover(self._direccion_movimiento_jugador) # Movemos al jugador en la dirección indicada
            else:
                # Solo cambiamos las direccion pero sin moverlo
                self._jugador.cambiar_direccion(self._direccion_movimiento_jugador)

            self._direccion_movimiento_jugador = None

            # Ordenamos los personajes por fila, para luego dibujarlos correctamente. Para que no se solapen.
            self._personajes.sort(self._comparar_posicion_personajes)
    

    def mover_jugador(self, direccion):
        ''' Establece hacia donde debe mover el jugador '''
        self._direccion_movimiento_jugador = direccion

    def _hay_colision(self, personaje, destino):
        ''' Comprueba si existe colision de un personajes con otros o con el mapa '''
        hay_colision = False
        # Comprobamos que la celda donde va a mover es pisable
        if (not self._mapa.es_pisable(destino[0],destino[1])):            
            hay_colision = True
            
        # Comprobamos las colisiones con el resto de personajes
        for item in self._personajes:
            if (item.nombre != personaje.nombre):
                if (item.obtener_posicion() == destino):
                    hay_colision = True
            
        return hay_colision
        
    def _comparar_posicion_personajes(self, a, b):
        ''' Compara y la posicion de un personaje con respecto a su fila '''
        return cmp(int(a.fila), int(b.fila))
