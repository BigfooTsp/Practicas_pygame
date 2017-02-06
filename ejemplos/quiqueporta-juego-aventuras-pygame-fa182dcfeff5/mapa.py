# -*- coding: utf-8 -*-
from xml.dom import minidom
import base64
import gzip
import StringIO

from utilidades.imagen import cortar_tileset
from utilidades.archivo import *

class Mapa:

    # Capas que forman el mapa
    LAYER_PISABLE = 0
    LAYER_SUELO = 1
    LAYER_OBJETOS = 2
    LAYER_OBJETOS_SUPERPUESTOS = 3
    LAYER_CIELO = 4

    TOP_LEFT = 0
    CENTER = 1
    BOTTOM_RIGHT = 2

    def __init__(self, nombre):

        # Nombre del archivo del mapa a cargar.
        self.nombre = nombre

        # Array para guardar las capas del mapa.
        self.capas = []
        
        # Cargamos el mapa en self.capas.
        self._cargar_mapa() # Inicializa los valores desde el xml.

        # Obtenemos un array unidimensional con todos los tilesets del mapa.
        self.tileset = cortar_tileset("data/imagenes/" + self.tileset, self.tam_tiles, True)
        
        self.direcciones = [[-1, 0], [1, 0], [0, 1], [0, -1]] # N, S, E, O

    # Extrae valores mapa desde XML.
    def _cargar_mapa(self):
        xmlMap = minidom.parse("data/mapas/" + self.nombre)
        nPrincipal = xmlMap.childNodes[0]

        # Tama�o mapa
        self.width = int(nPrincipal.attributes.get("width").value)
        self.height = int(nPrincipal.attributes.get("height").value)

        for i in range(len(nPrincipal.childNodes)):
            if nPrincipal.childNodes[i].nodeType == 1:
                if nPrincipal.childNodes[i].nodeName == "tileset":
                    if nPrincipal.childNodes[i].attributes.get("name").value != "config":
                        width = nPrincipal.childNodes[i].attributes.get("tilewidth").value
                        height = nPrincipal.childNodes[i].attributes.get("tileheight").value
                        nombre = nPrincipal.childNodes[i].childNodes[1].attributes.get("source").value
                        nombre = extraer_nombre(nombre)
                        if nPrincipal.childNodes[i].attributes.get("name").value == "tileset":
                            self.tileset = nombre                            
                    self.tam_tiles = (int(width), int(height))
                if nPrincipal.childNodes[i].nodeName == "layer":
                    layer = nPrincipal.childNodes[i].childNodes[1].childNodes[0].data.replace("\n", "").replace(" ", "")
                    layer = self._decodificar(layer) # Decodifica la lista
                    layer = self._convertir(layer, self.width) # Convierta en array bidimensional                        
                    self.capas.append(layer)
    
    def _decodificar(self, cadena):
        ''' Decodifica y descomprime los datos de un mapa creado con el TileMap Editor '''
        # Decodificar.
        cadena = base64.decodestring(cadena)

        # Descomprimir.
        copmressed_stream = StringIO.StringIO(cadena)
        gzipper = gzip.GzipFile(fileobj=copmressed_stream)
        cadena = gzipper.read()

        # Convertir.
        salida = []
        for idx in xrange(0, len(cadena), 4):
            val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
            (ord(str(cadena[idx + 2])) << 16) | (ord(str(cadena[idx + 3])) << 24)
            salida.append(val)

        return salida

    # Convierte un array unidimensional en uno bidimensional.
    def _convertir(self, lista, col):
        nueva = []
        for i in range(0, len(lista), col):
            nueva.append(lista[i:i + col])
        return nueva


    def dibujar(self, capa, dest, x, y):
        ''' Dibuja una capa del mapa en una surface '''
        x_aux = x
        y_aux = y

        for f in range(self.height): # filas
            for c in range(self.width): # columnas
                if self.capas[capa][f][c]:
                    dest.blit(self.tileset[self.capas[capa][f][c]], (x_aux, y_aux))
                x_aux = x_aux + self.tam_tiles[0]
            y_aux = y_aux + self.tam_tiles[1]
            x_aux = x
            
    def obtener_posicion_por_coordenadas(self, (x, y)):
        fila = (int)(y / self.tam_tiles[1])
        columna = (int)(x / self.tam_tiles[0])
        return (fila, columna)
            
    def obtener_coordenadas_por_posicion(self, (fila, columna), posicion):
        
        y = fila * self.tam_tiles[1] 
        x = columna * self.tam_tiles[0]            

        if (posicion == self.CENTER):
            y += (self.tam_tiles[1] / 2)
            x += (self.tam_tiles[0] / 2)
        elif (posicion == self.BOTTOM_RIGHT):
            y += self.tam_tiles[1]
            x += self.tam_tiles[0]
        
        return (x, y)
        
    def obtener_size_mapa_pixeles(self):
        return (self.tam_tiles[0] * self.width, self.tam_tiles[1] * self.height)
    
    def es_pisable(self, fila, columna):
        # Si la fila o columna esta fuera de los limites del mapa no se puede caminar.
        if ((fila >= self.height) or (fila < 0) or (columna >= self.width) or (columna < 0)):
            return False
        else:
            return not (self.capas[Mapa.LAYER_PISABLE][fila][columna]) # Comprobamos si es pisable en la Capa del mapa.

    def obtener_centro_celda(self, fila, columna):
        '''centrar el personaje en la celda en la que se encuentra'''
        x = (self.tam_tiles[0] * columna) + (self.tam_tiles[0] / 2)
        y = (self.tam_tiles[1] * fila) + (self.tam_tiles[1] / 2)
        return (x,y)