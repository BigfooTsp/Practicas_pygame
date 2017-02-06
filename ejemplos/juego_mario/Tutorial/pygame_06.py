#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
from Tkconstants import FALSE

 
# Variables
WIDTH = 900
HEIGHT = 500
MposX =300
MposY =318

cont=6
direc=True
i=0
xixf={}#xinicial y xfinal
Rxixf={}

parabola={}
salto = False

salto_Par=False

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
    
    
    global MposX
    global cont, direc,salto, salto_Par
    
     
    
    teclado = pygame.key.get_pressed()
    
    if teclado[K_q] and teclado[K_RIGHT] and salto_Par==False:
        salto_Par=True
    elif teclado[K_q] and teclado[K_LEFT] and salto_Par==False:
        salto_Par=True
         
    elif teclado[K_RIGHT]and salto==False and salto_Par==False:
        MposX+=2
        cont+=1
        direc=True
    elif teclado[K_LEFT]and salto==False and salto_Par==False:
        MposX-=2
        cont+=1
        direc=False
    elif teclado[K_q] and salto==False and salto_Par==False:
        salto=True           
    else :
         cont=6
         
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
    
    global salto_Par  
    bajada=False
    bajada_Par=False
    # el bucle principal del juego
    while True:
        
        time = clock.tick(60)
        
        sprite()
        teclado()
        
       
    
        fondo = pygame.transform.scale(fondo, (1000, 400))
             
        screen.blit(fondo, (0, 0))
        
        
        global MposX,MposY,salto
        
        if direc==True and salto==False: 
            screen.blit(mario, ( MposX, MposY),(xixf[i]))
    
        if direc==False and salto==False: 
            screen.blit(mario_inv, ( MposX, MposY),(Rxixf[i]))
        
        
       #salto normal
        if salto==True:            
            
            if direc==True:
                screen.blit(mario, ( MposX, MposY),(xixf[4]))
            if direc==False:
                screen.blit(mario_inv, ( MposX, MposY),(Rxixf[4]))   
            
            if bajada==False:
                MposY-=4               
                
            if bajada==True:
                MposY+=4               
            
            if MposY==186:
                bajada=True
            
            if MposY==318:
                bajada=False
                salto=False
        #==============================   
        
        #SALTO PARABOLICO
        if salto_Par==True and direc==True:            
            
            screen.blit(mario, ( MposX, MposY),(xixf[4]))
            
            if bajada_Par==False:
                MposY-=3
                MposX+=2
                
            if bajada_Par==True: 
                MposY+=3
                MposX+=2
            
            if MposY==246:
                bajada_Par=True
            
            if MposY==318:
                bajada_Par=False
                salto_Par=False
        elif salto_Par==True and direc==FALSE:            
            
            screen.blit(mario_inv, ( MposX, MposY),(Rxixf[4]))
            
            if bajada_Par==False:
                MposY-=3
                MposX-=2
                
            if bajada_Par==True:
                MposY+=3
                MposX-=2
            
            if MposY==246:
                bajada_Par=True
            
            if MposY==318:
                bajada_Par=False
                salto_Par=False   
    
        pygame.display.flip()
        
        
        
        
        # Cerrar la ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
    return 0



 
if __name__ == '__main__': 
    main()