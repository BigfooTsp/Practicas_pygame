#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lo de arriba obligatorio en python 27

import sys, pygame
from pygame.locals import *

WIDHT = 900
HEIGHT = 500
MposX = 100

#===========================================================
#=================IMAGEN====================================

def imagen(filename, transparent = False): # Ruta de archivo, transparente
	''' El formato png acepta transparente (en blanco en 
	la imagen)'''

	try : image = pygame.image.load(filename) # variable para cargar imagen (dentro de captura de error)
	except pygame.error, message:
		raise SystemExit, message

	image = image.convert() # convertimos imagen a formato interno de pygame

	if transparent:
		color = image.get_at((0,0)) # Color de la parte superior izquierda de la imagen (blanco en mario)
		image.set_colorkey(color, RLEACCEL) # ese será el color transparente.
	return image

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
		#salto. Requiere una conversión de parábola.
		MposX-=2

	return

#====================== MAIN ====================================
#================================================================

def main():
	pygame.init() # Inicializa variables

	screen = pygame.display.set_mode((WIDHT, HEIGHT)) # definimos pantalla
	pygame.display.set_caption("Mario")

	fondo = imagen("imagenes/fondo.png") # Pasamos la imagen por función imagen())
	mario = imagen("imagenes/mario.png",True) # Mario con transparencia

	clock = pygame.time.Clock() # reloj para reducir la velocidad del bucle

	##### Bucle principal del juego #####

	while True:

		time = clock.tick(60)

		teclado()

		fondo = pygame.transform.scale(fondo, (1000, 400)) # escala imagen de fondo
		screen.blit(fondo, (0,0)) # pintamos fondo en posición 0,0
		screen.blit(mario, (MposX, 304)) # pintamos a mario (desde izq, desde arriba)
		# LA variable MposX es la que se controla con las flechas X

		pygame.display.flip()

		# Posibles entradas de teclado y mouse:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
	return 0

#================================================================

if __name__ == '__main__':
	main()










