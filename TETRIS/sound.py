import gamelib

def linea_completa():
	"""
	Reproduce sonido de linea completa
	"""
	gamelib.play_sound("sounds/linea_completa.wav")

def pulsacion():
	"""
	Reproduce sonido de pulsacion de boton(best)
	"""
	gamelib.play_sound("sounds/pulse.wav")

def juego_terminado():
	"""
	Reproduce sonido de finalizacion de juego
	"""
	gamelib.play_sound("sounds/game_over.wav")

def punto():
	"""
	Reproduce sonido de punto nuevo
	"""
	gamelib.play_sound("sounds/point.wav")

def pulsacion_erronea():
	"""
	Reproduce sonido de pulsacion erronea de click
	"""
	gamelib.play_sound("sounds/pulse_error.wav")

def partida_guardada():
	"""
	Reproduce sonido de partida guardada
	"""
	gamelib.play_sound("sounds/save.wav")

def partida_cargada():
	"""
	Reproduce sonido de partida cargada
	"""
	gamelib.play_sound("sounds/load.wav")