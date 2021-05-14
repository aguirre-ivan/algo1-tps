MAXIMO_LISTA_MEJORES = 10

def guardar_partida(juego, puntuacion, ruta):
	"""
	Guarda el juego en el estado actual en un archivo.

	Siendo la primer linea la pieza actual, escrita en la forma "x,y,x,y,x,y,x,y" (siendo x,y las coordenadas)
	
	La segunda linea es la puntuacion escrita "n"

	Y las siguientes #n_alto_juego de lineas una lista la cual representa la grilla de juego (tal como esta representado en tetris.py), siendo por cada linea una fila representada sin corchetes; ejemplo en una linea = <1,0,1,1,1,1,1,1>

	Sobreescribe el archivo
	"""
	with open(ruta, "w") as f:

		coordenadas = []
		for x,y in juego[0]:
			coordenadas += [str(x)] + [str(y)]
		coordenadas = ",".join(coordenadas)
		f.write(f"{coordenadas}\n")

		f.write(f"{puntuacion}\n")

		for fila in juego[1]:
			linea = []
			for col in fila:
				linea += str(col)
			linea = ",".join(linea)
			f.write(f"{linea}\n")
		
def cargar_partida(juego, puntuacion, ruta): 
	"""
	Carga una partida guardada desde un archivo. Devuelve un estado del juego, de forma similar a crear_juego, pero en este caso el estado no es inicial, sino que es el mismo estado que se guardó.
	Devuelve el juego como esta representado en tetris.py
	Si el archivo esta vacio, devuelve el mismo juego y puntuacion ingresados
	"""
	tablero = []
	pieza = []

	with open(ruta) as f:
		coordenadas = f.readline().rstrip("\n")
		if coordenadas == "":
			return juego, puntuacion
		coordenadas = coordenadas.split(",")
		for i in range(0, len(coordenadas), 2):
			pieza += [(int(coordenadas[i]), int(coordenadas[i+1])),]
		pieza = tuple(pieza)

		puntuacion = f.readline().rstrip("\n")

		for renglon in f:
			fila = []
			linea = renglon.rstrip("\n").split(",")
			for n in linea:
				fila += [int(n)]
			tablero += [fila]

	return (pieza, tablero), int(puntuacion)

def guardar_puntuaciones(lista_puntuaciones, ruta):
	"""
	Recibida una lista de puntuaciones y una ruta, guarda las puntuaciones (sobreescribiendo el archivo) en .txt descripto de la manera <nombre>, <puntuacion> en cada linea
	"""
	with open(ruta, "w") as f:
		for i in range(len(lista_puntuaciones)):
			nombre = lista_puntuaciones[i][0]
			puntuacion = lista_puntuaciones[i][1]
			linea = f"{nombre},{puntuacion}\n"
			if i == len(lista_puntuaciones) - 1:
				f.write(linea.rstrip("\n"))
			else:
				f.write(linea)

def lista_puntuaciones(ruta):
	"""
	Recibido un archivo .txt con lineas del estilo
	<nombre>, <puntuacion> ordenados y devuelve una lista del estilo [(<nombre>,<puntuacion>),]
	"""
	resultado = []
	with open(ruta) as f:
		while True:
			linea = f.readline()
			if linea == "":
				break
			linea = linea.split(",")
			nombre = linea[0]
			puntuacion = linea[1].rstrip("\n")
			resultado += [(nombre, puntuacion),]
	return resultado

def indice_puntuacion_nueva(lista_puntuaciones, puntuacion_nueva):
	"""
	Recibe una lista ordenada con elementos (nombre, puntuacion) y una puntuacion nueva (nombre, puntuacion). Devuelve el indice donde se ubicaria
	Si ya existen iguales puntuaciones, posiciona esta debajo.
	"""
	i_izq = 0
	i_der = len(lista_puntuaciones)-1
	hay_puntuaciones_iguales = False

	while i_izq <= i_der:
		i_medio = (i_izq + i_der) // 2
		puntuacion_indice = lista_puntuaciones[i_medio][1]

		if int(puntuacion_indice) == puntuacion_nueva[1]:
			i_ref = i_medio #Creo un indice de referencia
			while True:
				#La puntuacion_nueva debe estar debajo de todas las iguales a esta
				if i_ref > len(lista_puntuaciones) - 1:
					break
				puntuacion_ref = lista_puntuaciones[i_ref][1]
				if int(puntuacion_ref) == puntuacion_nueva[1]:
					hay_puntuaciones_iguales = True
					i_ref += 1
				else:
					break
			if hay_puntuaciones_iguales:
				return i_ref
			return i_medio

		if int(puntuacion_indice) < puntuacion_nueva[1]:
			i_der = i_medio - 1
		else:
			i_izq = i_medio + 1
	return i_izq

def puntos_en_lista(lista_puntuaciones, puntuacion_nueva):
    """
    Recibe una lista con elementos (nombre, puntuacion) ordenada y se fija si la puntuacion_nueva (nombre, puntuacion) entra dentro de la lista. Si entra la ingresa y si hay mas de MAXIMO_LISTA_MEJORES elementos en la lista lista_puntuaciones elimina el ultimo.
    """
    indice = indice_puntuacion_nueva(lista_puntuaciones, puntuacion_nueva)
    lista_puntuaciones.insert(indice, (puntuacion_nueva))
    while len(lista_puntuaciones) > MAXIMO_LISTA_MEJORES:
    	lista_puntuaciones.pop()
    return lista_puntuaciones

def teclas(ruta):
	"""
	Recibido un archivo .txt con las lineas en el estilo
	<tecla> = <funcion>, devuelve un diccionario con la funcion como clave y la tecla como valor
	"""
	resultado = {}
	with open(ruta) as f:
		while True:
			linea = f.readline()
			if linea == "":
				break
			if linea == "\n":
				continue
			linea = linea.split(" = ")
			funcion = linea[1].rstrip("\n")
			tecla = linea[0]
			resultado[funcion] = resultado.get(funcion, []) + [tecla]
	return resultado

def ordenar_por_coordenadas(piezas):
	"""
	Recibido un diccionario con piezas como clave, y como valores una lista de tuplas con sus respectivas rotaciones, ordena estas ultimas segun sus coordenadas: por ejemplo, (pos_1, pos_2, pos_3, pos_4).
	Ordenada de modo que pos_1 pase a ser aquella que tiene menor valor de x y menor valor de y (usa sorted).
	"""
	for pieza in piezas:
		piezas[pieza] = sorted(piezas[pieza])
	return piezas

def piezas(ruta):
	"""
	Recibida una ruta con un archivo .txt el cual contiene las coordenadas de piezas rotadas, por linea:
	<pieza en rotación 0> <pieza en rotación 1> <pieza en rotación 2> <pieza en rotación 3> # Nombre pieza
	Genera un diccionario con el nombre de pieza como clave y como valor una lista con las rotaciones representadas en tuplas. Devuelve dicho diccionario aplicandole la funcion ordenar_por_coordenadas(dic)
	"""	
	resultado = {}
	with open(ruta) as f:
		for linea in f:
			pieza = linea.rstrip("\n").split(" # ")
			coordenadas = pieza[0].split(" ")
			resultado[pieza[1]] = []
			for r in coordenadas:
				rotacion = []
				r = r.split(";")
				for coord in r:
					x, y = coord.split(",")
					rotacion += [(int(x), int(y)),]
				resultado[pieza[1]] += [tuple(rotacion)]
	return ordenar_por_coordenadas(resultado)

def siguiente_rotacion(piezas):
	"""
	Recibido un diccionario con todas las rotaciones de cada pieza, genera un diccionario en que cada rotacion es una clave, y como valor tiene su siguiente rotacion.
	"""
	res = {}
	for p in piezas:
		for i in range(len(piezas[p])):
			if i == len(piezas[p]) - 1:
				res[piezas[p][i]] = piezas[p][0]
			else:
				res[piezas[p][i]] = piezas[p][i+1]
	return res