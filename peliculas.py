import csv

def cargar_peliculas_csv(ruta_archivo):
    peliculas = []
    with open(ruta_archivo, newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Saltear el encabezado
        for fila in lector:
            titulo = fila[0]
            genero = fila[1]
            duracion = int(fila[2])  # Convertimos duración a número
            peliculas.append([titulo, genero, duracion])
    return peliculas

# Ejemplo de uso
pelis = cargar_peliculas_csv("peliculas.csv")
for p in pelis:
    print(p)

def agregar_pelicula_csv(ruta_archivo):
    titulo = input("Ingresa el título de la película: ")
    genero = input("Ingresa el género de la película: ")
    duracion = input("Ingresa la duración de la película (en minutos): ")

    with open(ruta_archivo, 'a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([titulo, genero, duracion])
    print("Película agregada exitosamente.")

# Ejemplo de uso
agregar_pelicula_csv("peliculas.csv")