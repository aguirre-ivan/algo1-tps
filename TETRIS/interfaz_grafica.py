import tetris
import gamelib

LADO_CELDA = 30
ALTO_JUEGO, ANCHO_JUEGO = LADO_CELDA * tetris.ALTO_JUEGO, LADO_CELDA * tetris.ANCHO_JUEGO 
ALTO_VENTANA = ALTO_JUEGO + 2 * LADO_CELDA
ANCHO_VENTANA = ANCHO_JUEGO + LADO_CELDA * 6
BORDE = 1
SEPARACION_BOTONES = 3

GUARDAR = "save"
CARGAR = "load"
BEST = "best"
SCORE = "score"
BOTONES = [GUARDAR, CARGAR, BEST, SCORE]

def pixel_a_cartesiano(x, y):
    """
    Recibidas coordenadas en pixeles las devuelve en cartesianas
    """
    return x // LADO_CELDA, y // LADO_CELDA

def dibujar_celda(lado_celda, x, y, color):
	"""
	Recibe coordenadas cartesianas, un lado de celda en pixeles, color y dibuja la celda con el color indicado
	"""
	x1 = x * lado_celda 
	y1 = y * lado_celda
	x2 = x1 + lado_celda
	y2 = y1 + lado_celda
	gamelib.draw_rectangle(x1, y1, x2, y2, fill = color)

def celdas_fijas():
	"""
	No recibe nada, devuelve un conjunto con todas las coordeanadas de las celdas fijas (fondo)
	"""
	bordes_fijos = set()
	#Transformo a cartesiano
	ancho_ventana, alto_ventana = pixel_a_cartesiano(ANCHO_VENTANA, ALTO_VENTANA)
	ancho_juego, alto_juego = pixel_a_cartesiano(ANCHO_JUEGO + LADO_CELDA, ALTO_JUEGO + LADO_CELDA)

	for y in range(alto_ventana):
		bordes_fijos.add((0, y),)
		bordes_fijos.add((ancho_juego, y),)
		bordes_fijos.add((ancho_ventana - BORDE, y),)

	for x in range(ancho_juego, ancho_ventana):
		filas = [3, 6, 9, 12, 13]
		for i in filas:
			bordes_fijos.add((x, BORDE * i))

	for x in range(ancho_ventana):
		bordes_fijos.add((x, 0),)
		bordes_fijos.add((x, alto_ventana - BORDE),)

	return bordes_fijos

def dibujar_borde(color):
	"""
	Recibe un color y dibuja las celdas de los bordes fijos en dicho color
	"""
	bordes = celdas_fijas()
	for x, y in bordes:
		dibujar_celda(LADO_CELDA, x, y, color)

def dibujar_pieza(pieza, color):
	"""
	Recibe una pieza, y la dibuja 
	"""
	for (x, y) in pieza:
		dibujar_celda(LADO_CELDA, x + BORDE, y + BORDE, color)

def dibujar_superficie_consolidada(juego, color):
	"""
	Recibido un estado de juego y un color dibuja la superficie consolidada
	"""
	tablero = tetris.tablero(juego)
	for y in range(len(tablero)):
		for x in range(len(tablero[y])):
			if tablero[y][x] == tetris.SUPERFICIE:
				dibujar_celda(LADO_CELDA, x + BORDE, y + BORDE, color)

def posicion_boton(factor_n):
	"""
	Recibido un valor n (numero) , devuelve las coordenadas x1, y1, x2, y2 (en pixeles) entre las que se encuentra el boton en forma de rectangulo.
	Siendo
	x1, y1 = (ANCHO_JUEGO + 2 * LADO_CELDA, factor_n * LADO_CELDA)
	Y las dimensiones del boton: (largo = 3*LADO_CELDA, alto = 2*LADO_CELDA)
	"""
	x1 = ANCHO_JUEGO + 2 * LADO_CELDA
	y1 = LADO_CELDA * factor_n
	x2 = x1 + 3 * LADO_CELDA 
	y2 = y1 + 2 * LADO_CELDA
	return x1, y1, x2, y2

def tocar_boton(botones, x, y):
	"""
	Recibida una lista de 4 botones, y coordenadas x, y en pixeles. Devuelve en str el nombre del boton que se toco, si no toco ninguno o toco en la casilla SCORE no devuelve nada
	Utiliza la funcion posicion_boton()
	Los botones empiezan en n = BORDE
	"""
	n = BORDE
	for boton in botones:
		if boton == SCORE:
			return
		x1, y1, x2, y2 = posicion_boton(n)
		if x1 < x < x2 and y1 < y < y2:
			return boton
		n += SEPARACION_BOTONES

def dibujar_boton(boton, n):
	"""
	Recibido un tipo de boton en formato str. y un numero entero de boton n, inserta la imagen "img/{boton}.gif" de 90px60p en la posicion (ANCHO_JUEGO + 2 * LADO_CELDA, n * LADO_CELDA).
	Utiliza la funcion posicion_boton()
	Aclaracion: la imagen DEBE existir.
	"""
	x_inicial, y_inicial, _, _ = posicion_boton(n)

	gamelib.draw_image(f"img/{boton}.gif", x_inicial, y_inicial)


def escribir_puntuacion(puntuacion, n):
	"""
	Recibida una puntuacion tipo str, y un numero n(numero boton) tipo int, escribe la puntuacion en la posicion (ANCHO_JUEGO + 2 * LADO_CELDA, n * LADO_CELDA) + factores (centrado_x, centrado_y)
	"""
	centrado_x = LADO_CELDA * 3 / 2
	centrado_y = LADO_CELDA
	x = ANCHO_JUEGO + 2 * LADO_CELDA + centrado_x
	y = n * LADO_CELDA + centrado_y
	gamelib.draw_text(puntuacion, x, y, size=LADO_CELDA // 2, fill="turquoise")

def dibujar_botones(botones, puntuacion):
	"""
	Recibida una lista de 4 botones los dibuja en las posiciones disponibles, utilizando la funcion dibujar_boton. 
	En el boton que sea SCORE, escribe la puntuacion ingresada tipo int
	Los botones empiezan desde el n = BORDE
	"""
	n = BORDE
	for boton in botones:
		dibujar_boton(boton, n)
		if boton == SCORE:
			escribir_puntuacion(puntuacion, n)
		n += SEPARACION_BOTONES

def dibujar_siguiente_pieza(siguiente_pieza, color):
	"""
	Recibida la siguiente pieza la dibuja en su lugar y dibuja el letrero
	"""
	x_inicial = ANCHO_JUEGO + 2 * LADO_CELDA
	y_inicial = LADO_CELDA * 14

	gamelib.draw_image("img/next.gif", x_inicial, y_inicial)
	x_inicial, y_inicial = pixel_a_cartesiano(x_inicial, y_inicial + 2 * BORDE)

	factor_tamaño = 1.5
	centrado_x = BORDE * 3 // 2
	centrado_y = BORDE // 2

	for (x, y) in siguiente_pieza:
		x = x_inicial * factor_tamaño + x
		y = (y_inicial + 2 * BORDE) * factor_tamaño + y
		x = x + centrado_x
		y = y + centrado_y
		dibujar_celda(LADO_CELDA // factor_tamaño, x, y, color)

def dibujar_columna_derecha(siguiente_pieza, color, puntuacion):
    """
    Recibe la siguiente pieza, un color y una puntuacion y dibuja toda la interfaz de la columna derecha y la pieza siguiente del color recibido.
    No devuelve nada
    """
    dibujar_botones(BOTONES, puntuacion)
    dibujar_siguiente_pieza(siguiente_pieza, color)