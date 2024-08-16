import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

imagen = None

# Declaración de la ventana principal
ventana = tk.Tk()
ventana.title("Angel Editor")

ancho_pantalla = ventana.winfo_screenwidth()
largo_pantalla = ventana.winfo_screenheight()

ancho_ventana = 1000
largo_ventana = 600

posicion_x = (ancho_pantalla - ancho_ventana) // 2
posicion_y = (largo_pantalla - largo_ventana) // 2

ventana.geometry(f"{ancho_ventana}x{largo_ventana}+{posicion_x}+{posicion_y}")

# Funciones principales
def cargar_imagen():
    global imagen
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*png;")]
    )

    if file_path:
        imagen = Image.open(file_path)
        mostrar_imagen(imagen)

def mostrar_imagen(imagen):
    imagen.thumbnail((400, 600))
    imagen_tk = ImageTk.PhotoImage(imagen)  
    label_img.config(image=imagen_tk)
    label_img.image = imagen_tk

def aplicar_filtro(event):
    seleccion = cuadro_lista.curselection()
    if seleccion:
        filtro_seleccionado = cuadro_lista.get(seleccion[0])
        if filtro_seleccionado == "Rojo":
            tonos_rojos()
        elif filtro_seleccionado == "Azul":
            tonos_azules()
        elif filtro_seleccionado == "Verde":
            tonos_verdes()
        elif filtro_seleccionado == "Gris1":
            tonos_gris1()
        elif filtro_seleccionado == "Gris2":
            tonos_gris2()
        elif filtro_seleccionado == "Gris3":
            tonos_gris3()

# Filtros de color
def tonos_gris1():
    global imagen
    if imagen:
        imagen_gris = imagen.convert("RGB")
        gris = [(int((r+g+b)/3),int((r+g+b)/3),int((r+g+b)/3)) for (r, g, b) in imagen_gris.getdata()]
        imagen_gris.putdata(gris)
        mostrar_imagen(imagen_gris)

def tonos_gris2():
    global imagen
    if imagen:
        imagen_gris = imagen.convert("RGB")
        gris = [(int(0.299*r+0.587*g+0.114*b),int(0.299*r+0.587*g+0.114*b),int(0.299*r+0.587*g+0.114*b)) for (r, g, b) in imagen_gris.getdata()]
        imagen_gris.putdata(gris)
        mostrar_imagen(imagen_gris)

def tonos_gris3():
    global imagen
    if imagen:
        imagen_gris = imagen.convert("RGB")
        gris = [((r,r,r)) for (r, g, b) in imagen_gris.getdata()]
        imagen_gris.putdata(gris)
        mostrar_imagen(imagen_gris)

def tonos_rojos():
    global imagen
    if imagen:
        imagen_rojo = imagen.convert("RGB")
        rojo = [(r, 0, 0) for (r, g, b) in imagen_rojo.getdata()]
        imagen_rojo.putdata(rojo)
        mostrar_imagen(imagen_rojo)

def tonos_verdes():
    global imagen
    if imagen:
        imagen_verde = imagen.convert("RGB")
        verde = [(0, g, 0) for (r, g, b) in imagen_verde.getdata()]
        imagen_verde.putdata(verde)
        mostrar_imagen(imagen_verde)

def tonos_azules():
    global imagen
    if imagen:
        imagen_azul = imagen.convert("RGB")
        azul = [(0, 0, b) for (r, g, b) in imagen_azul.getdata()]
        imagen_azul.putdata(azul)
        mostrar_imagen(imagen_azul)

# Botones y lista
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(pady=20)

cuadro_lista = tk.Listbox(ventana, height=4, width=15, selectmode="single")
cuadro_lista.pack()

filtros = ["Rojo", "Azul", "Verde", "Gris1","Gris2","Gris3"]

for filtro in filtros:
    cuadro_lista.insert(tk.END, filtro)

cuadro_lista.bind("<<ListboxSelect>>", aplicar_filtro)

label_img = tk.Label(ventana)
label_img.pack()

# Loop de ventana principal
ventana.mainloop()
