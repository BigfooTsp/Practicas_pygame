#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Lo de arriba obligatorio en python 27

'''================================================================
 Práctica de tutorial de pygame youtube (hackerseingenieros)
 python 2.7 y pygame 1.9
#================================================================'''
,
# Módulos
import sys, pygame
from pygame.locals import *
#===================== VARIABLES CONSTANTES =====================
#================================================================

WIDHT = 900
HEIGHT = 500
MposX = 100 

cont=6
direc=True
i=0
xixf = {} # xinicial y xfinal
Rxixf = {}

#===================== IMAGEN ===================================
#================================================================

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

#===================== TECLADO ==================================
#================================================================

def teclado():

	teclado = pygame.key.get_pressed() # variable que captura teclado y get_presed devuelve esas teclas

	global MposX
	global cont, direc

	if teclado[K_RIGHT]:
		MposX += 2
		cont += 1
		direc = True
	if teclado[K_LEFT]:
		MposX-=2
		cont += 1
		direc = False
	if teclado[K_q]:
		#salto. Requiere una conversión de parábola.
		MposX-=2

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
	p=6

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

	screen = pygame.display.set_mode((WIDHT, HEIGHT)) # definimos pantalla
	pygame.display.set_caption("Mario")

	fondo = imagen("imagenes/fondo.png") # Pasamos la imagen por función imagen())
	mario = imagen("imagenes/sprites_mario.png",True) # Mario con transparencia
	mario_inv = pygame.transform.flip(mario,True,False) 
	# Inversos de imagen        [ arch, invertir eje x, invertir eje ]

	clock = pygame.time.Clock() # reloj para reducir la velocidad del bucle (cada 60ms)

	##### Bucle principal del juego #####

	while True:
		# reloj a 60 ms
		time = clock.tick(60)

		# funciones
		sprite()
		teclado()

		# configurando pintado de fondo.
		fondo = pygame.transform.scale(fondo, (1000, 400)) # escala imagen de fondo
		screen.blit(fondo, (0,0)) # pintamos fondo en posición 0,0
		
		# Configurando pinatado de Mario:		
			# control del sprite mostrado mediante xixf[i]
		if direc == True: # (Hacia la derecha)
			screen.blit(mario, (MposX, 318), (xixf[i])) 
			#         [archivo (coordenada x, y), pixeles del archivo a imprimir]
		if direc == False: # (Hacia la izquierda)
			screen.blit(mario_inv, (MposX, 318), (Rxixf[i]))

		# Pinta pantalla
		pygame.display.flip()

		# Posibles entradas de teclado y mouse:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
	return 0

#================================================================

if __name__ == '__main__':
	main()










