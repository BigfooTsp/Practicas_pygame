# -*- coding: utf-8 -*-
class Nodo:
	def __init__(self, pos=[0, 0], padre=None):
		self.pos = pos
		self.padre = padre
		self.h = distancia(self.pos, pos_f)
		
		if self.padre == None:
			self.g = 0
		else:
			self.g = self.padre.g + 1
		self.f = self.g + self.h

class AStar:
	def __init__(self, mapa):
		
		self.mapa = mapa
		globals()["pos_f"] = buscarPos(3, self.mapa)
		
		# Nodos de inicio y fin.
		self.inicio = Nodo(buscarPos(2, mapa))
		self.fin = Nodo(buscarPos(3, mapa))
		
		# Crea las listas abierta y cerrada.
		self.abierta = []
		self.cerrada = []
		
		# Añade el nodo inicial a la lista cerrada.
		self.cerrada.append(self.inicio)
		
		# Añade vecinos a la lista abierta
		self.abierta += self.vecinos(self.inicio)
		
		# Buscar mientras objetivo no este en la lista cerrada.
		while self.objetivo():
			if not self.abierta:
				break
			self.buscar()
		
		if not self.abierta:
			self.camino = -1
		else:	
			self.camino = self.camino()
			
	
	# Devuelve una lista con los nodos vecinos transitables.	
	def vecinos(self, nodo):
		vecinos = []
		try:
			if self.mapa[nodo.pos[0] + 1][nodo.pos[1]] != 1:
				vecinos.append(Nodo([nodo.pos[0] + 1, nodo.pos[1]], nodo))
			if self.mapa[nodo.pos[0] - 1][nodo.pos[1]] != 1:
				vecinos.append(Nodo([nodo.pos[0] - 1, nodo.pos[1]], nodo))
			if self.mapa[nodo.pos[0]][nodo.pos[1] - 1] != 1:
				vecinos.append(Nodo([nodo.pos[0], nodo.pos[1] - 1], nodo))
			if self.mapa[nodo.pos[0]][nodo.pos[1] + 1] != 1:
				vecinos.append(Nodo([nodo.pos[0], nodo.pos[1] + 1], nodo))
		except Exception, e:
			pass				
		finally:
			return vecinos


		
	
	# Pasa el elemento de f menor de la lista abierta a la cerrada. 	
	def f_menor(self):
		a = self.abierta[0]
		n = 0
		for i in range(1, len(self.abierta)):
			if self.abierta[i].f < a.f:
				a = self.abierta[i]
				n = i
		self.cerrada.append(self.abierta[n])
		del self.abierta[n]
		
	
	# Comprueba si un nodo está en una lista.	
	def en_lista(self, nodo, lista):
		for i in range(len(lista)):
			if nodo.pos == lista[i].pos:
				return 1
		return 0
	
	
	# Gestiona los vecinos del nodo seleccionado.	
	def ruta(self):
		for i in range(len(self.nodos)):
			if self.en_lista(self.nodos[i], self.cerrada):
				continue
			elif not self.en_lista(self.nodos[i], self.abierta):
				self.abierta.append(self.nodos[i])
			else:
				if self.select.g + 1 < self.nodos[i].g:
					for j in range(len(self.abierta)):
						if self.nodos[i].pos == self.abierta[j].pos:
							del self.abierta[j]
							self.abierta.append(self.nodos[i])
							break
	
	# Analiza el último elemento de la lista cerrada.
	def buscar(self):
		self.f_menor()
		self.select = self.cerrada[-1]
		self.nodos = self.vecinos(self.select)
		self.ruta()
	
	# Comprueba si el objetivo objetivo está en la lista abierta.
	def objetivo(self):
		for i in range(len(self.abierta)):
			if self.fin.pos == self.abierta[i].pos:
				return 0
		return 1
	
	# Retorna una lista con las posiciones del camino a seguir.
	def camino(self):
		for i in range(len(self.abierta)):
			if self.fin.pos == self.abierta[i].pos:
				objetivo = self.abierta[i]
				
		camino = []
		while objetivo.padre != None:
			camino.append(objetivo.pos)
			objetivo = objetivo.padre
			
		camino.reverse()
		return camino


# Devuelve la posición de "x" en una lista.
def buscarPos(x, mapa):
	for f in range(len(mapa)):
		for c in range(len(mapa[0])):
			if mapa[f][c] == x:
				return [f, c]
	return 0

# Distancia entre dos puntos.
def distancia(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1]) #Valor absoluto.

