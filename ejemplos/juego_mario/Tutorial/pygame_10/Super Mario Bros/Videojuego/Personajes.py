import sys, pygame

class Mario(object):
    
    _posX=0
    _posY=420
    _frame=0
    _images=[]
    _con=0
    _direc=True
    _salto=False
    _subida=True
    
    def __init__(self):
        tileset=pygame.image.load("images/Mario y Luigi.png").convert()
        
        color = tileset.get_at((0,0))
        
        tileset.set_colorkey(color)
        
        self._images.append(tileset.subsurface((1,17,16,16)))
        
        self._images.append(tileset.subsurface((18,17,16,16)))        
        
        self._images.append(tileset.subsurface((35,17,16,16)))
        
        self._images.append(tileset.subsurface((69,17,16,16)))                
        
        for i in range(len(self._images)):
            self._images[i]=pygame.transform.scale2x(self._images[i])
     
        return 
    
    def imagenMario(self):
        
        if self._frame==len(self._images)-1:
            self._frame=0 
        
        return self._images[self._frame]        
     
    def saltar(self):
        
        if self._subida==True:
            self._posY-=4
            if self._direc==True:
                self._posX+=1
            else:
                self._posX-=1
            
            
        if self._posY<=310:
            self._subida=False
            
            
        if self._subida==False:
            self._posY+=4            
            if self._direc==True:
                self._posX+=1
            else:
                self._posX-=1
            
        if self._subida==False and self._posY>=420:
            self._subida=True
            self._salto=False
            self._frame=0
        
            

        
        
        
    


        return   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        