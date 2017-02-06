# -*- coding: utf-8 -*-
import copy

import pygame
from pygame.locals import *

from mapa import Mapa
from utilidades.astar import AStar

class Mundo:
    """ Clase para controlar todo lo que ocurre durante el juego:
        Colisiones, Dibujar personajes, control del jugador, etc ...
    """

    def __init__(self, mapa, personajes, objetos):
        """ Constructor de la Clase que obtiene el mapa y los personajes que intervendrán en esta mundo. 
        
        argumentos:
        mapa -- Objeto Mapa del juego.
        personajes -- Array con los personajes que intervienen en este mundo.
            En la lista que pasemos de los personajes, el primero debe ser siempre el Jugador.
        objetos -- Array con los objetos que intervienen en este mundo.
        
        """

        self._personajes = personajes 
        self._objetos = objetos        

        # En la lista que pasemos de los personajes, el primero debe ser siempre el Jugador.
        self._jugador = personajes[0]

        self._mapa = mapa
        (self._mapa_pixeles_ancho, self._mapa_pixeles_alto) = self._mapa.obtener_size_mapa_pixeles()        

        # Variable para saber hacia donde quiere mover el jugador.
        self._direccion_movimiento_jugador = None


        self.surface_mundo = pygame.Surface(self._mapa.obtener_size_mapa_pixeles())
        self.surface_mundo = self.surface_mundo.convert()
        self.surface_mundo.fill((0, 0, 0))
        
    def _dibujar (self):
        """ Dibuja las capas del mapa y TODOS los personajes y objetos del juego. 
        
        argumentos:
        destino -- Surface donde se dibujará todo.
        
        """
        self._mapa.dibujar(Mapa.LAYER_SUELO, self.surface_mundo, 0, 0)
        self._mapa.dibujar(Mapa.LAYER_OBJETOS, self.surface_mundo, 0, 0)
        self._mapa.dibujar(Mapa.LAYER_OBJETOS_SUPERPUESTOS, self.surface_mundo, 0, 0)
        # Dibujamos los objetos
        for objeto in self._objetos:
            objeto.dibujar(self.surface_mundo)
        # Dibujamos los personajes
        for personaje in self._personajes:
            personaje.dibujar(self.surface_mundo)
        self._mapa.dibujar(Mapa.LAYER_CIELO, self.surface_mundo, 0, 0)
    
    def obtener_viewport(self, rect):
        return self.surface_mundo.subsurface(rect)

    def obtener_viewport_jugador(self, (alto, ancho)):
        (x_jugador,y_jugador) = self._jugador.obtener_coordenadas()        
        
        x = x_jugador - (ancho / 2)
        if (x < 0):
            x = 0
        if (x + ancho > self._mapa_pixeles_ancho):
            x = self._mapa_pixeles_ancho - ancho
            
        y = y_jugador -(alto / 2)
        if (y < 0):
            y = 0
        if (y + alto > self._mapa_pixeles_alto):
            y = self._mapa_pixeles_alto - alto
             
        return self.surface_mundo.subsurface((x, y, ancho, alto))
    
    def update(self):
        """ Mueve y actualiza las posiciones de los personajes. """

        # Ordenamos los personajes por fila, para luego dibujarlos correctamente. Para que no se solapen.
        self._personajes.sort(self._comparar_coordenadas_personajes)

        for personaje in self._personajes:
            if (personaje.andando): # Si está andando.
                # Si el personaje se encuentra en el centro de la celda a donde debia llegar ...
                if (personaje.obtener_coordenadas() == self._mapa.obtener_coordenadas_por_posicion((personaje.camino[0][0], personaje.camino[0][1]),self._mapa.CENTER)):                    
                    del personaje.camino[:1] # Eliminamos esa celda del camino ha seguir porque ya ha llegado a ella.                    
                    if ((personaje.camino == []) or (personaje.camino == None)): # Si ya no queda camino a seguir...
                        personaje.parar() # Paramos al Personaje.
                        if not(personaje.accion == None): # Si tiene asignada alguna acción después de haber llegado a su destino ...
                            personaje.accion() # Ejecutamos la acción
                            personaje.accion = None # Y limpiamos la acción
                        if (personaje.nombre != "Jugador"): # Si el Personaje no es el Jugador establacemos su dirección final.
                            personaje.actualizar_direccion(personaje.direccion_final)
                    else: # Calculamos la nueva direccion hacia donde tiene que mover
                        # Obtenemos la fila y columna donde se encuenta el personaje.
                        origen = self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas())
                        # Establecemos hacia donde tiene que mirar el Personaje para ir en esa dirección.
                        personaje.actualizar_direccion(self._mapa.direcciones.index([personaje.camino[0][0] - origen[0], personaje.camino[0][1] - origen[1]]))
                else: # Si el personaje no esa todavia en el centro de la celda                    
                    if (not self._hay_colision(personaje, (personaje.camino[0][0], personaje.camino[0][1]))): # Si no hay colisión en la celda de destino                        
                        personaje.mover(personaje.obtener_direccion()) # Movemos al personaje en esa dirección.
                    else: # Si hay colision
                        celda_personaje = self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas())
                        personaje.actualizar_posicion(self._mapa.obtener_coordenadas_por_posicion((celda_personaje[0], celda_personaje[1]),self._mapa.CENTER))
                        # Volvermos a calcular una ruta para llegar al destino.
                        self.ir_a(personaje, personaje.destino, personaje.direccion_final)
                    
            personaje.update() # Actualizamos el personaje.
        
        for objeto in self._objetos: # Actualizamos los objetos.
            objeto.update()
        
        self._dibujar(
                      )    
    def mover_jugador(self, direccion):
        """ Establece hacia donde debe mover el jugador.
        
        argumentos
        direccion -- dirección hacia donde se quiero mover al jugador.
        
        """
        # Si no está andado ya y no está bloqueado.
        if ((not self._jugador.andando) and (not self._jugador.bloqueado)):
        
            # Si la dirección es distinta a la actual.
            if (self._jugador.obtener_direccion() != direccion):
                self._jugador.actualizar_direccion(direccion) # Actualizamos su dirección.
            else: # Si la dirección es distina.
                self._direccion_movimiento_jugador = direccion # Establecemos la nueva dirección del jugador.
                
                # Calculamos donde va a mover el Jugador
                posicion_actual_jugador = self._mapa.obtener_posicion_por_coordenadas(self._jugador.obtener_coordenadas())
                
                fila_a_mover = posicion_actual_jugador[0] + self._mapa.direcciones[direccion][0]
                columna_a_mover = posicion_actual_jugador[1] + self._mapa.direcciones[direccion][1]
                
                destino_a_mover = (fila_a_mover, columna_a_mover)
                
                self._jugador.actualizar_direccion(direccion)
                self._jugador.destino = destino_a_mover

                camino_a_seguir = []
                camino_a_seguir.append(destino_a_mover)
                
                if (not self._hay_colision(self._jugador, destino_a_mover)):                
                    self._jugador.ir_a(camino_a_seguir) # Movemos al jugador en la dirección indicada                
        elif (self._jugador.bloqueado): # Si está bloqueado solo cambiamos la dirección
            self._jugador.actualizar_direccion(direccion)
            
    def ir_a (self, personaje, destino, direccion_final):
        
        camino = self._obtener_camino(personaje, destino)

        if (camino != None):
            personaje.ir_a(camino)

            origen = self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas())        
            personaje.actualizar_direccion(self._mapa.direcciones.index([personaje.camino[0][0] - origen[0], personaje.camino[0][1] - origen[1]]))
            
            personaje.andando = True
            personaje.direccion_final = direccion_final
            personaje.destino = destino
        else:
            personaje.andando = False
            personaje.direccion_final = direccion_final
            personaje.destino = None
            
    def ir_a_y_accion (self, personaje, destino, direccion_final, accion):
            self.ir_a(personaje, destino, direccion_final)
            personaje.accion = accion                

    def _hay_colision(self, personaje, destino):
        ''' Comprueba si existe colision de un personajes con otros o con el mapa '''
        hay_colision = False
        # Comprobamos que la celda donde va a mover es pisable
        if (not self._mapa.es_pisable(destino[0], destino[1])):            
            hay_colision = True
            
        # Comprobamos las colisiones con el resto de personajes
        for item in self._personajes:
            if (item.nombre != personaje.nombre):
                if (self._mapa.obtener_posicion_por_coordenadas(item.obtener_coordenadas()) == destino):
                    hay_colision = True
            

        # Comprobamos las colisiones con los objetos
        for item in self._objetos:
            if (self._mapa.obtener_posicion_por_coordenadas(item.obtener_coordenadas()) == destino):
                hay_colision = True

        return hay_colision
        
    def esta_personaje_en_posicion(self, personaje, (fil, col)):
        if (self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas()) == (fil, col)):
            return True
        else:
            return False

    def jugador_tiene(self, objeto):
        try:
            index = self._jugador.inventario.index(objeto)
        except ValueError:
            index = -1
        
        return (index >= 0)
            
        
    def obtener_objeto_de(self,(fil,col)):
        # Comprobamos si hay algun personaje u objeto en esa posicion   
        objeto = None
        for item in self._personajes:
            if (item.nombre != "Jugador"):         
                if (self.esta_personaje_en_posicion(item,(fil,col))):
                    objeto = item
                    break
            
        for item in self._objetos:
            if (self.esta_personaje_en_posicion(item,(fil,col))):
                objeto = item
                break
                
        return objeto
        
    def obtener_celda_delantera_personaje(self):        
        (fil,col) = self._mapa.obtener_posicion_por_coordenadas(self._jugador.obtener_coordenadas())
        fil += self._mapa.direcciones[self._jugador.obtener_direccion()][0]
        col += self._mapa.direcciones[self._jugador.obtener_direccion()][1]
        return (fil,col)
    
                        
    def _comparar_coordenadas_personajes(self, a, b):
        ''' Compara la posicion de un personaje con respecto a su eje y '''
        return cmp(int(a.obtener_coordenadas()[1]), int(b.obtener_coordenadas()[1]))

        
    # ----------------------------------------------
    # PATH FINDING
    # ----------------------------------------------
    
    def _obtener_camino(self, personaje, destino):

        camino = None

        origen = self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas())        
        fila_origen = origen[0]
        columna_origen = origen[1]
        
        fila_destino = destino[0]
        columna_destino = destino[1]

        # Si ya esta en esa posicion no calcula ruta a ninguna parte
        if (self._mapa.obtener_posicion_por_coordenadas(personaje.obtener_coordenadas()) == destino):
                return camino
        else:

            if ((fila_origen == fila_destino) and (columna_origen == columna_destino)):
                camino = [[fila_destino, columna_destino]]
            else:
                mapa_pisable = copy.deepcopy(self._mapa.capas[Mapa.LAYER_PISABLE])
                
                objetos = self._personajes + self._objetos
                
                for item in objetos:
                    if (item.nombre != personaje.nombre):
                        posicion_otro_personaje = self._mapa.obtener_posicion_por_coordenadas(item.obtener_coordenadas())                    
                        mapa_pisable[posicion_otro_personaje[0]][posicion_otro_personaje[1]] = 1
                        # Si en el destino hay alguien no se calcula nada
                        if ((fila_destino == posicion_otro_personaje[0]) and (columna_destino == posicion_otro_personaje[1])):
                            return camino
                    
                mapa_pisable[fila_origen][columna_origen] = 2 # Origen
                mapa_pisable[fila_destino][columna_destino] = 3 # Destino

                A = AStar(mapa_pisable)

                if A.camino == -1:
                    camino = None # No se puede llegar al destino
                else:
                    camino = A.camino

            return camino
    