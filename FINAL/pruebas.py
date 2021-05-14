import traceback
import random
import csv
import imdb

def ejercicio_1():
    i = imdb.IMDB()

    id_bredice = i.actor_agregar("Leticia Brédice", 1972, 8, 26)
    id_darin = i.actor_agregar("Ricardo Darín", 1957, 1, 16)
    id_pauls = i.actor_agregar("Gastón Pauls", 1972, 1, 17)
    id_villamil = i.actor_agregar("Solead Villamil", 1969, 6, 19)

    # verificamos que los IDs son únicos
    assert len({id_bredice, id_darin, id_pauls, id_villamil}) == 4
    assert i.cantidad_actores() == 4
    assert i.actor_nombre(id_darin) == "Ricardo Darín"
    assert i.actor_nacimiento(id_pauls) == (1972, 1, 17)

    id_9reinas = i.film_agregar("Nueve Reinas", 2000, 8, 31, [id_bredice, id_darin, id_pauls])
    id_secreto = i.film_agregar("El secreto de sus ojos", 2009, 5, 21, [id_darin, id_villamil])

    assert id_9reinas != id_secreto
    assert i.cantidad_films() == 2
    assert i.film_nombre(id_9reinas) == "Nueve Reinas"
    assert i.film_lanzamiento(id_secreto) == (2009, 5, 21)
    assert set(i.film_actores(id_secreto)) == {id_darin, id_villamil}

    assert set(i.actor_films(id_darin)) == {id_9reinas, id_secreto}
    assert set(i.actor_films(id_bredice)) == {id_9reinas}

def ejercicio_2():
    i = imdb.IMDB()

    id_bredice = i.actor_agregar("Leticia Brédice", 1972, 8, 26)
    id_darin = i.actor_agregar("Ricardo Darín", 1957, 1, 16)
    id_pauls = i.actor_agregar("Gastón Pauls", 1972, 1, 17)
    id_villamil = i.actor_agregar("Solead Villamil", 1969, 6, 19)

    id_9reinas = i.film_agregar("Nueve Reinas", 2000, 8, 31, [id_bredice, id_darin, id_pauls])
    id_secreto = i.film_agregar("El secreto de sus ojos", 2009, 5, 21, [id_darin, id_villamil])

    i.escribir_csv()

    verificar_csv('actores.csv', [
        [id_bredice, "Leticia Brédice", 1972, 8, 26],
        [id_darin, "Ricardo Darín", 1957, 1, 16],
        [id_pauls, "Gastón Pauls", 1972, 1, 17],
        [id_villamil, "Solead Villamil", 1969, 6, 19],
    ])
    verificar_csv('films.csv', [
        [id_9reinas, "Nueve Reinas", 2000, 8, 31],
        [id_secreto, "El secreto de sus ojos", 2009, 5, 21],
    ])
    verificar_csv('films_actores.csv', [
        [id_9reinas, id_bredice],
        [id_9reinas, id_darin],
        [id_9reinas, id_pauls],
        [id_secreto, id_darin],
        [id_secreto, id_villamil],
    ])

def ejercicio_3():
    i = imdb.IMDB()

    id_bredice = i.actor_agregar("Leticia Brédice", 1972, 8, 26)
    id_darin = i.actor_agregar("Ricardo Darín", 1957, 1, 16)
    id_pauls = i.actor_agregar("Gastón Pauls", 1972, 1, 17)
    id_villamil = i.actor_agregar("Solead Villamil", 1969, 6, 19)
    id_cortese = i.actor_agregar("Rita Cortese", 1949, 8, 5)

    id_9reinas = i.film_agregar("Nueve Reinas", 2000, 8, 31, [id_bredice, id_darin, id_pauls])
    id_secreto = i.film_agregar("El secreto de sus ojos", 2009, 5, 21, [id_darin, id_villamil])
    id_relatos = i.film_agregar("Relatos salvajes", 2014, 8, 21, [id_cortese, id_darin])
    id_hable = i.film_agregar("Herencia", 2001, 6, 20, [id_cortese])

    r = i.films_decadas()

    for k in list(r.keys()):
        r[k] = sorted(r[k])

    assert_iguales('films_decadas()', r, {
        2000: sorted([id_9reinas, id_secreto, id_hable]),
        2010: sorted([id_relatos]),
    })

def ejercicio_4():
    i = imdb.IMDB()
    actores, films = popular_imdb(i)

    assert float(i.film_promedio(films[0])) == 0.0

    i.calificar(films[0], 7)
    assert float(i.film_promedio(films[0])) == 7.0

    i.calificar(films[0], 9)
    assert float(i.film_promedio(films[0])) == 8.0

    for id_film in films:
        promedio = random.uniform(1, 10)
        for _ in range(random.randint(50, 150)):
            i.calificar(id_film, puntaje_aleatorio(promedio))

    films = i.films_top10()
    assert len(films) == 10
    for j in range(len(films) - 1):
        assert i.film_promedio(films[j]) >= i.film_promedio(films[j + 1])

def ejercicio_5():
    i = imdb.IMDB()

    id_bredice = i.actor_agregar("Leticia Brédice", 1972, 8, 26)
    id_darin = i.actor_agregar("Ricardo Darín", 1957, 1, 16)
    id_pauls = i.actor_agregar("Gastón Pauls", 1972, 1, 17)
    id_villamil = i.actor_agregar("Solead Villamil", 1969, 6, 19)
    id_cortese = i.actor_agregar("Rita Cortese", 1949, 8, 5)

    id_9reinas = i.film_agregar("Nueve Reinas", 2000, 8, 31, [id_bredice, id_darin, id_pauls])
    id_secreto = i.film_agregar("El secreto de sus ojos", 2009, 5, 21, [id_darin, id_villamil])
    id_relatos = i.film_agregar("Relatos salvajes", 2014, 8, 21, [id_cortese, id_darin])

    assert i.distancia(id_darin, id_pauls) == 1
    assert i.distancia(id_bredice, id_cortese) == 2

def popular_imdb(i):
    actores = []
    for _ in range(100):
        id_actor = i.actor_agregar(
            f"Actor {len(actores) + 1}",
            random.randint(1920, 2010),
            random.randint(1, 12),
            random.randint(1, 28),
        )
        actores.append(id_actor)

    films = []
    for _ in range(100):
        id_film = i.film_agregar(
            f"Film {len(films) + 1}",
            random.randint(1940, 2020),
            random.randint(1, 12),
            random.randint(1, 28),
            random.sample(actores, random.randint(1, 10)),
        )
        films.append(id_film)

    return actores, films

def puntaje_aleatorio(promedio):
    return max(1, min(10, int(random.gauss(promedio, 2))))

def verificar_csv(ruta, filas):
    def normalizar(filas):
        return sorted([[str(x) for x in linea] for linea in filas])
    filas = normalizar(filas)
    with open(ruta) as f:
        filas_archivo = normalizar(csv.reader(f))
    assert filas_archivo == filas, \
        f"El archivo CSV {ruta} no es correcto\nContenido esperado:\n  {filas}\nContenido obtenido:\n  {filas_archivo}"

def assert_iguales(k, v1, v2):
    k1 = f"Resultado de {k}"
    k2 = f"Resultado esperado"
    n = max(len(k1), len(k2))
    assert v1 == v2, f"\n  {k1:<{n}}: {v1}\n  {k2:<{n}}: {v2}"

def main():
    ejercicios = [
        ejercicio_1,
        ejercicio_2,
        ejercicio_3,
        ejercicio_4,
        ejercicio_5,
    ]

    ejercicios_ok = 0

    for i, ejercicio in enumerate(ejercicios):
        try:
            random.seed(0)
            ejercicio()
            resultado = 'OK'
            ejercicios_ok += 1
        except:
            print()
            traceback.print_exc()
            print()
            resultado = 'FAIL'
        print(f"{ejercicio.__name__}: {resultado}")

    print(f"Cantidad de ejercicios OK: {ejercicios_ok}")

main()
