import tetris
import gamelib
import db
import interfaz_grafica
import sound

from random import choice

ESPERA_DESCENDER = 8

ALTO_VENTANA, ANCHO_VENTANA = interfaz_grafica.ALTO_VENTANA, interfaz_grafica.ANCHO_VENTANA

COLOR_BORDES = "gray11"
COLORES_SUPERFICIE = ["gray26", "snow4"]
COLORES_PIEZA = ["cyan", "deep pink", "tomato", "pale green", "firebrick3", "chocolate1", "purple1", "aquamarine2", "yellow", "dark salmon"]
COLOR_SIGUIENTE = "magenta"

TECLAS = db.teclas("database/teclas.txt")
RUTA_GUARDADO = "database/partida_guardada.txt"
RUTA_PUNTUACIONES = "database/puntuaciones.txt"

def mostrar_puntuaciones(lista_puntuaciones):
    """
    Recibe una lista con elementos (nombre, puntuacion) y muestra las mejores puntuaciones
    """
    resultado = "BEST SCORES\n\n"
    for i in range(len(lista_puntuaciones)):
        linea = f"{i+1}.{lista_puntuaciones[i][0]} = {lista_puntuaciones[i][1]} puntos\n"
        if i == len(lista_puntuaciones)-1:
            linea = linea.rstrip("\n")
        resultado += linea
    gamelib.say(resultado)

def nueva_puntuacion(puntos, lista_puntuaciones):
    """
    Recibe una puntuacion tipo int y una lista de puntuaciones con elementos (nombre, puntuacion).
    Pide al usuario un nombre y lo ingresa en la lista de mejores puntuaciones. 
    Guarda dicha lista en la base de datos y las muestra al jugador.
    El contrato supone que dicha puntuacion entra en la lista.
    """
    nombre = gamelib.input("INGRESE SU NOMBRE")
    while nombre == "" or nombre == None:
        gamelib.say("ERROR, DEBE INGRESAR UN NOMBRE")
        nombre = gamelib.input("INGRESE NUEVAMENTE SU NOMBRE")
    puntuacion_nueva = nombre, puntos
    lista_puntuaciones = db.puntos_en_lista(lista_puntuaciones, puntuacion_nueva)
    db.guardar_puntuaciones(lista_puntuaciones, RUTA_PUNTUACIONES)
    mostrar_puntuaciones(lista_puntuaciones)

def juego_terminado(puntos):
    """
    Muestra al usuario un mensaje de que el juego esta terminado. Se fija si la puntuacion entra en las mejores puntuaciones, en caso de que esto suceda le pide un nombre, la ingresa en dicha lista y luego la muestra.
    En caso contrario, no hace nada.
    No devuelve nada.
    """
    sound.juego_terminado()
    lista_puntuaciones = db.lista_puntuaciones(RUTA_PUNTUACIONES)
    gamelib.say("JUEGO TERMINADO")
    if len(lista_puntuaciones) == 0:
        nueva_puntuacion(puntos, lista_puntuaciones)
    else:
        ultimo_puntaje = int(lista_puntuaciones[len(lista_puntuaciones)-1][1])
        if puntos > ultimo_puntaje or len(lista_puntuaciones) < db.MAXIMO_LISTA_MEJORES:
            nueva_puntuacion(puntos, lista_puntuaciones)

def colores_superficie(lista_colores, color):
    """
    Recibida una lista de 2 colores y un color de ellos, alterna entre ellos
    """
    if color == lista_colores[0]:
        return lista_colores[1]
    return lista_colores[0]

def cambiar_siguiente_pieza(cambiar_pieza, siguiente_pieza, color_pieza):
    """
    Recibe un booleano, la siguiente pieza y un color_pieza 
    Si el booleano es True cambia la siguiente_pieza y el color_pieza. Si es False devuelve lo mismo
    """
    if cambiar_pieza:
        return tetris.generar_pieza(), choice(COLORES_PIEZA)
    return siguiente_pieza, color_pieza

def click_boton(x_click, y_click, juego, puntos):
    """
    Recibe las coordenadas en pixel de un click(event.button) y realiza la opcion correspondiente al boton presionado
    Si no se toca ningun boton no hace nada y devuelve juego, siguiente_pieza, puntos
    """
    boton = interfaz_grafica.tocar_boton(interfaz_grafica.BOTONES, x_click, y_click)
    if boton == interfaz_grafica.GUARDAR:
        db.guardar_partida(juego, puntos, RUTA_GUARDADO)
        sound.partida_guardada()
    if boton == interfaz_grafica.CARGAR:
        juego, puntos = db.cargar_partida(juego, puntos, RUTA_GUARDADO)
        sound.partida_cargada()
    if boton == interfaz_grafica.BEST:
        sound.pulsacion()
        lista_puntuaciones = db.lista_puntuaciones(RUTA_PUNTUACIONES)
        mostrar_puntuaciones(lista_puntuaciones)
    if not boton:
        sound.pulsacion_erronea()
    return juego, puntos

def controles(tecla_presionada, juego, siguiente_pieza, puntos):
    """
    Recibe una tecla presionada(event.key), un estado de juego, la siguiente pieza, y los puntos y ejecuta la accion correspondiente.
    Si a la tecla no esta accionada, no realiza ninguna accion, la funcion devuelve juego, False, puntos
    """
    if tecla_presionada in TECLAS["IZQUIERDA"]:
        juego = tetris.mover(juego, tetris.IZQUIERDA)
    if tecla_presionada in TECLAS["DERECHA"]:
        juego = tetris.mover(juego, tetris.DERECHA)
    if tecla_presionada in TECLAS["DESCENDER"]:
        juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
        return juego, cambiar_pieza, puntos
    if tecla_presionada in TECLAS["GUARDAR"]:
        db.guardar_partida(juego, puntos, RUTA_GUARDADO)
        sound.partida_guardada()
    if tecla_presionada in TECLAS["CARGAR"]:
        juego, puntos = db.cargar_partida(juego, puntos, RUTA_GUARDADO)
        sound.partida_cargada()
    if tecla_presionada in TECLAS["ROTAR"]:
        juego = tetris.rotar_pieza(juego)
    return juego, False, puntos

def juego_mostrar(juego, color_pieza, color_superficie, siguiente_pieza, puntos):
    """
    Recibe un estado de juego, el color de la pieza actual, el color de la superficie consolidada, la siguiente pieza y los puntos.
    Nuestra el estado de juego
    """
    gamelib.draw_image('img/fondo.gif', interfaz_grafica.LADO_CELDA, interfaz_grafica.LADO_CELDA)
    interfaz_grafica.dibujar_pieza(tetris.pieza_actual(juego), color_pieza)
    interfaz_grafica.dibujar_borde(COLOR_BORDES)
    interfaz_grafica.dibujar_columna_derecha(siguiente_pieza, COLOR_SIGUIENTE, puntos)
    interfaz_grafica.dibujar_superficie_consolidada(juego, color_superficie)

def juego_nuevo():
    """
    No recibe nada. Crea un nuevo estado de juego.
    Devuelve una tupla de los siguientes elementos:
    juego, siguiente_pieza, cambiar_pieza, color_pieza, color_superficie, puntos
    """
    juego = tetris.crear_juego(tetris.generar_pieza())
    siguiente_pieza, cambiar_pieza = tetris.generar_pieza(), False
    color_pieza, color_superficie = COLORES_PIEZA[0], COLORES_SUPERFICIE[0]
    puntos = 0
    return juego, siguiente_pieza, cambiar_pieza, color_pieza, color_superficie, puntos

def main():
    # Inicializar el estado del juego
    gamelib.title("TETRIS")
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    timer_bajar = ESPERA_DESCENDER
    juego, siguiente_pieza, cambiar_pieza, color_pieza, color_superficie, puntos = juego_nuevo()
    while gamelib.loop(fps=30):


        gamelib.draw_begin()
        juego_mostrar(juego, color_pieza, color_superficie, siguiente_pieza, puntos)
        gamelib.draw_end()

        if tetris.terminado(juego):
            juego_terminado(puntos)
            juego, siguiente_pieza, cambiar_pieza, color_pieza, color_superficie, puntos = juego_nuevo()

        for event in gamelib.get_events():
            if event.type == gamelib.EventType.KeyPress:

                if event.key in TECLAS["SALIR"]:
                    return
                juego, cambiar_pieza, puntos = controles(event.key, juego, siguiente_pieza, puntos)
                siguiente_pieza, color_pieza = cambiar_siguiente_pieza(cambiar_pieza, siguiente_pieza, color_pieza)

                if cambiar_pieza:
                    puntos += 1
                    sound.punto()

            if event.type == gamelib.EventType.ButtonPress:
                x, y = event.x, event.y
                juego, puntos = click_boton(x, y, juego, puntos)

            if event.type == gamelib.EventType.ButtonPress:
                x, y = event.x, event.y

        timer_bajar -= 1
        if timer_bajar == 0:
            timer_bajar = ESPERA_DESCENDER

            color_superficie = colores_superficie(COLORES_SUPERFICIE
                , color_superficie)
            
            if not cambiar_pieza:
                juego, cambiar_pieza = tetris.avanzar(juego, siguiente_pieza)
                siguiente_pieza, color_pieza = cambiar_siguiente_pieza(cambiar_pieza, siguiente_pieza, color_pieza)
                if cambiar_pieza:
                    puntos += 1
                    sound.punto()
            cambiar_pieza = False
        
gamelib.init(main)