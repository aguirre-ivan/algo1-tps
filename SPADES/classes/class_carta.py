CARTAS = 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 1
PALOS = "D", "C", "P", "T"

class Carta:
	def __init__(self, numero=None, palo=None):
		"""
		Recibe numero entero y palo en formato str
		"""
		self.palo = palo
		self.numero = numero

	def __gt__(self, otra):
		"""
		Una carta es mayor a otra numericamente si esta primera en el orden de CARTAS
		"""
		i_self = 0
		i_otra = 0
		for i in range(len(CARTAS)):
			if self.numero == CARTAS[i]:
				i_self = i
			if otra.numero == CARTAS[i]:
				i_otra = i
		return i_self > i_otra

	def carta_nula(self):
		"""
		Verifica si una carta es nula, es decir si su palo y numero son None
		"""
		return self.palo == None and self.numero == None

	def __eq__(self, otra):
		"""
		Dos cartas son iguales si tienen el mismo palo y el mismo numero
		"""
		return self.palo == otra.palo and self.numero == otra.numero

	def mismo_palo(self, otra):
		"""
		Recibe otra carta del mismo tipo, devuelve True si son del mismo palo, False si son distinto.
		"""
		return self.palo == otra.palo