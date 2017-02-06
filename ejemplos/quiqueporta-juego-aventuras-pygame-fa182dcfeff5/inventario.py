import pygame
from pygame.locals import *
from utilidades.texto import Texto

class Inventario(object):
    
    def __init__(self):
        self.letra = pygame.font.Font(None, 16)
        self.surface_inventario = pygame.Surface((140,200))
        
    def get_surface(self, inventario):        
        self.surface_inventario.fill((0,0,0))
        
        self.surface_inventario.blit(Texto.render_textrect("Inventario", self.letra, Rect(0,0,200,20), (255,255,255), (0,0,0,), 0),(5,5));
        
        y = 20
        for item in inventario:
            self.surface_inventario.blit(item.imagen_objeto, (10, y))
            self.surface_inventario.blit(Texto.render_textrect(item.nombre, self.letra, Rect(0,0,200,50), (255,255,255), (0,0,0,), 0),(30,y));
            y += 16
        return self.surface_inventario
        #surface.blit(self.surface_inventario, (160, 0))    
        