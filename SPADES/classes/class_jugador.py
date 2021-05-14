class Jugador:
	def __init__(self, nombre):
		self.nombre = nombre
		self.mano = []
		self.puntos = 0
		self.apuesta = -1
		self.bazas = 0
		
	def sumar_bazas(self):
		"""
		Suma una baza
		"""
		self.bazas += 1
	
	def reiniciar_apuesta(self):
		"""
		Reinicia la puesta del jugador (-1)
		"""
		self.apuesta = -1

	def reiniciar_bazas(self):
		"""
		Reinicia las bazas a 0
		"""
		self.bazas = 0
		
	def asignar_apuesta(self, apuesta):
		"""
		Recibida una apuesta la asigna a self.apuesta
		"""
		self.apuesta = apuesta

	def limpiar_mano(self):
		"""
		Limpia la mano de cartas
		"""
		self.mano = []

	def agregar_carta(self, carta):
		"""
		Recibe una carta del tipo Carta y la agrega a su mano
		"""
		self.mano.append(carta)

	def sacar_carta(self, carta):
		"""
		Recibe una carta del tipo Carta y la quita de su mano, la devuelve.
		Condicion: la carta debe estar en la mano
		"""
		self.mano.remove(carta)
		return carta

	def sumar_puntos(self, puntos):
		"""
		Recibe puntos (int) y los suma
		"""
		self.puntos += puntos