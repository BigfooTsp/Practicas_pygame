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
WIDTH = 32*30
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
    
    global mario, nivel,fondo, enemigos
     
    mario = Personajes.Mario()
    
    nivel= Escenario.Mapa()
    
    nivel.cargarMapa("Nivel1")
    
    fondo = Util.imagen("images/clouds.png", False, True)
   
   
    enemigos=[]
    
    enemigos.append(Personajes.Enemy("goomba",250,True))    
    enemigos.append(Personajes.Enemy("koopa",1500,True))
    enemigos.append(Personajes.Enemy("goomba",1800))    
    enemigos.append(Personajes.Enemy("koopa",2000))
    enemigos.append(Personajes.Enemy("goomba",2100))   
    enemigos.append(Personajes.Enemy("koopa",2500))

    return
 
def Updates():

    global mario
   
    Util.teclado(mario,nivel, WIDTH)    
    #Escenario
      
    #Enemigo()
    #Coliciones()
   
    return
 
 


def Draw():
    global time, nivel
     
    #Escenario y fondo
    nivel._posfondo-=0.3
    
    
    screen.blit(fondo,(nivel._posfondo,0) )
        
    for i in range(nivel._MapaH ):
        for j in range(nivel._MapaW):
            
            pos=nivel._matrizMapa[i][j]-1
            screen.blit(nivel._mapaImagenes[pos],(j*32+nivel._postile,i*32) )
            

        
   
   #Dibujar Mario
   
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
        
     
     
     
    #Dibujar Enemigos
    
    for enemy in enemigos:
           
        if enemy._activo==True:   
            screen.blit(enemy.animacion(mario,WIDTH),(enemy._posX,enemy._posY))        
        else:
            if mario._posAbs<=enemy._posX-500:
                enemy._activo=True
       
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