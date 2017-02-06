# -*- coding: utf-8 -*-

from personaje import Personaje

class Jugador(Personaje):

    def __init__(self):

        Personaje.__init__(self, 'Jugador', 'data/imagenes/image.png',(49,35))
        
        # Aqui definimos los cuadros de animación de como se mueven los personajes en cada ciclo.
        self._animacion = [[1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2], 
                           [7, 7, 7, 7, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8],  
                           [4, 4, 4, 4, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],  
                           [10, 10, 10, 10, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11]] #N,S,E,O        

        # Para las imagenes de nuestros personajes, el offset es (16,28)
        self._offset_x = 15
        self._offset_y = 40

        # MAPA 1
        self.REGISTRADO_MAPA1 = False
        

class NPC_Policia_1(Personaje):

    def __init__(self):

        Personaje.__init__(self, 'Ordenador1', 'data/imagenes/enemigo.png',(32,32))
        
        # MAPA 1
        self.APARTARSE_ORDENADOR = False
        self.LEYENDO = False

class NPC_Preso_1(Personaje):

    def __init__(self):

        Personaje.__init__(self, 'Preso1', 'data/imagenes/enemigo.png',(32,32))
        
        # MAPA 2

class NPC_Preso_2(Personaje):

    def __init__(self):

        Personaje.__init__(self, 'Preso1', 'data/imagenes/enemigo2.png',(32,32))
        
        # MAPA 2
        
