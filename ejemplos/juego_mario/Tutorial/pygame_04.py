#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *

 
# Constantes
WIDTH = 900
HEIGHT = 500
MposX =100


#===========================================================
#=================IMAGEN====================================

def imagen(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
#================================================================ 

#======================TECLADO===================================
#================================================================
def teclado():
    teclado = pygame.key.get_pressed()
     
    global MposX
        
    if teclado[K_RIGHT]:
        MposX+=2
    if teclado[K_LEFT]:
        MposX-=2
    if teclado[K_q]:
        #SALTO
        MposX-=2
        
    return 
    




def main():
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")
 
    fondo = imagen("imagenes/fondo.png")       
    mario = imagen("imagenes/mario.png",True)
     
    clock = pygame.time.Clock()
    
      
 
    # el bucle principal del juego
    while True:
        
        time = clock.tick(60)
        
        teclado()
        
 
    
        fondo = pygame.transform.scale(fondo, (1000, 400))       
        screen.blit(fondo, (0, 0))
        screen.blit(mario, ( MposX, 304))
    
        pygame.display.flip()
        
        
        
        
        # Posibles entradas del teclado y mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    return 0



 
if __name__ == '__main__': 
    main()