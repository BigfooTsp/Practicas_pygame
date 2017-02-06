#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''================================================================
 Práctica de tutorial de pygame youtube (hackerseingenieros)
 python 3.4 y pygame 1.9.2b
#================================================================'''

# Módulos
import sys, pygame
from pygame.locals import *
#from Tkconstants import FALSE
#===================== VARIABLES CONSTANTES =====================
#================================================================

WIDHT = 900
HEIGHT = 500
MposX = 100 
MposY = 318

cont=6
direc=True # (True = derecha, False = iszquierda)
i=0
xixf = {} # xinicial y xfinal
Rxixf = {}

parabola={}
salto = False
salto_Par = False

#===================== IMAGEN ===================================
#================================================================

def imagen(filename, transparent = False): # Ruta de archivo, transparente
	''' El formato png acepta transparente (en blanco en 
	la imagen)'''

	try: 
		image = pygame.image.load(filename) # variable para cargar imagen (dentro de captura de error)
	except pygame.error as message:
		raise SystemExit (message)

	image = image.convert() # convertimos imagen a formato interno de pygame

	if transparent:
		color = image.get_at((0,0)) # Color de la parte superior izquierda de la imagen (blanco en mario)
		image.set_colorkey(color, RLEACCEL) # ese será el color transparente.
	return image

#===================== TECLADO ==================================
#================================================================

def teclado():

	global MposX
	global cont, direc, salto, salto_Par

	teclado = pygame.key.get_pressed() # variable que captura teclado y get_presed devuelve esas teclas

	if teclado[K_q] and teclado[K_RIGHT] and salto_Par == False:
		salto_Par = True
	elif teclado[K_q] and teclado[K_LEFT] and salto_Par == False:
		salto_Par = True

	elif teclado[K_RIGHT] and salto == False and salto_Par == False:
		MposX += 2
		cont += 1
		direc = True
	elif teclado[K_LEFT] and salto == False and salto_Par == False:
		MposX-=2
		cont += 1
		direc = False
	elif teclado[K_q] and salto == False and salto_Par == False:
		salto = True

	else: 
		cont = 6

	return

#===================== SPRITE ===================================
#================================================================
def sprite():

	global cont # ¿[]Hay que redefinir las globales en cada función?

	# diccionario que contiene las divisiones del sprite
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

	# Contador rotatorio de pasos que indica el sprite a mostrar
	p=6 # (Sprite a mostrar)

	global i

	if cont == p:
		i=0
	if cont == p*2:
		i=1
	if cont == p*3:
		i=2
	if cont == p*4:
		i=3
	if cont == p*5:
		i=4
	if cont == p*6:
		i=5
		cont = 0
	return

#====================== MAIN ====================================
#================================================================

def main():
	pygame.init() # Inicializa variables

	##### Variables:
	screen = pygame.display.set_mode((WIDHT, HEIGHT)) # definimos pantalla
	pygame.display.set_caption("Mario")
	fondo = imagen("imagenes/fondo.png") # Pasamos la imagen por función imagen())
	mario = imagen("imagenes/sprites_mario.png",True) # Mario con transparencia
	mario_inv = pygame.transform.flip(mario,True,False) # Inversos de imagen        [ arch, invertir eje x, invertir eje y ]
	
	clock = pygame.time.Clock() # reloj para reducir la velocidad del bucle (cada 60ms)

	global salto_Par
	bajada = False
	bajada_Par = False

	##### Bucle principal del juego #####
	while True:
		
		time = clock.tick(60) # reloj a 60 ms

		sprite()
		teclado()

		###### configurando pintado de fondo.
		fondo = pygame.transform.scale(fondo, (1000, 400)) # escala imagen de fondo
		screen.blit(fondo, (0,0)) # pintamos fondo en posición 0,0

		
		###### Configurando pintado de Mario:	
		global MposX, MposY, salto

		if direc == True and salto == False:
			screen.blit(mario, (MposX, MposY), (xixf[i])) #  [archivo (coordenada x, y), pixeles del archivo a imprimir]
		if direc == False and salto == False:
			screen.blit(mario_inv, (MposX, MposY), (Rxixf[i]))

		# Salto normal:
		if salto == True:

			if direc == True:
				screen.blit(mario, (MposX, MposY), (xixf[4]))
			if direc == False:
				screen.blit(mario_inv, (MposY, MposY), (Rxixf[4]))

			if bajada == False:
				MposY -= 4
			if bajada == True:
				MposY += 4

			if MposY == 186:
				bajada = True
			if MposY == 318:
				bajada = False
				salto = False

		# Salto parabólico:
		if salto_Par == True and direc == True:
			screen.blit(mario, (MposX, MposY), (xixf[4]))

			if bajada_Par == False:  #(arr, der)
				MposY -= 3
				MposX += 2
			if bajada_Par == True: #(ab, der)
				MposY += 3
				MposX += 2

			if MposY == 246:
				bajada_Par = True
			if MposY == 318:
				bajada_Par=False
				salto_Par=False

		elif salto_Par == True and direc == False:
			screen.blit(mario_inv, (MposX, MposY), (Rxixf[4]))

			if bajada_Par == False: #()
				MposY -= 3
				MposX -= 2
			if bajada_Par == True:
				MposY += 3
				MposX -= 2

			if MposY == 246:
				bajada_Par = True
			if MposY == 318:
				bajada_Par = False
				salto_Par = False


		###### Pinta pantalla
		pygame.display.flip()

		# Cerrar ventana:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
	return 0

#================================================================

if __name__ == '__main__':
	main()










