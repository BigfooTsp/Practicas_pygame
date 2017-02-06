# -*- coding: utf-8 -*-
import pygame
from utilidades.imagen import cortar_tileset


class Objeto_Mundo:
    """ Clase que implementa los métodos comunes de todos los objetos que intervienen en el juego. """
    
    # Constantes que indican las posibles direcciones de un objeto en el juego. 
    NORTE = 0
    SUR = 1
    ESTE = 2
    OESTE = 3
    
    # Velocidad de movimiento del Objeto.
    VELOCIDAD = 0
    
    def __init__(self, nombre, imagen, tile_alto, tile_ancho):
        """Inicialización del Objeto Mundo.
                
        argumentos:
        nombre -- nombre del objeto en el mundo (Ej.: Policia_1, Ladron_1, Policia_2, Perro_1, ...) .
        imagen -- ruta de la imagen del objeto.
        tile_alto -- alto del objeto en pixeles.
        tile_ancho -- ancho del objeto en pixeles.
        
        """
        
        self.nombre = nombre
        self.tipo = "Objeto" # Definimos por defecto el tipo de Objeto como "Objeto".
        
        self._tile_alto = tile_alto
        self._tile_ancho = tile_ancho

        # Nos definimos un rectangulo para moverlo por el juego
        self._rect = pygame.Rect(0, 0, self._tile_ancho, self._tile_alto)
        
        # Cortamos el tileset con las imagenes del objeto.
        self._tileset = cortar_tileset(imagen, (self._tile_ancho, self._tile_alto), False)
        
        # Offset para dibujar el objeto. 
        # Por defecto es el centro del tile.
        self._offset_x = self._tile_ancho / 2
        self._offset_y = self._tile_alto / 2
        
        # Establecemos la dirección por defecto hacia donde mirará el Objeto.
        self._direccion = Objeto_Mundo.SUR
        
        # Creamos un array con los valores de [fila,columna] con respecto a su posición en los 4 puntos cardinales.
        # Por ejemplo, para ir hacia el NORTE deberemos restar -1 a la fila en la que estamos y la columna la 
        # deberemos dejar igual, en este caso le sumaríamos 0.
        self._direcciones = [[-1, 0], [1, 0], [0, 1], [0, -1]] # N,S,E,O
        
        # Creamos el array con las animaciones.
        # Por defecto siempre se dibujará el tile 0 del array de imagenes del tileset que hemos cargado anteriormente.
        self._animacion = [[0],[0],[0],[0]] # N,S,E,O
                      
        # Frame actual de la animación.
        self._frame = 0
        
        # Variable para bloquear un objeto y no se pueda mover
        self.bloqueado = True                    
        
        # Nos guardamos una imagen del tileset, en este caso la primera.
        self.imagen_objeto = self._tileset[0]
    
    def update(self):
        """ Actualiza el estado del objeto. """
        pass
        
    def dibujar(self, destino):
        """ Dibuja el objeto en el surface indicado 
        
        argumentos:
        destino -- suface donde se desea dibujar el objeto.
        
        """ 
        # Obtenemos el _frame que debemos dibujar dependiento de la orientación del personaje.
        cuadro_animacion = self._animacion[self._direccion][self._frame]

        # Dibujamos el tile correspondiente, teniendo encuenta el offset que establecimos al principio.
        destino.blit(self._tileset[cuadro_animacion], (self._rect.centerx - self._offset_x, self._rect.centery - self._offset_y))

    def obtener_coordenadas(self):
        """ Retorna las coordenadas centrales X e Y del objeto. """
        return (self._rect.centerx, self._rect.centery)
    
    def actualizar_direccion(self, direccion):
        """ Actualiza la dirección del objeto.
        
        argumentos:
        direccion -- dirección hacia donde mira el objeto (Ej.: Objeto_Mundo.NORTE, Objeto_Mundo.SUR, ETC ...)
        
        """
        self._direccion = direccion
        
    def obtener_direccion(self):
        """ Obtiene la dirección actual del objeto. """
        return self._direccion

    def actualizar_posicion(self, (coord_x, coord_y)):
        """ Establece la nueva coordenada central X e Y del objeto. 
        
        argumentos:
        coord_x -- coordenada x del objeto.
        coord_y --- coordenada y del objeto
        
        """
        self._rect.centerx = coord_x
        self._rect.centery = coord_y
     
    def mover(self, orientacion, velocidad=VELOCIDAD):
        """ Mueve el rectángulo del objeto, en la orientación indicada un número de pixeles igual a la velocidad.
        
        argumentos:
        orientacion -- dirección hacia donde debe mover (Ej.: Objeto_Mundo.NORTE, Objeto_Mundo.SUR, ETC ...).
        velicidad -- número de pixeles que se moverá.
        """        
        if ((orientacion != None) and (not self.bloqueado)): # Si no está bloqueado entonces se puede mover.
            self.actualizar_direccion(orientacion)
            self._rect.move_ip(self._direcciones[self._direccion][1] * velocidad, self._direcciones[self._direccion][0] * velocidad)
    

class Objeto_Vacio(Objeto_Mundo):
    """ Clase que define un Objeto del Mundo con una imagen transparente."""
    
    def __init__(self, nombre):
        Objeto_Mundo.__init__(self, nombre,'data/imagenes/objeto_vacio.png',16,16)
            