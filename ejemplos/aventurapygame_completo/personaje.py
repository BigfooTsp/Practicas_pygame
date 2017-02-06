# -*- coding: utf-8 -*-
from pygame.locals import *

from utilidades.imagen import *

class Personaje():

    TILE_ALTO = 32
    TILE_ANCHO = 32

    NORTE = 0
    SUR = 1
    ESTE = 2
    OESTE = 3

    def __init__(self, nombre, imagen):

        # Nombre identificativo del Personaje
        self.nombre = nombre
        
        # Nos definimos un rectangulo
        self.rect = Rect(0,0,Personaje.TILE_ANCHO,Personaje.TILE_ALTO)

        # Tileset con la animación del personaje.
        self.tileset = cortar_tileset(imagen, (Personaje.TILE_ANCHO, Personaje.TILE_ALTO), False)

        self.direccion = Personaje.SUR
        self.direcciones = [[-1, 0], [1, 0], [0, 1], [0, -1]] #N,S,E,O

        self.offset = (16,28)
        
        # Fila y columna donde se encuentra actualmente el personaje en el mapa.
        self.fila = 0
        self.columna = 0       

        self.animacion = [[0], [5], [1], [6]] #N,S,E,O
                
    def update(self):
        pass

    def dibujar(self, destino, coordenadas):
        # Obtenemos el cuadro que debemos dibujar dependiento de la orientación del personaje.
        cuadro_animacion = self.animacion[self.direccion][0]

        # Dibujamos el tile correspondiente.
        destino.blit(self.tileset[cuadro_animacion], (coordenadas[0] - self.offset[0], coordenadas[1] - self.offset[1]))

    def actualizar_posicion(self, (fila, columna)):        
        self.fila = fila
        self.columna = columna

    def mover(self, orientacion):

        if (orientacion != None):
            self.cambiar_direccion(orientacion)
            fila = self.fila + self.direcciones[self.direccion][0]
            columna = self.columna + self.direcciones[self.direccion][1]
            self.actualizar_posicion((fila, columna))            

    def cambiar_direccion(self, direccion):
        self.direccion = direccion

    def obtener_posicion(self):
        return (self.fila, self.columna)
