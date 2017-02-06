# -*- coding: utf-8 -*-
from xml.dom import minidom
import pygame
from pygame.locals import *
from gamemanager.states import  gamestate
from utilidades import texto


class ConversacionState(gamestate.GameState):
 
    PREGUNTA = 0
    RESPUESTAS = 1

    ID_RESPUESTA = 0
    SIGUIENTE = 1
    TEXTO_RESPUESTA = 2
    RETURN_RESPUESTA = 3
    
    COLOR_SELECCIONADO = (255, 0, 0)
    COLOR_PREGUNTA = (62, 96, 150)
    COLOR_RESPUESTA = (0, 0, 0)
    
    BGCOLOR = (250, 250, 250)
    BGCOLOR_SELECCIONADO = (255, 255, 255)
    BGCOLOR_PREGUNTA = (255, 255, 255)
    BGCOLOR_RESPUESTA = (255, 255, 255)
    
    ANCHO_CONVERSACION = 210
    ALTO_CONVERSACION = 110

    POSICION_CONVERSACION_PADRE = (10, 20)
    POSICION_CONVERSACION = (30, 20)
    
    POSICION_IMAGEN_PERSONAJE = (0,0)
    
    def __init__(self, parent, archivo, id_dialogo, personaje):
        self.parent = parent
        self.letra = pygame.font.Font(None, 18)

        self.xml_documento = minidom.parse('data/conversaciones/'+archivo)
        self.id_dialogo = id_dialogo
        self.siguiente_id_dialogo = -1
        self.dialogo = []
        self.fin_conversacion = False
        self.imagen_respuestas = []
        self.opcion_seleccionada = 0
        
        self._personaje = personaje
 
        self.background = pygame.Surface((ConversacionState.ANCHO_CONVERSACION,ConversacionState.ALTO_CONVERSACION))
                
 
    def start(self):
        # Cargamos el archivo de las conversaciones
        for node in self.xml_documento.getElementsByTagName('dialogue'):

            pregunta = []
            respuestas = []

            if (node.hasChildNodes()):
                for i in range(len(node.childNodes)):
                    if (node.childNodes[i].nodeName == "speech"):
                        pregunta = node.childNodes[i].childNodes[0].data
                    elif (node.childNodes[i].nodeName == "response"):
                        respuestas.append([node.childNodes[i].getAttribute("id"), node.childNodes[i].getAttribute("nextdialogue"), node.childNodes[i].childNodes[0].data, node.childNodes[i].getAttribute("respuesta")])

            self.dialogo.append([pregunta, respuestas])
        
        # Generamos las imagenes de la conversacion actual
        self._obtener_imagen_pregunta()
        self._obtener_imagen_respuestas()
 
    def cleanUp(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass
 
    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_DOWN :
                    self.opcion_seleccionada += 1
                elif event.key == pygame.K_UP :
                    self.opcion_seleccionada -= 1
                elif event.key == pygame.K_RETURN :
                    # Nos guardamos la respuesta
                    self.parent.respuesta = self.dialogo[self.id_dialogo][ConversacionState.RESPUESTAS][self.opcion_seleccionada][ConversacionState.RETURN_RESPUESTA]
                    print self.parent.respuesta
                    self.siguiente_id_dialogo = int(self.dialogo[self.id_dialogo][ConversacionState.RESPUESTAS][self.opcion_seleccionada][ConversacionState.SIGUIENTE])
                    self.id_dialogo = self.siguiente_id_dialogo
                 
                if (self.opcion_seleccionada < 0):
                    self.opcion_seleccionada = len(self.dialogo[self.id_dialogo][ConversacionState.RESPUESTAS]) - 1
                if (self.opcion_seleccionada > len(self.dialogo[self.id_dialogo][ConversacionState.RESPUESTAS]) - 1):
                    self.opcion_seleccionada = 0
                    
                self._obtener_imagen_pregunta()
                self._obtener_imagen_respuestas()
            
    def update(self):
        # Salimos si no hay mas dialogos a seguir.
        if (self.siguiente_id_dialogo == 0):
            self.parent.popState()        
 
    def draw(self):
        self.background.fill(ConversacionState.BGCOLOR)        
        self.background.blit(self.background, ConversacionState.POSICION_CONVERSACION)
        self.background.blit(self._personaje.imagen_objeto, ConversacionState.POSICION_IMAGEN_PERSONAJE)        
        self.background.blit(self.imagen_pregunta, ConversacionState.POSICION_CONVERSACION)
        i = self.imagen_pregunta.get_height() + 5
        for respuesta in self.imagen_respuestas:
            self.background.blit(respuesta, (ConversacionState.POSICION_CONVERSACION[0], ConversacionState.POSICION_CONVERSACION[1] + i))
            i += respuesta.get_height() + 5
            
        self.parent.screen.blit(self.background, ConversacionState.POSICION_CONVERSACION_PADRE)
            
    def _obtener_imagen_pregunta(self):
        if (self.siguiente_id_dialogo != 0):
            self.imagen_pregunta = texto.Texto.render_textrect(self.dialogo[self.id_dialogo][ConversacionState.PREGUNTA], self.letra, Rect(0, 0, ConversacionState.ANCHO_CONVERSACION, 20), ConversacionState.COLOR_PREGUNTA, ConversacionState.BGCOLOR_PREGUNTA, 0)

    def _obtener_imagen_respuestas(self):
        self.imagen_respuestas = []
        for respuesta in self.dialogo[self.id_dialogo][ConversacionState.RESPUESTAS]:
            if (self.opcion_seleccionada == int(respuesta[ConversacionState.ID_RESPUESTA])):
                self.imagen_respuestas.append(texto.Texto.render_textrect(respuesta[ConversacionState.TEXTO_RESPUESTA], self.letra, Rect(0, 0, ConversacionState.ANCHO_CONVERSACION, 10), ConversacionState.COLOR_SELECCIONADO, ConversacionState.BGCOLOR_SELECCIONADO, 0))
            else:
                self.imagen_respuestas.append(texto.Texto.render_textrect(respuesta[ConversacionState.TEXTO_RESPUESTA], self.letra, Rect(0, 0, ConversacionState.ANCHO_CONVERSACION, 10), ConversacionState.COLOR_RESPUESTA, ConversacionState.BGCOLOR_RESPUESTA, 0))
        