import gamelib
from classes.class_carta import Carta
from classes.class_juego import Juego
from classes.class_jugador import Jugador
from classes.class_ronda import Ronda
from classes.class_vuelta import Vuelta
import classes.class_carta
import classes.class_juego
from random import randrange

PALOS = classes.class_carta.PALOS
CARTAS = classes.class_carta.CARTAS
RONDA_FINAL = classes.class_juego.RONDA_FINAL

def mazo_completo():
	"""
	No recibe nada, devuelve una lista de Cartas representando el mazo completo
	"""
	mazo = []

	for numero in CARTAS:
		for palo in PALOS:
			mazo.append(Carta(numero, palo))

	return mazo

def repartir_cartas(juego, mazo):
	"""
	Recibe un mazo y un estado de juego.
	Devuelve una tupla, (juego, mazo_sobrante)
	"""
	return juego, juego.repartir(mazo)

def crear_juego(jugadores):
	"""
	Recibe una lista con cada nombre de jugador y crea y devuelve un nuevo estado de juego del tipo Juego.
	"""
	juego = Juego(jugadores)
	juego, mazo_sobrante = repartir_cartas(juego, mazo_completo())
	juego = carta_triunfo(juego, mazo_sobrante)
	return juego

def juego_actualizar(juego):
	"""
	Recibe un estado de juego y lo actualiza avanzando una vuelta.
	Devuelve el nuevo estado de juego.
	Precondicion: el juego no debe estar terminado.
	"""
	juego = vuelta(juego)
	if juego.ronda.vuelta.numero_vuelta == juego.ronda.numero_ronda:
		return avanzar_ronda(juego)
	return avanzar_vuelta(juego)

def bazas_a_0(juego):
	"""
	Recibido un estado de juego, reinicia las bazas de todos los jugadores a 0
	"""
	for jugador in juego.jugadores:
		juego.jugadores[jugador].reiniciar_bazas()
	return juego

def avanzar_ronda(juego):
	"""
	Avanza de ronda en el estado de juego, devuelve un nuevo estado de juego.
	"""
	juego = verificar_puntuaciones(juego)
	juego = quitar_apuestas(juego)

	juego.ronda.vuelta.reiniciar_vueltas()
	
	juego = bazas_a_0(juego)

	juego.siguiente_ronda()

	juego, mazo_sobrante = repartir_cartas(juego, mazo_completo())

	if juego.ronda.numero_ronda == RONDA_FINAL:
		carta_corazones = Carta(1, "C")
		juego = carta_triunfo(juego, [carta_corazones])
	else:
		juego = carta_triunfo(juego, mazo_sobrante)
	return juego

def avanzar_vuelta(juego):
	"""
	Avanza la vuelta, devuelve el nuevo estado de juego.
	Preconodicion, las vueltas no deben superar al numero de rondas
	"""
	juego.ronda.vuelta.avanzar()
	return juego

def vuelta(juego):
	"""
	Recibido un estado de juego, realiza la comprobacion final de la vuelta.
	Precondicion, todas las cartas de la "vuelta" deben estar sobre la mesa
	Aclaracion: No avanza la vuelta, eso lo hace la funcion avanzar_vuelta(juego)
	"""
	jugador_ganador = determinar_ganador_mano(juego)
	gamelib.say(f"EL GANADOR DE LA BAZA FUE\n{jugador_ganador}")
	juego.jugadores[jugador_ganador].sumar_bazas()
	juego.turno_actual = jugador_ganador
	return juego

def tirar_carta(juego, carta):
	"""
	Pone la carta en mesa del jugador, cambia turno y saca dicha carta de la mano del jugador.
	Si es el primer turno, la carta se agrega al atributo de la vuelta del juego carta_mesa
	Precondicion: la carta debe estar en la mano del jugador del turno actual. 
	"""
	turno_actual = juego.turno_actual
	juego.jugadores[turno_actual].mano.remove(carta)
	juego.ronda.vuelta.agregar_carta_mesa(carta, turno_actual)
	cambiar_turno(juego)

	return juego

def carta_triunfo(juego, mazo):
	"""
	Recibido un estado de juego y un mazo sobrante (lista de Cartas), saca una al azar y actualiza la carta triunfo del estado de juego
	Precondicion: la lista no puede estar vacia, 
	"""
	if len(mazo) == 1:
		i_carta = 0
	else:
		i_carta = randrange(len(mazo))
	carta = mazo[i_carta]
	juego.ronda.asignar_carta_triunfo(carta)
	return juego

def pedir_apuesta(juego, apuesta):
	"""
	Recibe una apuesta int, la asigna al jugador del turno actual del juego.
	Cambia a turno siguiente
	Devuelve un nuevo estado de juego
	"""
	turno = juego.turno_actual
	juego.jugadores[turno].apuesta = apuesta
	juego = cambiar_turno(juego)
	
	return juego

def cambiar_turno(juego):
	"""
	Recibido un estado de juego, cambia el turno al siguiente y devuelve unn nuevo estado de juego.
	"""
	turno = juego.turno_actual
	juego.turno_actual = juego.siguiente_turno[turno]
	return juego

def todos_apostaron(juego):
	"""
	Recibido un estado de juego verifica si todos apostaron, en caso positivo devuelve True, en caso contrario, devuelve False
	"""
	for jugador in juego.jugadores:
		if juego.jugadores[jugador].apuesta == -1:
			return False
	return True

def quitar_apuestas(juego):
	"""
	Recibido un estado de juego reinicia todas las apuestas de los jugadores.
	"""
	for jugador in juego.jugadores:
		juego.jugadores[jugador].apuesta = -1
	return juego

def verificar_puntuaciones(juego):
	"""
	Recibido un estado de juego verifica si algun jugador coincidio su numero de bazas. Verifica todas las puntuaciones
	Devuelve un nuevo estado de juego
	"""
	ronda = juego.ronda.numero_ronda
	for jugador in juego.jugadores:
		apuesta = juego.jugadores[jugador].apuesta
		bazas = juego.jugadores[jugador].bazas
		if apuesta == bazas:
			juego.jugadores[jugador].puntos += 10 + 5 * bazas
			if apuesta == 0:
				juego.jugadores[jugador].puntos += 5 * ronda
	return juego

def juego_terminado(juego):
	"""
	Recibido un estado de juego, devuelve True si el juego esta terminado, False si no.
	"""
	return juego.ronda.numero_ronda == RONDA_FINAL + 1

def ganador(juego):
	"""
	Recibido un estado de juego, devuelve el jugador ganador.
	"""
	jugador_ganador = juego.turno_actual #Empiezo con un turno ganado

	for jugador in juego.jugadores:
		if juego.jugadores[jugador].puntos > juego.jugadores[jugador_ganador].puntos:
			jugador_ganador = jugador
	return jugador_ganador

def tiene_carta_mesa(juego):
	"""
	Recibido un estado de juego, devuelve True si el jugador del turno actual tiene una carta del mismo palo que el palo de carta de apertura en su mano. False en caso contrario
	"""
	turno_actual = juego.turno_actual
	for carta in juego.jugadores[turno_actual].mano:
		if carta.mismo_palo(juego.ronda.vuelta.carta_mesa):
			return True
	return False

def tiene_carta_triunfo(juego):
	"""
	Recibido un estado de juego, devuelve True si el jugador del turno actual tiene una carta del palo triunfo, False en caso contrario.
	"""
	turno_actual = juego.turno_actual
	for carta in juego.jugadores[turno_actual].mano:
		if carta.mismo_palo(juego.ronda.carta_triunfo):
			return True
	return False

def carta_mayor_palo(juego, carta):
	"""
	Recibido un estado de juego, devuelve True si la carta elegida es la mayor del palo en la mano
	"""
	turno_actual = juego.turno_actual
	for c in juego.jugadores[turno_actual].mano:
		if carta.mismo_palo(c):
			if c > carta:
				return False
	return True

def carta_valida(juego, carta):
	"""
	Recibido un estado de juego y una carta, devuelve True si la carta es valida para tirar, False si no lo es.
	"""
	turno_actual = juego.turno_actual
	n_cartas_mano = len(juego.jugadores[turno_actual].mano)
	if juego.ronda.vuelta.mesa_vacia(): #Si es el primero en tirar
		return True

	carta_apertura = juego.ronda.vuelta.carta_mesa 
	carta_triunfo = juego.ronda.carta_triunfo

	if carta.mismo_palo(carta_apertura):
		if carta_mayor_palo(juego, carta):
			return True
		return False

	if not tiene_carta_mesa(juego):
		if carta.mismo_palo(carta_triunfo):
			if carta_mayor_palo(juego, carta):
				return True
			return False
		if not tiene_carta_triunfo(juego):
			return True

	return False

def le_gana(juego, carta1, carta2):
	"""
	Recibido un estado de juego y dos cartas las compara, si carta1 es mayor a carta2 devuelve True, sino devuelve False
	Aclaracion: existe la posibilidad que la carta sea la misma (ya que puede coincidir con el caso base en determinar_ganador_mano), en ese caso devuelve false.
	"""
	if carta1 == carta2:
		return False

	palo_triunfo = juego.ronda.carta_triunfo.palo
	palo_apertura = juego.ronda.vuelta.carta_mesa.palo

	if carta1.palo == palo_triunfo:
		if carta2.palo == palo_triunfo:
			return carta1 > carta2
		return True

	if carta1.palo == palo_apertura:
		if carta2.palo == palo_triunfo:
			return False
		if carta2.palo == palo_apertura:
			return carta1 > carta2

	#La carta1 es de uno de los otros dos palos
	if carta2.palo == palo_triunfo or carta2.palo == palo_apertura:
		return False

	#La carta2 tambien es uno de los otros dos palos
	return carta1 > carta2


def determinar_ganador_mano(juego):
	"""
	Recibido un estado de juego, determina quien fue el ganador de la mano.
	Devuelve el nombre del jugador.
	"""
	jugador_ganador = juego.turno_actual
	carta_ganadora = juego.ronda.vuelta.cartas_puestas[jugador_ganador]

	for jugador in juego.ronda.vuelta.cartas_puestas:
		carta = juego.ronda.vuelta.cartas_puestas[jugador]
		if le_gana(juego, carta, carta_ganadora):
			carta_ganadora = carta
			jugador_ganador = jugador

	return jugador_ganador