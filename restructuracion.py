import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv
import os

# Rutas
RUTA_ARCHIVO = "peliculas.csv"
IMAGEN_FONDO = "fondo.jpg"

# Funciones
def cargar_peliculas_csv():
    peliculas = []
    try:
        with open(RUTA_ARCHIVO, newline='', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            next(lector)
            for fila in lector:
                peliculas.append([fila[0], fila[1], int(fila[2])])
    except FileNotFoundError:
        pass
    return peliculas

def guardar_peliculas_csv():
    with open(RUTA_ARCHIVO, "w", newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Titulo", "Género", "Duracion"])
        escritor.writerows(peliculas)

def actualizar_lista():
    listbox.delete(0, tk.END)
    for peli in peliculas:
        listbox.insert(tk.END, f"🎬 {peli[0]:30} 🎭 {peli[1]:15} ⏱️ {peli[2]} min")

def limpiar_entradas():
    entry_titulo.delete(0, tk.END)
    entry_genero.delete(0, tk.END)
    entry_duracion.delete(0, tk.END)

def agregar_pelicula():
    titulo = entry_titulo.get().strip()
    genero = entry_genero.get().strip()
    duracion = entry_duracion.get().strip()

    if not titulo or not genero or not duracion:
        messagebox.showwarning("⚠️ Campos incompletos", "Completá todos los campos.")
        return
    try:
        duracion = int(duracion)
    except ValueError:
        messagebox.showerror("❌ Error", "La duración debe ser un número.")
        return

    peliculas.append([titulo, genero, duracion])
    guardar_peliculas_csv()
    actualizar_lista()
    limpiar_entradas()

def seleccionar_pelicula(event):
    seleccion = listbox.curselection()
    if seleccion:
        idx = seleccion[0]
        peli = peliculas[idx]
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, peli[0])
        entry_genero.delete(0, tk.END)
        entry_genero.insert(0, peli[1])
        entry_duracion.delete(0, tk.END)
        entry_duracion.insert(0, peli[2])

def editar_pelicula():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showinfo("✏️ Seleccionar", "Seleccioná una película para editar.")
        return

    idx = seleccion[0]
    titulo = entry_titulo.get().strip()
    genero = entry_genero.get().strip()
    duracion = entry_duracion.get().strip()

    if not titulo or not genero or not duracion:
        messagebox.showwarning("⚠️ Campos incompletos", "Completá todos los campos.")
        return
    try:
        duracion = int(duracion)
    except ValueError:
        messagebox.showerror("❌ Error", "La duración debe ser un número.")
        return

    peliculas[idx] = [titulo, genero, duracion]
    guardar_peliculas_csv()
    actualizar_lista()
    limpiar_entradas()

def eliminar_pelicula():
    seleccion = listbox.curselection()
    if not seleccion:
        messagebox.showinfo("🗑️ Seleccionar", "Seleccioná una película para eliminar.")
        return

    idx = seleccion[0]
    confirmacion = messagebox.askyesno("Eliminar", f"¿Eliminar '{peliculas[idx][0]}'?")
    if confirmacion:
        peliculas.pop(idx)
        guardar_peliculas_csv()
        actualizar_lista()
        limpiar_entradas()

# Funciones de ordenamiento (NUEVAS)
def ordenar_az():
    global peliculas
    peliculas = sorted(peliculas, key=lambda x: x[0].lower())  # Ordena por título (A-Z)
    guardar_peliculas_csv()
    actualizar_lista()

def ordenar_duracion():
    global peliculas
    peliculas.sort(key=lambda x: x[2])  # Ordena por duración (menor a mayor)
    guardar_peliculas_csv()
    actualizar_lista()

def ordenar_genero():
    global peliculas
    peliculas = sorted(peliculas, key=lambda x: (x[1].lower(), x[0].lower()))  # Ordena por género y luego título
    guardar_peliculas_csv()
    actualizar_lista()

# INTERFAZ
ventana = tk.Tk()
ventana.title("🎥 Gestor de Películas")
ventana.geometry("900x800")  # Aumenté el tamaño para los nuevos botones
ventana.resizable(False, False)

# Imagen de fondo
if os.path.exists(IMAGEN_FONDO):
    imagen = Image.open(IMAGEN_FONDO)
    imagen = imagen.resize((900, 800))
    fondo = ImageTk.PhotoImage(imagen)
    fondo_label = tk.Label(ventana, image=fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    ventana.configure(bg="#f9f7f1")

# Contenedor principal
contenedor = tk.Frame(ventana, bg="#ffffff", bd=4, relief="ridge")
contenedor.place(relx=0.5, rely=0.04, anchor="n")

tk.Label(contenedor, text="🎞️ Mis Películas 🎞️", font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#333").pack(pady=12)

# Formulario
formulario = tk.Frame(ventana, bg="#ffffff")
formulario.place(relx=0.5, rely=0.15, anchor="n")

entry_font = ("Arial", 12)
label_opts = {"bg": "#ffffff", "anchor": "w", "font": ("Arial", 12, "bold")}

tk.Label(formulario, text="🎬 Título:", **label_opts).grid(row=0, column=0, sticky="w", pady=5)
entry_titulo = tk.Entry(formulario, width=45, font=entry_font)
entry_titulo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(formulario, text="🎭 Género:", **label_opts).grid(row=1, column=0, sticky="w", pady=5)
entry_genero = tk.Entry(formulario, width=45, font=entry_font)
entry_genero.grid(row=1, column=1, padx=10, pady=5)

tk.Label(formulario, text="⏱️ Duración (min):", **label_opts).grid(row=2, column=0, sticky="w", pady=5)
entry_duracion = tk.Entry(formulario, width=45, font=entry_font)
entry_duracion.grid(row=2, column=1, padx=10, pady=5)

# Botones principales
botones = tk.Frame(ventana, bg="#ffffff")
botones.place(relx=0.5, rely=0.32, anchor="n")

btn_style = {"width": 18, "height": 2, "font": ("Arial", 11, "bold")}

tk.Button(botones, text="➕ Agregar", command=agregar_pelicula, bg="#c8e6c9", **btn_style).grid(row=0, column=0, padx=10)
tk.Button(botones, text="✏️ Editar", command=editar_pelicula, bg="#fff59d", **btn_style).grid(row=0, column=1, padx=10)
tk.Button(botones, text="🗑️ Eliminar", command=eliminar_pelicula, bg="#ffcdd2", **btn_style).grid(row=0, column=2, padx=10)

# Botones de ordenamiento (NUEVOS)
botones_orden = tk.Frame(ventana, bg="#ffffff")
botones_orden.place(relx=0.5, rely=0.39, anchor="n")

btn_orden_style = {"width": 15, "height": 1, "font": ("Arial", 10, "bold")}

tk.Button(botones_orden, text="Ordenar A-Z", command=ordenar_az, bg="#bbdefb", **btn_orden_style).grid(row=0, column=0, padx=5, pady=5)
tk.Button(botones_orden, text="Por Duración", command=ordenar_duracion, bg="#bbdefb", **btn_orden_style).grid(row=0, column=1, padx=5, pady=5)
tk.Button(botones_orden, text="Por Género", command=ordenar_genero, bg="#bbdefb", **btn_orden_style).grid(row=0, column=2, padx=5, pady=5)


# Lista de películas
listbox_frame = tk.Frame(ventana, bg="#ffffff", bd=3, relief="ridge")
listbox_frame.place(relx=0.5, rely=0.47, anchor="n")

listbox = tk.Listbox(listbox_frame, width=100, height=18, font=("Courier New", 11), bg="#fdfdfd", fg="#333")
listbox.pack(padx=10, pady=10)
listbox.bind("<<ListboxSelect>>", seleccionar_pelicula)

# Carga inicial
peliculas = cargar_peliculas_csv()
actualizar_lista()

ventana.mainloop()