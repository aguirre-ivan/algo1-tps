from classes.class_vuelta import Vuelta
from classes.class_carta import Carta

class Ronda:
	def __init__(self):
		self.numero_ronda = 1
		self.carta_triunfo = Carta()
		self.vuelta = Vuelta()

	def asignar_carta_triunfo(self, carta_triunfo):
		"""
		Recibe una carta y la asigna a la carta triunfo
		"""
		self.carta_triunfo = carta_triunfo

	def no_hay_carta_triunfo(self):
		"""
		Si self.carta_triunfo == -1, devuelve True, en caso contrario devuelve False
		"""
		return self.carta_triunfo.carta_nula()

	def avanzar(self):
		"""
		Avanza a la siguiente ronda
		"""
		self.carta_triunfo = Carta()
		self.numero_ronda += 1