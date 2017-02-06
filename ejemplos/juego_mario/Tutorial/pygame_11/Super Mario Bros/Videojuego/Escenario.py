import base64
import StringIO
import json
import gzip
import pygame
from pygame.locals import *


class Mapa(object):
    
    _tileH=0
    _tileW=0
    
    _MapaW=0    
    _MapaH=0
   
    _transparentcolor=-1
    _matrizMapa=[]
    _mapaImagenes=[]
    
    _postile=0
    _posfondo=0
    
    _posEnemy=0


    def __init__(self):
        
        
        return
       
       
    def cargarMapa(self,Nivel):
                
        
        f = open("maps/"+Nivel+".json", "r")
        data = json.load(f)
        f.close()
        
        
        i=0
        
        
    
        for item in data["layers"]:            
            self.layers(item)
            
            
            
           
        for item in data["tilesets"]:
            self.tilesets(item)
            i+=1
    
        
        
        return
       
       
    def layers(self, layer):  
        
        self._MapaW= layer["width"]
        self._MapaH=layer["height"]
        
        
        #Obtener Mapa           
        mapa=layer["data"]   
        
        
        
        #Decodificar
        mapa = base64.decodestring(mapa)
        
        
        
           
        #descomprimir    
        cadena=gzip.zlib.decompress(mapa);
        
        
        
        # Convertir caracteres a numeros
        salida = []
        for idx in xrange(0, len(cadena), 4):
            val = ord(str(cadena[idx])) | (ord(str(cadena[idx + 1])) << 8) | \
            (ord(str(cadena[idx + 2])) << 16) | (ord(str(cadena[idx + 3])) << 24)
            salida.append(val)
       
        
        matrizTemp=[]
       
        #Convertir vector en Matriz
        for i in range(0, len(salida), self._MapaW):
            matrizTemp.append(salida[i:i+self._MapaW])
        
        self._matrizMapa=matrizTemp[:]
        
        
        
        return

       
    def tilesets(self,tileset):
        
        self._tileW=tileset["tilewidth"]
        self._tileH=tileset["tileheight"]        
        
        imgTemp=tileset["name"]
        
        try :
            self._transparentcolor=tileset["transparentcolor"]
            
        except :
            pass
        
        try:
            img=pygame.image.load("images/"+imgTemp+".png").convert()
        except pygame.error, message:
                raise SystemExit, message
        if self._transparentcolor!=-1:
            
            alpha=self._transparentcolor        
            alpha = alpha.lstrip('#')
            lv = len(alpha)
            alpha=tuple(int(alpha[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))                            
            img.set_colorkey(alpha, RLEACCEL)
            
            
            
        self.array_Tileset(img)
            
        
        
        return 
       
     
    def array_Tileset(self,img):
        
        
        for i in range(30):

            for j in range(27):
                self._mapaImagenes.append(img.subsurface((j*18,i*18,self._tileW,self._tileH)))
                
                        
        
        for i in range(len(self._mapaImagenes)):
            self._mapaImagenes[i]=pygame.transform.scale2x(self._mapaImagenes[i])
        
        
        
        
            
        return
    
    
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    """
    def cortar(self,img,rectangulo): 
        rect = pygame.Rect(rectangulo) 
        image = pygame.Surface(rect.size).convert() 
        image.blit(img,(0, 0), rect) 
        return image 
    """
    