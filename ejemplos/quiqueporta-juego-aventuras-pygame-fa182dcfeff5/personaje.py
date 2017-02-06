# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *

from objeto_mundo import Objeto_Mundo

class Personaje(Objeto_Mundo):
    """ Clase que define la estructura de un personaje del juego. """

    # Los personajes mueven 1 pixel cada vez que se mueven.
    VELOCIDAD = 1

    def __init__(self, nombre, imagen, size):

        # Llamada a la clase padre.
        Objeto_Mundo.__init__(self, nombre, imagen, size[0], size[1])
        
        # Definimos el tipo de objeto.
        self.tipo = "Personaje"
        
        # Establecemos la dirección por defecto.
        self._direccion = Personaje.SUR        

        # Para las imagenes de nuestros personajes, el offset es (16,28)
        self._offset_x = 16
        self._offset_y = 28
        
        # Aqui definimos los cuadros de animación de como se mueven los personajes en cada ciclo.
        self._animacion = [[0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 10, 10, 10, 10], 
                           [5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5, 11, 11, 11, 11], 
                           [1, 1, 1, 1, 4, 4, 4, 4, 1, 1, 1, 1, 7, 7, 7, 7], 
                           [6, 6, 6, 6, 3, 3, 3, 3, 6, 6, 6, 6, 9, 9, 9, 9]] #N,S,E,O        

        # Establecemos la imagen del Personaje por defecto para las conversaciones.                      
        self.imagen_objeto = self._tileset[5]
                              
        # El Personaje no está bloqueado por defecto.  
        self.bloqueado = False
                      
        # Variables para mover mediante IA el objeto
        self.andando = False
        self.destino = []
        self.direccion_final = Personaje.SUR        
        self.accion = None
        
        # Inventario de objetos.
        self.inventario = []
    
    def update(self):
        """ Actualiza la animación de movimiento de un Personaje. """ 
        if (self.andando): # Si está "andando" ...
            self._frame += 1 # Incrementamos el cuadro de animación
            if self._frame >= len(self._animacion[self._direccion]): # Si superamos los elementos de array volvemos a 0.
                self._frame = 0
        else:
            self._frame = 0 # Si no está andando el cuadro de animación es el 0.

    def ir_a(self, camino):
        """ Pone en movimiento a un Personaje.
         
        argumentos:
        camino --- array con las celdas (fil,col) por donde debe pasar el personaje para llegar a su destino.
        
        """
        self.andando = True
        self.bloqueado = False      
        self.camino = camino

    def parar(self):
        """ Para el movimiento de un Personaje. """
        self.andando = False
        self.camino = None        
        self.destino = []
    
    def mover(self, direccion):
        """ Mueve el Personaje en la dirección indicada. 
        
        argumentos:
        direccion -- dirección hacia donde debe mover el Personaje.
        
        """
        Objeto_Mundo.mover(self, direccion, Personaje.VELOCIDAD);
        
