import pygame
from pygame.locals import *

def cargar_imagen(filename, transparent=False, pixel=(0, 0)):
    """ Carga una imagen y estblece un color como transparente si se desea. """
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert()
    if transparent:
        color = image.get_at(pixel)
        image.set_colorkey(color, RLEACCEL)
    return image

def cortar_tileset(filename, (w, h), con_None=False):
    """ Corta un tilest y lo almacena en un array unidimensional. """
    image = cargar_imagen(filename, True)
    rect = image.get_rect()
    col = rect.w / w
    fil = rect.h / h
    sprite = []
    if con_None:
        sprite = [None]

    for f in range(fil):
        for c in range(col):
            sprite.append(image.subsurface((rect.left, rect.top, w, h)))
            rect.left += w
        rect.top += h
        rect.left = 0

    return sprite
