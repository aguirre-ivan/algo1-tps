ALTO_JUEGO, ANCHO_JUEGO = 300, 300
ALTO_CUADRO_TEXTO = 50
ALTO_VENTANA, ANCHO_VENTANA = ALTO_JUEGO + ALTO_CUADRO_TEXTO * 2, ANCHO_JUEGO

LADOS_CASILLA = 30
DIAMETRO_CIRCULO = 20
ALTO_CRUZ = 20

def pixel_a_cartesiano(x, y):
    """
    Recibidas coordenadas en pixeles las devuelve en cartesianas
    """
    return x // LADOS_CASILLA, ((y - ALTO_CUADRO_TEXTO) // LADOS_CASILLA)

_, LARGO_Y_CARTESIANO = pixel_a_cartesiano(0, ALTO_JUEGO + ALTO_CUADRO_TEXTO)
LARGO_X_CARTESIANO, _ = pixel_a_cartesiano(ANCHO_JUEGO, 0)

FIGURAS_TOTALES_DISPONIBLES = LARGO_Y_CARTESIANO * LARGO_X_CARTESIANO

BORDE_Y_CARTESIANO = LARGO_Y_CARTESIANO - 1 
BORDE_X_CARTESIANO = LARGO_X_CARTESIANO - 1

#Les resto 1 debido a que mis coordenadas en tabla empiezan desde el 0, y no del 1

COLOR_CIRCULO = "cyan"
COLOR_CRUZ = "deep pink"

import gamelib

def juego_crear():
    """
    Inicializar el estado del juego
    """
    tablero = {"CRUZ":[], "CIRCULO":[]}
    turno = "CIRCULO"
    return tablero, turno

def tablero_actual(juego):
    """
    Recibido un estado de juego, devuelve el tablero actual
    """
    return juego[0]

def turno_actual(juego):
    """
    Recibido el estado de juego, devuelve el turno actual
    """
    return juego[1]

def siguiente_turno(turno):
    """
    Dado un turno actual, devuelve el siguiente turno, solo entre opciones "CIRCULO" o "CRUZ"
    """
    if turno == "CIRCULO":
        return "CRUZ"
    return "CIRCULO"

def color_turno(turno):
    """
    Recibido un turno, devuelve el color del turno actual
    "CIRCULO" = "orange red"
    "CRUZ" = "deep pink"
    """
    if turno == "CIRCULO":
        return COLOR_CIRCULO
    return COLOR_CRUZ

def dibujar_circulo(x, y):
    """
    Recibidas coordenadas cartesianas, dibuja un circulo en el centro de la casilla correspondiente
    """
    borde = (LADOS_CASILLA - DIAMETRO_CIRCULO) // 2
    x1 = x * LADOS_CASILLA + borde
    y1 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + borde
    x2 = x * LADOS_CASILLA + (LADOS_CASILLA - borde)
    y2 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + (LADOS_CASILLA - borde)
    gamelib.draw_oval(x1, y1, x2, y2, outline=COLOR_CIRCULO, fill="", width="2")

def dibujar_cruz(x, y):
    """
    Recibidas coordenadas cartesianas, dibuja una cruz en la casilla correspondiente
    """
    borde = (LADOS_CASILLA - ALTO_CRUZ) // 2
    xa1 = x * LADOS_CASILLA + borde
    ya1 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + borde
    xa2 = x * LADOS_CASILLA + (LADOS_CASILLA - borde)
    ya2 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + (LADOS_CASILLA - borde)
    gamelib.draw_line(xa1, ya1, xa2, ya2, fill=COLOR_CRUZ, width="2")
    xb1 = x * LADOS_CASILLA + (LADOS_CASILLA - borde)
    yb1 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + borde
    xb2 = x * LADOS_CASILLA + borde
    yb2 = y * LADOS_CASILLA + ALTO_CUADRO_TEXTO + (LADOS_CASILLA - borde)
    gamelib.draw_line(xb1, yb1, xb2, yb2, fill=COLOR_CRUZ, width="2")

def cinco_en_linea(lista_numeros):
    """
    Recibida una lista de mas de 5 numeros enteros, verifica hay 5 o mas numeros todos consecutivos. Aclaracion: No hace falta que esten ordenados
    Devuelve una tupla, siendo el primero elemento un booleano que indica la condicion anterior, y el segundo una lista con dichos numeros consecutivos(descartando los que no) o un None si el primer elemento fue F
    """
    lista_numeros = sorted(lista_numeros)
    for i in range(len(lista_numeros)-4):
        lista_devuelta = [lista_numeros[i]]
        for k in range(i, len(lista_numeros)-1):
            numero_siguiente = lista_numeros[k] + 1
            if numero_siguiente != lista_numeros[k+1] and len(lista_devuelta) < 5:
                break
            lista_devuelta += [numero_siguiente]
        if len(lista_devuelta) >= 5:
            return True, lista_devuelta
    return False, None

def ultima_figura_dibujada(juego):
    """
    Recibido un estado de juego devuelve en coordenadas cartesianas la ultima figura dibuja, solo y solo si existe al menos una figura del turno en el juego.
    """
    tablero = tablero_actual(juego)
    turno = turno_actual(juego)

    indice_ult_posicion = len(tablero[turno]) - 1
    ultima_posicion = tablero[turno][indice_ult_posicion]
    return ultima_posicion

def linea_recta(juego, orientacion):
    """
    Recibido un estado de juego y una orientacion (solo admite "horizontal" o "vertical"), verifica si hay CINCO EN LINEA (o mas) y borra las figuras dibujadas pertenecientes.
    """
    turno = turno_actual(juego)
    tablero = tablero_actual(juego)

    if len(tablero[turno]) < 1:
        return

    x_ult, y_ult = ultima_figura_dibujada(juego)

    if orientacion == "horizontal":
        i = (0, 1) # i[0]=indice[0] / i[1]=indice[1]
        i_ult = y_ult
    elif orientacion == "vertical":
        i = (1, 0) # i[0]=indice[1] / i[1]=indice[0]
        i_ult = x_ult

    x_ult, y_ult = ultima_figura_dibujada(juego)
    posiciones_en_linea = [pos[i[0]] for pos in tablero[turno] if pos[i[1]] == i_ult]
    if len(posiciones_en_linea) >= 5:
        hay_linea, n_a_borrar = cinco_en_linea(posiciones_en_linea)
        if hay_linea:
            figuras_no_eliminadas = []
            for posicion in tablero[turno]:
                if not (posicion[i[1]] == i_ult and posicion[i[0]] in n_a_borrar):
                    figuras_no_eliminadas += (posicion,)
            tablero[turno] = figuras_no_eliminadas
            gamelib.play_sound("linea.wav")

def juego_mostrar(juego):
    """Actualizar la ventana"""
    turno = turno_actual(juego)
    tablero = tablero_actual(juego)

    gamelib.draw_image('fondo_texto.gif', 0, 0)
    gamelib.draw_image('fondo_juego.gif', 0, ALTO_CUADRO_TEXTO)
    gamelib.draw_image('fondo_texto.gif', 0, ALTO_VENTANA - ALTO_CUADRO_TEXTO)
    gamelib.draw_text('5 EN LINEA', ANCHO_VENTANA//2, ALTO_CUADRO_TEXTO//2, fill=color_turno(turno))
    gamelib.draw_text(f"TURNO: {turno}", ANCHO_VENTANA//2, ALTO_VENTANA-ALTO_CUADRO_TEXTO//2, fill=color_turno(turno))

    for y in range(ALTO_CUADRO_TEXTO, ALTO_JUEGO + ALTO_CUADRO_TEXTO + 1, LADOS_CASILLA):
        gamelib.draw_line(0, y, ANCHO_JUEGO, y, fill='tomato4', width=2)
    for x in range(0, ANCHO_JUEGO, LADOS_CASILLA):
        gamelib.draw_line(x, ALTO_CUADRO_TEXTO, x, ALTO_CUADRO_TEXTO + ALTO_JUEGO, fill='tomato4', width=2)

    for (x, y) in tablero["CIRCULO"]:
        dibujar_circulo(x, y)
    for (x, y) in tablero["CRUZ"]:
        dibujar_cruz(x, y)

def juego_actualizar(juego, x, y):
    """
    Actualizar el estado del juego

    x e y son las coordenadas (CARTESIANAS) donde el usuario hizo click.
    Esta función determina si esas coordenadas corresponden a una celda
    del tablero; en ese caso determina el nuevo estado del juego y lo
    devuelve.
    """
    tablero = tablero_actual(juego)
    turno = turno_actual(juego)
    tablero[turno] += [(x, y),]
    linea_recta(juego, "horizontal")
    linea_recta(juego, "vertical")
    return tablero, siguiente_turno(turno)

def main():
    gamelib.play_sound("linea.wav")
    gamelib.title("EPIC GAME")
    juego = juego_crear()
    # Ajustar el tamaño de la ventana
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    # Mientras la ventana esté abierta:
    while gamelib.is_alive():
        tablero = tablero_actual(juego)
        turno = turno_actual(juego)
        # Todas las instrucciones que dibujen algo en la pantalla deben ir
        # entre `draw_begin()` y `draw_end()`:
        gamelib.draw_begin()
        juego_mostrar(juego)
        gamelib.draw_end()
        # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
        # usuario presionó una tecla o un botón del mouse, etc).
        # Esperamos hasta que ocurra un evento
        ev = gamelib.wait()

        if not ev:
            # El usuario cerró la ventana.
            break
        
        if (len(tablero["CRUZ"]) + len(tablero["CIRCULO"])) == FIGURAS_TOTALES_DISPONIBLES:
            gamelib.play_sound('game_over.wav')
            gamelib.say(f"JUEGO FINALIZADO\nEl ganador es el {turno}")
            break

        if ev.type == gamelib.EventType.KeyPress and ev.key == 'Escape':
            # El usuario presionó la tecla Escape, cerrar la aplicación.
            break

        if ev.type == gamelib.EventType.ButtonPress:
            # El usuario presionó un botón del mouse
            x, y = ev.x, ev.y # averiguamos la posición donde se hizo click
            x, y = pixel_a_cartesiano(x, y)
            if (0 <= x <= BORDE_X_CARTESIANO and 0 <= y <= BORDE_Y_CARTESIANO) and not ((x,y) in tablero["CIRCULO"] or (x, y) in tablero["CRUZ"]):
                juego = juego_actualizar(juego, x, y)
                gamelib.play_sound('click_casilla.wav')
            else:
                gamelib.play_sound('click_error.wav')

gamelib.init(main)