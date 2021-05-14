class _Actor:
    "_Actor es un objeto privado de IMDB"

    def __init__(self, nombre, año, mes, dia):
        """
        Crea una instancia de _Actor con nombre, fecha de nacimiento(tupla), y 0 films participados.
        """
        self.nombre = nombre
        self.fecha_nacimiento = (año, mes, dia)
        self.films_participados = []

    def agregar_film_participado(self, id_film):
        """
        Agrega a films participados el id_film recibido. No devuelve nada.
        """
        self.films_participados.append(id_film)

class _Film:
    "_Film es un objeto privado de IMDB"

    def __init__(self, nombre, año, mes, dia, ids_actores):
        """
        Crea una instancia de _Film con nombre, fecha de lanzamiento(tupla), y una lista de ids de actores participes.
        """
        self.nombre = nombre
        self.fecha_lanzamiento = (año, mes, dia)
        self.actores_participes = ids_actores
        self.calificacion = 0

    def definir_calificacion(self, numero):
        """
        Recibido un numero del 1 al 10 lo promedia con la calificacion.
        """
        if self.calificacion == 0:
            self.calificacion = numero
        else:
            self.calificacion = (self.calificacion + numero) // 2

    def obtener_calificacion(self):
        """
        Devuelve la calificacion
        """
        return self.calificacion

class IMDB:
    "IMDB es una base de datos de cine"

    def __init__(self):
        """
        Crea una instancia de IMDB con 0 actores y 0 films.
        """
        self.actores = {}
        self.films = {}
        self.top10 = []

    def actor_agregar(self, nombre, año, mes, dia):
        """
        Recibe el nombre y la fecha de nacimiento de un actor o actriz, y lo agrega a la base de datos.
        Devuelve el ID del actor, que debe ser distinto a los IDs de los otros actores existentes.
        """
        id_actor = len(self.actores)
        self.actores[id_actor] = _Actor(nombre, año, mes, dia)
        return id_actor

    def cantidad_actores(self):
        """
        Devuelve la cantidad de actores existentes en la base de datos.
        """
        return len(self.actores)

    def actor_nombre(self, id_actor):
        """
        Recibe el ID de un actor y devuelve su nombre.
        """
        return self.actores[id_actor].nombre

    def actor_nacimiento(self, id_actor):
        """
        Recibe el ID de un actor y devuelve su fecha de nacimiento (tupla (año, mes, día)).
        """
        return self.actores[id_actor].fecha_nacimiento

    def film_agregar(self, nombre, año, mes, dia, ids_actores):
        """
        Recibe el nombre, la fecha de lanzamiento y una lista de IDs de actores que participaron en un film, y agrega el film a la base de datos.
        Devuelve el ID del film, que debe ser distinto a los IDs de los otros films existentes.
        """
        id_film = len(self.films)
        self.films[id_film] = _Film(nombre, año, mes, dia, ids_actores)
        for id_actor in ids_actores:
            self.actores[id_actor].agregar_film_participado(id_film)
        if len(self.top10) < 10:
            self.top10.append(id_film)
        return id_film

    def cantidad_films(self):
        """
        Devuelve la cantidad de films existentes en la base de datos.
        """
        return len(self.films)

    def film_nombre(self, id_film):
        """
        Recibe el ID de un film y devuelve su nombre.
        """
        return self.films[id_film].nombre

    def film_lanzamiento(self, id_film):
        """
        Recibe el ID de un film y devuelve su fecha de lanzamiento (tupla (año, mes, día)).
        """
        return self.films[id_film].fecha_lanzamiento
    
    def film_actores(self, id_film):
        """
        Recibe el ID de un film y devuelve la lista de IDs de los actores que participaron en el mismo.
        """
        return self.films[id_film].actores_participes

    def actor_films(self, id_actor):
        """
        Recibe el ID de un actor y devuelve la lista de IDs de los films en los que participó.
        """
        return self.actores[id_actor].films_participados

    def escribir_csv(self):
        """
        Escribe tres archivos CSV, todos sin encabezado:
        -actores.csv con formato nombre,año,mes,día
        -films.csv con formato nombre,año,mes,día
        -films_actores.csv con formato id_film,id_actor
        Cada una de las líneas de este archivo representa una relación ”tal actor trabajó en tal film”
        """
        archivo_actores = open("actores.csv", "w")

        for id_actor in range(self.cantidad_actores()):
            fecha = self.actor_nacimiento(id_actor)
            fecha = f"{fecha[0]},{fecha[1]},{fecha[2]}"
            archivo_actores.write(f"{id_actor},{self.actor_nombre(id_actor)},{fecha}\n")
        archivo_actores.close()


        archivo_films = open("films.csv", "w")
        archivo_films_actores = open("films_actores.csv", "w")

        for id_film in range(self.cantidad_films()):
            fecha = self.film_lanzamiento(id_film)
            fecha = f"{fecha[0]},{fecha[1]},{fecha[2]}"
            archivo_films.write(f"{id_film},{self.film_nombre(id_film)},{fecha}\n")

            id_actores = self.film_actores(id_film)
            for id_actor in id_actores:
                archivo_films_actores.write(f"{id_film},{id_actor}\n")

        archivo_films.close()
        archivo_films_actores.close()

    def films_decadas(self):
        """
        Agrupamiento de films por décadas, devuelve un diccionario con clave decada y valor una lista de films.
        """
        resultado = {}
        for id_film in range(self.cantidad_films()):
            año = decada(self.film_lanzamiento(id_film))
            resultado[año] = resultado.get(año, []) + [id_film]
        return resultado

    def calificar(self, id_film, calificacion):
        """
        Agrega la calificación (número entre 1 y 10) al film
        """
        self.films[id_film].definir_calificacion(calificacion)
        for i in range(len(self.top10)):
            if calificacion > self.top10[i]:
                self.top10.insert(i, id_film)
                if len(self.top10) > 10:
                    self.top10.pop() 

    def film_promedio(self, id_film):
        """
        Devuelve la calificación promedio del film. En caso de que el film no haya recibido ninguna calificación, devuelve 0.
        """
        return self.films[id_film].obtener_calificacion()

    def films_top10(self):
        """
        Devuelve la lista de los IDs de los 10 films con mejor promedio, ordenada de mayor a menor según el promedio.
        """
        return self.top10

    def distancia(self, id_actor1, id_actor2):
        """
        Devuelve la distancia entre los actores dados. 
        Dados dos actores o actrices, podemos intentar trazar un camino según las películas en las que actuaron; y definimos la distancia entre dos actores como la longitud del camino mínimo entre ellos.
        """
        visitados = set()
        lista_q = [(id_actor1, 0),]

        visitados.add(id_actor1)
        lista_q.append((id_actor1, 0))

        while len(lista_q) != 0:
            (id_actor_v, d) = lista_q.pop()
            if id_actor_v == id_actor2:
                return d
            for id_film in self.actor_films(id_actor_v):
                for id_actor_w in self.film_actores(id_film):
                    if id_actor_w not in visitados:
                        visitados.add(id_actor_w)
                        lista_q.append((id_actor_w, d+1))

def decada(fecha):
    """
    Recibe una fecha en formato (año, mes, dia)
    Devuelve la decada.
    """
    return fecha[0] // 10 * 10