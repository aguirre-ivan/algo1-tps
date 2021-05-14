ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = "CUBO"
Z = "Z"
S = "S"
I = "I"
L = "L"
L_INV = "L_INV"
T = "T"

SUPERFICIE = 1
SIN_SUPERFICIE = 0

from random import choice
import db
import sound

PIEZAS = db.piezas("database/piezas.txt")
SIGUIENTE_ROTACION = db.siguiente_rotacion(PIEZAS)

def posicion_estandar(pieza):
	"""
	Dadas todas las rotaciones de una pieza, devuelve la posicion estandar de dicha pieza, es decir, la rotacion 0
	"""
	return pieza[0]

def generar_pieza(pieza=None):
	"""
	Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
	se generará una pieza del tipo indicado. Los tipos de pieza posibles
	están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

	El valor retornado es una tupla donde cada elemento es una posición
	ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
	I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
	ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
	"""
	if pieza == None:
		pieza = choice(list(PIEZAS.keys()))
	return posicion_estandar(PIEZAS[pieza])

def trasladar_pieza(pieza, dx, dy):
	"""
	Traslada la pieza de su posición actual a (posicion + (dx, dy)).

	La pieza está representada como una tupla de posiciones ocupadas,
	donde cada posición ocupada es una tupla (x, y). 
	Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
	el desplazamiento dx=2, dy=3 se devolverá la pieza 
	( (2, 3), (2, 4), (2, 5), (2, 6) ).
	"""
	pieza_trasladada = ()
	for (x, y) in pieza:
		pieza_trasladada += ((x + dx, y + dy,),)
	return pieza_trasladada

def pieza_en_origen(pieza):
	"""
	Recibida la rotacion de una pieza, la ubica en el origen (no en el centro).
	Devuelve la pieza ubicada en el origen y una tupla de coordenadas de cuanto hay que trasladarla para devolverla a su posicion original.
	"""
	x = 0
	y = 0
	while pieza[0][0] > 0:
		pieza = trasladar_pieza(pieza, -1, 0)
		x += 1
	while pieza[0][1] > 0:
		pieza = trasladar_pieza(pieza, 0, -1)
		y += 1
	return (pieza, (x, y))

def pieza_centrada(pieza):
	"""
	Dada una pieza la ubica arriba en el centro
	"""
	return trasladar_pieza(pieza, ANCHO_JUEGO//2, 0)

def pieza_y_positiva(pieza):
	"""
	Recibida la pieza centrada, la traslada hacia abajo hasta que sus coordenadas y sean positivas
	"""
	for i in range(len(pieza)):
		while pieza[i][1] < 0:
			pieza = trasladar_pieza(pieza, 0, 1)
	return pieza

def pieza_avanzada(pieza):
	"""
	Dada una pieza la avanza una posicion
	"""
	return trasladar_pieza(pieza, 0, 1)

def fila_vacia(ancho):
	"""
	Dado un ancho de juego, devuelve una fila con todos los valores en sin_superficie
	"""
	return [SIN_SUPERFICIE] * ancho

def fila_completa(ancho):
	"""
	Dado un ancho de juego, devuelve una fila completa, que seria la fila con todos los valores con superficie
	"""
	return [SUPERFICIE] * ancho

def tablero_vacio(ancho, alto):
	"""
	Dado el alto y ancho de juego, se devuelve un tablero vacio (con todos los valores del tablero en sin_superifice)
	"""
	tablero_vacio = []
	for i in range(alto):
		tablero_vacio.append(fila_vacia(ancho))
	return tablero_vacio

def crear_juego(pieza_inicial):
	"""
	Crea un nuevo juego de Tetris.

	El parámetro pieza_inicial es una pieza obtenida mediante 
	pieza.generar_pieza. Ver documentación de esa función para más información.

	El juego creado debe cumplir con lo siguiente:
	- La grilla está vacía: hay_superficie da False para todas las ubicaciones
	- La pieza actual está arriba de todo, en el centro de la pantalla.
	- El juego no está terminado: terminado(juego) da False

	Que la pieza actual esté arriba de todo significa que la coordenada Y de 
	sus posiciones superiores es 0 (cero).
	"""
	pieza_inicial = pieza_centrada(pieza_inicial)
	tablero_inicial = tablero_vacio(ANCHO_JUEGO, ALTO_JUEGO)
	juego = (pieza_inicial, tablero_inicial)
	return juego

def dimensiones(juego):
	"""
	Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
	"""
	return len(tablero(juego)[0]), len(tablero(juego))

def pieza_actual(juego):
	"""
	Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
	grilla ocupadas por la pieza actual.

	Se entiende por pieza actual a la pieza que está cayendo y todavía no
	fue consolidada con la superficie.

	La coordenada (0, 0) se refiere a la posición que está en la esquina 
	superior izquierda de la grilla.
	"""
	return juego[0]

def tablero(juego):
	"""
	Dado un estado de juego devuelve el estado de tablero actual.
	1 = Superficie consolidada
	0 = Superficie sin consolidar
	"""
	return juego[1]

def hay_superficie(juego, x, y):
	"""
	Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
	
	La coordenada (0, 0) se refiere a la posición que está en la esquina 
	superior izquierda de la grilla.
	"""
	return tablero(juego)[y][x] == SUPERFICIE

def mover(juego, direccion):
	"""
	Mueve la pieza actual hacia la derecha o izquierda, si es posible.
	Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
	recibido si el movimiento no se puede realizar.

	El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
	"""
	#Si no se puede mover devuelvo lo mismo, sino la muevo y devuelvo la tupla (pieza, grilla)
	pieza_movida = trasladar_pieza(pieza_actual(juego), direccion, 0)
	for (x, y) in pieza_actual(juego):
		if x + direccion < 0 or x + direccion > (ANCHO_JUEGO-1):
			return juego
	for (x, y) in pieza_movida:
		if hay_superficie(juego, x, y):
			return juego
	return pieza_movida, tablero(juego)

def acomodar_rotacion_x(rotacion):
	"""
	Recibida una rotacion, la acomoda dentro del tablero respecto de sus laterales, por si es que al rotar la pieza, ésta queda fuera.
	Devuelve un valor int, que es el desplazamiento que tiene fuera en la variable x.
	"""
	x_izquierdo = 0
	x_derecho = ANCHO_JUEGO - 1
	for x, y in rotacion:
		if x < x_izquierdo:
			x_izquierdo = x
		if x > x_derecho:
			x_derecho = x
	if x_izquierdo == 0:
		if x_derecho == ANCHO_JUEGO - 1:
			return 0
		return x_derecho - (ANCHO_JUEGO - 1)
	return x_izquierdo

def acomodar_rotacion_y(rotacion):
	"""
	Recibida una rotacion, la acomoda dentro del tablero respecto de su alto, por si es que al rotar la pieza, ésta queda fuera.
	Devuelve un valor int, que es el desplazamiento que tiene fuera en la variable y.
	"""
	y_mayor = ALTO_JUEGO - 1
	for x,y in rotacion:
		if y > y_mayor:
			y_mayor = y
	if y_mayor == ALTO_JUEGO - 1:
		return 0
	return y_mayor - (ALTO_JUEGO - 1)

def rotacion_acomodada(rotacion):
	"""
	Recibida una rotacion, la acomoda dentro del tablero, por si es que al rotar la pieza, esta queda fuera.
	"""
	factor_x = - acomodar_rotacion_x(rotacion)
	factor_y = - acomodar_rotacion_y(rotacion)
	return trasladar_pieza(rotacion, factor_x, factor_y)
			
def siguiente_rotacion(rotacion):
	"""
	Recibida una rotacion de una pieza, devuelve como una tupla, su siguiente rotacion acomodada.
	"""
	rotacion_en_origen, traslacion = pieza_en_origen(rotacion)
	x_tras, y_tras = traslacion
	sig_rot = SIGUIENTE_ROTACION[rotacion_en_origen]
	rot_acomodada = rotacion_acomodada(trasladar_pieza(sig_rot, x_tras, y_tras))
	return rot_acomodada

def rotar_pieza(juego):
	"""
	Recibe un estado de juego y devuelve un nuevo estado de juego con la pieza rotada
	Si hay superficie en la pieza rotada, prueba con la siguiente rotacion y asi sucesivamente hasta que no tenga mas opcion que devolver la misma pieza que recibio.
	Si la pieza queda fuera de los bordes del juego, la mete dentro (a menos que haya superficie que lo impida).
	"""
	pieza_inicial = pieza_actual(juego)
	pieza_rotada = siguiente_rotacion(pieza_inicial)

	for _ in range(3): #Numero maximo de rotaciones
		juego = pieza_rotada, tablero(juego)
		posicion_valida = True
		for x, y in pieza_rotada:
			if hay_superficie(juego, x, y):
				pieza_rotada = siguiente_rotacion(pieza_rotada)
				posicion_valida = False
				break
		if posicion_valida:
			return juego
	return pieza_inicial, tablero(juego)

def avanzar(juego, siguiente_pieza):
	"""
	Avanza al siguiente estado de juego a partir del estado actual.
	
	Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
	es el nuevo estado del juego y el segundo valor es un booleano que indica
	si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
	actual con la superficie).
	
	Avanzar el estado del juego significa:
	 - Descender una posición la pieza actual.
	 - Si al descender la pieza no colisiona con la superficie, simplemente
	   devolver el nuevo juego con la pieza en la nueva ubicación.
	 - En caso contrario, se debe
	   - Consolidar la pieza actual con la superficie.
	   - Eliminar las líneas que se hayan completado.
	   - Cambiar la pieza actual por siguiente_pieza.

	Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
	el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
	llamando a generar_pieza().

	**NOTA:** Hay una simplificación respecto del Tetris real a tener en
	consideración en esta función: la próxima pieza a agregar debe entrar 
	completamente en la grilla para poder seguir jugando, si al intentar 
	incorporar la nueva pieza arriba de todo en el medio de la grilla se
	pisara la superficie, se considerará que el juego está terminado.

	Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
	se debe devolver el mismo juego que se recibió.
	"""
	if terminado(juego):
		return juego, False
	for (x, y) in pieza_avanzada(pieza_actual(juego)):
		if y>(ALTO_JUEGO-1) or hay_superficie(juego, x, y):
			juego = consolidar_pieza_superficie(juego)
			return (pieza_centrada(siguiente_pieza), eliminar_lineas(tablero(juego))), True
	pieza_trasladada = pieza_avanzada(pieza_actual(juego))
	return (pieza_trasladada, tablero(juego)), False

def consolidar_pieza_superficie(juego):
	"""
	Dado un estado de juego, convierte la pieza actual a superficie consolidada
	"""
	for (x, y) in pieza_actual(juego):
		tablero(juego)[y][x] = SUPERFICIE 
	return juego

def eliminar_lineas(tablero):
	"""
	Dado un tablero, elimina las filas iguales a [1,1,1,1,1,1,1,1,1], y traslada las filas superiores una posicion hacia abajo
	"""
	for indice in range(ALTO_JUEGO):
		if tablero[indice] == fila_completa(ANCHO_JUEGO):
			sound.linea_completa()
			if indice == 0:
				tablero[indice] = fila_vacia(ANCHO_JUEGO)
			else:
				for i in range(indice,0,-1):
					tablero[i] = tablero[i-1]
				tablero[0] = fila_vacia(ANCHO_JUEGO)
	return tablero

def terminado(juego):
	"""
	Devuelve True si el juego terminó, es decir no se pueden agregar
	nuevas piezas, o False si se puede seguir jugando.
	"""
	pieza, _ = pieza_en_origen(pieza_actual(juego))
	pieza = pieza_y_positiva(pieza_avanzada(pieza_centrada(pieza)))
	for x, y in pieza:
		if hay_superficie(juego, x, y):
			return True
	return False

