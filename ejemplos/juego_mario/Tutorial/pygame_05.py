#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *

 
# Constantes
WIDTH = 900
HEIGHT = 500
MposX =300


cont=6
direc=True
i=0
xixf={}#xinicial y xfinal
Rxixf={}
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
    global cont, direc
    
        
    if teclado[K_RIGHT]:
        MposX+=2
        cont+=1
        direc=True
    elif teclado[K_LEFT]:
        MposX-=2
        cont+=1
        direc=False
    elif teclado[K_q]:
        #SALTO
        MposX-=2
    #else :
         #cont=6
        
    return 
    

#===================SPRITE===============================
#========================================================
def sprite():

    global cont
 
    xixf[0]=(0,0,20,41)
    xixf[1]=(22,0,25,41)
    xixf[2]=(47,0,25,41)
    xixf[3]=(73,0,20,41)
    xixf[4]=(93,0,27,41)
    xixf[5]=(120,0,27,41)
    
    Rxixf[0]=(122,0,22,41)
    Rxixf[1]=(96,0,25,41)
    Rxixf[2]=(74,0,22,41)
    Rxixf[3]=(50,0,23,41)
    Rxixf[4]=(24,0,26,41)
    Rxixf[5]=(0,0,25,41)
    
    p=6
    
    global i
        
    if cont==p:
        i=0
    
    if cont==p*2:
        i=1
    
    if cont==p*3:
        i=2
    
    if cont==p*4:
        i=3
    
    if cont==p*5:
        i=4
    
    if cont==p*6:
       i=5
       cont=0
    
    return





def main():
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mario")
    
 
    fondo = imagen("imagenes/fondo.png")
    
          
    mario = imagen("imagenes/sprites_mario.png",True)   
    mario_inv=pygame.transform.flip(mario,True,False);
     
    clock = pygame.time.Clock()
    
      
 
    # el bucle principal del juego
    while True:
        
        time = clock.tick(60)
        
        sprite()
        teclado()
        
       
    
        fondo = pygame.transform.scale(fondo, (1000, 400))
             
        screen.blit(fondo, (0, 0))
        
        if direc==True: 
            screen.blit(mario, ( MposX, 318),(xixf[i]))
    
        if direc==False: 
            screen.blit(mario_inv, ( MposX, 318),(Rxixf[i]))
    
        pygame.display.flip()
        
        
        
        
        # Cerrar la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    return 0



 
if __name__ == '__main__': 
    main()