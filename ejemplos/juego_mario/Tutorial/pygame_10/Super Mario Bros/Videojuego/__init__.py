#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame
from pygame.locals import *
from time import clock
import os

import Util 
import Personajes
import Escenario

 
#Tamaño  la pantalla
WIDTH = 32*40
HEIGHT = 32*15

 
def Initialize():
    
    global clock, screen, nivel
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Super Mario Bros")
    clock = pygame.time.Clock()
    
    
    
   
    return screen
 
def LoadContent():
    
    global mario, nivel,fondo
     
    mario = Personajes.Mario()
    
    nivel= Escenario.Mapa()
    
    nivel.cargarMapa("Nivel1")
    
    fondo = Util.imagen("images/clouds.png", False, True)
   
    return
 
def Updates():

    global mario
   
    Util.teclado(mario)    
    #Escenario
      
    #Enemigo()
    #Coliciones()
   
    return
 
 
 
def Draw():
    global time
     
    screen.blit(fondo,(0,0) )
        
    for i in range(nivel._MapaH ):
        for j in range(nivel._MapaW):
            
            pos=nivel._matrizMapa[i][j]
            screen.blit(nivel._mapaImagenes[pos-1],(j*32,i*32) )
            

        
   
    if mario._salto==False:
        
        if mario._direc==True:
            screen.blit(mario.imagenMario(),(mario._posX,mario._posY))
        else:
            mario_inv=pygame.transform.flip(mario.imagenMario(),True,False);
            screen.blit(mario_inv,(mario._posX,mario._posY))
    else:        
        mario.saltar()
        if mario._direc==True:
            screen.blit(mario._images[3],(mario._posX,mario._posY))
        else:
            mario_inv=pygame.transform.flip(mario._images[3],True,False);
            screen.blit(mario_inv,(mario._posX,mario._posY))
        
            
        
            
    
       
    pygame.display.flip()
   
    return
 
 
 
 
def main():
   
    Initialize()
   
    LoadContent()
   
    global time
    
    
     
    while True:
       
        time = clock.tick(60)
       
       
     
        Updates()
       
        Draw()
       
       
       
        #if gameOver==True
            #UnLoadContent()
         
     
       
   
   
    return
 
 
 
 
if __name__ == '__main__':
    main()