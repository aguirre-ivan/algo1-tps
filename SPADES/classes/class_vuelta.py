from classes.class_carta import Carta

class Vuelta:
	def __init__(self):
		self.carta_mesa = Carta()
		self.ganador_vuelta = None
		self.numero_vuelta = 0
		self.cartas_puestas = {}

	def agregar_carta_mesa(self, carta, jugador):
		"""
		Agrega una carta a la mesa, al diccionaro cartas_puestas, donde usa a la carta como clave y valor al jugador. Si el diccionario esta vacio (la carta tirada es la primera de la mesa) se agrega a self.carta_mesa
		No devuelve nada
		"""
		if self.carta_mesa.carta_nula():
			self.carta_mesa = carta
		self.cartas_puestas[jugador] = carta

	def avanzar(self):
		"""
		Avanza el numero de vuelta, reinicia todas las cartas_puestas en la mesa
		No devuelve nada
		"""
		self.numero_vuelta += 1
		self.cartas_puestas = {}
		self.carta_mesa = Carta()

	def mesa_vacia(self):
		"""
		Devuelve True si no hay cartas en la mesa, si hay cartas devuelve False
		"""
		return not len(self.cartas_puestas)

	def reiniciar_vueltas(self):
		"""
		Reinicia las vueltas a 0. (porque se cambio de ronda). Quita la carta mesa.
		"""
		self.numero_vuelta = 0
		self.carta_mesa = Carta()
		self.cartas_puestas = {}