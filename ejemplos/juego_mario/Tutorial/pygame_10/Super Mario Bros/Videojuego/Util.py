import pygame, sys
from pygame.locals import *



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

 
def teclado(mario):
   
    teclado = pygame.key.get_pressed()
    
    if teclado[K_q] and mario._salto==False:
        mario._salto=True
        mario._subida=True
        
    
    if teclado[K_RIGHT]:
        mario._posX+=2
        mario._con+=1
        mario._direc=True
       
    elif teclado[K_LEFT]:
        mario._posX-=2
        mario._con+=1
        mario._direc=False
    else:
        mario._frame=0
    
    
    if mario._con>=6:        
        mario._frame+=1
        mario._con=0
    
      
    # Cerrar la ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
   
       
    return
 