#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
 
 
# Constantes
WIDTH = 900
HEIGHT = 500
 
#===========================================================
#=================IMAGEN====================================
 
def imagen(filename, transparent=False):
        image = pygame.image.load(filename)
        #except pygame.error, message:
         #       raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
#================================================================
 
def main():
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")
 
   
    fondo = imagen("imagenes/fondo.png")      
    mario = imagen("imagenes/mario.png",True)
 
   
    fondo = pygame.transform.scale(fondo, (1000, 400))
   
   
    screen.blit(fondo, (0, 0))
    screen.blit(mario, (100, 304))
   
    pygame.display.flip()
 
 
    # el bucle principal del juego
    while True:
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
   
    return 0
 
 
 
 
if __name__ == '__main__':
    main()