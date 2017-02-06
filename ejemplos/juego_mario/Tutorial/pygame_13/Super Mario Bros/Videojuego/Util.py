import pygame, sys
from pygame.locals import *
from Videojuego import Personajes
import Videojuego

clock = pygame.time.Clock()

def imagen(filename, transparent=False,expandir=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
                
        if expandir:
            image=pygame.transform.scale2x(image)
                
        return image

mitad=False
def teclado(mario,nivel,WIDTH):
   

   
    teclado = pygame.key.get_pressed()
    global mitad, blink_posY
    
    if mario._vida==True:
    
        if teclado[K_q] and mario._salto==False:
            mario._salto=True
            mario._subida=True
            
        
        if teclado[K_RIGHT]:
            
            if mario._posX<WIDTH/2+30:
                mario._posX+=2
                
            else:           
                nivel._postile-=2
                nivel._posEnemy+=1
            
            mario._alto=False     
            mario._con+=1
            mario._direc=True
            mario._posAbs+=1
            
               
        elif teclado[K_LEFT]:
            mario._posX-=2
            mario._con+=1
            mario._direc=False
            mario._posAbs-=1
            
        else:
            mario._frame=0
            mario._alto=True
        
        
        if mario._con>=6:        
            mario._frame+=1
            mario._con=0
    
    
        
      
    # Cerrar la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
   
       
    return

def colision(mario,enemigos):
    
    if mario._posY==420:
        
        for i in range(len(enemigos)):
            
            if mario._posX+32>enemigos[i]._posX and mario._posX+32<enemigos[i]._posX+32:
                mario._vida=False
                mario._posMuerte=mario._posX                
                
                return True
    
    return False