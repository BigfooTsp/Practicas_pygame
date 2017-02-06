from xml.dom import minidom
import pygame
from pygame.locals import *

from utilidades import texto


class Conversacion():
 
    PREGUNTA = 0
    RESPUESTAS = 1

    ID_RESPUESTA = 0
    SIGUIENTE = 1
    TEXTO_RESPUESTA = 2
    RETURN_RESPUESTA = 3
    
    COLOR_SELECCIONADO = (255, 0, 0)
    COLOR_PREGUNTA = (255, 255, 255)
    COLOR_RESPUESTA = (255, 255, 255)
    BGCOLOR_SELECCIONADO = (0, 0, 0)
    BGCOLOR_PREGUNTA = (0, 0, 0)
    BGCOLOR_RESPUESTA = (0, 0, 0)
    
    ANCHO_CONVERSACION = 155
    ALTO_CONVERSACION = 400

    POSICION_CONVERSACION = (5, 170)
    
    def __init__(self, archivo, id_dialogo):
    
        self.background = pygame.Surface((160, 100))
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))        

        self.letra = pygame.font.Font(None, 14)

        self.xml_documento = minidom.parse(archivo)
        self.id_dialogo = id_dialogo
        self.siguiente_id_dialogo = -1
        self.dialogo = []
        self.fin_conversacion = False
        self.imagen_respuestas = []
        self.opcion_seleccionada = 0
        
        self._cargar_conversacion()
        self.respuesta = ""
 
    def _cargar_conversacion(self):
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
  
    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_DOWN :
                    self.opcion_seleccionada += 1
                elif event.key == pygame.K_UP :
                    self.opcion_seleccionada -= 1
                elif event.key == pygame.K_RETURN :
                    # Nos guardamos la respuesta
                    self.respuesta = self.dialogo[self.id_dialogo][Conversacion.RESPUESTAS][self.opcion_seleccionada][Conversacion.RETURN_RESPUESTA]
                    self.siguiente_id_dialogo = int(self.dialogo[self.id_dialogo][Conversacion.RESPUESTAS][self.opcion_seleccionada][Conversacion.SIGUIENTE])
                    self.id_dialogo = self.siguiente_id_dialogo
                 
                if (self.opcion_seleccionada < 0):
                    self.opcion_seleccionada = len(self.dialogo[self.id_dialogo][Conversacion.RESPUESTAS]) - 1
                if (self.opcion_seleccionada > len(self.dialogo[self.id_dialogo][Conversacion.RESPUESTAS]) - 1):
                    self.opcion_seleccionada = 0
                    
                self._obtener_imagen_pregunta()
                self._obtener_imagen_respuestas()
            
    def hay_dialogo(self):
        # Salimos si no hay mas dialogos a seguir.
        if (self.siguiente_id_dialogo == 0):
            return self.respuesta
        else:
            return None
 
    def dibujar(self, dest_surface):
        dest_surface.blit(self.background, Conversacion.POSICION_CONVERSACION)        
        dest_surface.blit(self.imagen_pregunta, Conversacion.POSICION_CONVERSACION)
        i = self.imagen_pregunta.get_height() + 5
        for respuesta in self.imagen_respuestas:
            dest_surface.blit(respuesta, (Conversacion.POSICION_CONVERSACION[0], Conversacion.POSICION_CONVERSACION[1] + i))
            i += respuesta.get_height() + 5
            
    def _obtener_imagen_pregunta(self):
        if (self.siguiente_id_dialogo != 0):
            self.imagen_pregunta = texto.Texto.render_textrect(self.dialogo[self.id_dialogo][Conversacion.PREGUNTA], self.letra, Rect(0, 0, Conversacion.ANCHO_CONVERSACION, 20), Conversacion.COLOR_PREGUNTA, Conversacion.BGCOLOR_PREGUNTA, 0)

    def _obtener_imagen_respuestas(self):
        self.imagen_respuestas = []
        for respuesta in self.dialogo[self.id_dialogo][Conversacion.RESPUESTAS]:
            if (self.opcion_seleccionada == int(respuesta[Conversacion.ID_RESPUESTA])):
                self.imagen_respuestas.append(texto.Texto.render_textrect(respuesta[Conversacion.TEXTO_RESPUESTA], self.letra, Rect(0, 0, Conversacion.ANCHO_CONVERSACION, 10), Conversacion.COLOR_SELECCIONADO, Conversacion.BGCOLOR_SELECCIONADO, 0))
            else:
                self.imagen_respuestas.append(texto.Texto.render_textrect(respuesta[Conversacion.TEXTO_RESPUESTA], self.letra, Rect(0, 0, Conversacion.ANCHO_CONVERSACION, 10), Conversacion.COLOR_RESPUESTA, Conversacion.BGCOLOR_RESPUESTA, 0))
        