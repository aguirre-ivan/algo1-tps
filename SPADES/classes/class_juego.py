from classes.class_jugador import Jugador
from classes.class_ronda import Ronda
from classes.class_carta import Carta
from random import randrange

RONDA_FINAL = 13

class Juego:
	def __init__(self, jugadores):
		"""
		Recibe una lista jugadores, y le da los siguientes atributos:
		self.ronda del objeto tipo Ronda
		self.jugadores el cual es un diccionario con claves de nombre y valores un objeto del tipo Jugador()
		"""
		self.ronda = Ronda()
		self.jugadores = {}

		siguiente_turno = {}
		for i_jugador in range(len(jugadores)): #Creo un diccionario con los siguientes turnos de cada jugador
			if i_jugador == len(jugadores) - 1:
				siguiente_turno[jugadores[i_jugador]] = jugadores[0]
			else:
				siguiente_turno[jugadores[i_jugador]] = jugadores[i_jugador+1]

		self.siguiente_turno = siguiente_turno

		primer_jugador = jugadores[randrange(len(jugadores)-1)]

		self.turno_actual = self.primer_jugador = primer_jugador
		for jugador in jugadores:
			self.jugadores[jugador] = Jugador(jugador)

	def repartir(self, mazo):
		"""
		Reparte self.ronda cartas a cada jugador descontandolas del mazo(lista de Cartas) recibido.
		Devuelve el mazo restante
		El mazo no debe estar vacio y deben alcanzar las cartas para cada jugador.
		Si el numero de ronda se paso de la ronda final es porque no se debe repartir mas, entonces se devuelve el mazo.
		"""
		if self.ronda.numero_ronda > RONDA_FINAL:
			return mazo
		for jugador in self.jugadores:
			for i in range(self.ronda.numero_ronda):
				if len(mazo) == 1:
					i_carta_random = 0
				else:
					i_carta_random = randrange(len(mazo)-1)
				carta_sacada = mazo.pop(i_carta_random)
				self.jugadores[jugador].agregar_carta(carta_sacada)
		return mazo

	def siguiente_ronda(self):
		"""
		Avanza a la siguiente ronda.
		"""
		self.primer_jugador = self.siguiente_turno[self.primer_jugador]
		self.turno_actual = self.primer_jugador
		self.ronda.avanzar()