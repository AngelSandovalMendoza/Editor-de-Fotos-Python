import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageFilter
import numpy as np

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
        elif filtro_seleccionado == "Brillo":
            brillo()
        elif filtro_seleccionado == "Alto Contraste":
            alto_contraste()
        elif filtro_seleccionado == "Inverso":
            inverso()
        elif filtro_seleccionado == "Mosaico":
            mosaico()
        elif filtro_seleccionado == "Blur":
            blur()
        elif filtro_seleccionado == "Motion Blur":
            motion_blur()
        elif filtro_seleccionado == "Bordes":
            find_edges()
        

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

def brillo():
    global imagen
    aumento = 0.5
    if imagen:
        imagen_brillo = imagen.convert("RGB")
        brillo = [tuple(min(int(aumento * c), 255) for c in (r, g, b)) for (r, g, b) in imagen_brillo.getdata()]
        imagen_brillo.putdata(brillo)
        mostrar_imagen(imagen_brillo)

def alto_contraste():
    global imagen
    tonos_gris2()
    if imagen:
        alta_imagen = imagen.convert("RGB")
        contraste = []
        for (r, g, b) in alta_imagen.getdata():
            c = ((r+g+b)//3) 
            if c < 127:
                contraste.append((0, 0, 0))   
            else:
                contraste.append((255, 255, 255))
        alta_imagen.putdata(contraste)
        mostrar_imagen(alta_imagen)

def inverso():
    global imagen
    tonos_gris2()
    if imagen:
        alta_imagen = imagen.convert("RGB")
        contraste = []
        for (r, g, b) in alta_imagen.getdata():
            c = ((r+g+b)//3) 
            if c < 127:
                contraste.append((255, 255, 255))   
            else:
                contraste.append((0, 0, 0))
        alta_imagen.putdata(contraste)
        mostrar_imagen(alta_imagen)

def mosaico():
    global imagen
    tamano_bloque = 10
    if imagen:
        imagen_mosaico = imagen.convert("RGB")
        ancho, alto = imagen_mosaico.size
        pixeles = imagen_mosaico.load()

        for y in range(0, alto, tamano_bloque):
            for x in range(0, ancho, tamano_bloque):
                # Definir el área del bloque
                area = (x, y, min(x + tamano_bloque, ancho), min(y + tamano_bloque, alto))
                bloque = imagen_mosaico.crop(area)
                
                # Calcular el color promedio del bloque
                promedio_color = bloque.resize((1, 1)).getpixel((0, 0))
                
                # Aplicar el color promedio a todo el bloque
                for i in range(tamano_bloque):
                    for j in range(tamano_bloque):
                        if x + i < ancho and y + j < alto:
                            pixeles[x + i, y + j] = promedio_color

        mostrar_imagen(imagen_mosaico)

def blur():
    global imagen
    if imagen:
        imagen_blur = imagen.copy()
        pixeles = imagen_blur.load()
        ancho, alto = imagen_blur.size

        for y in range(1, alto-1):
            for x in range(1, ancho-1):
                vecinos = [
                    pixeles[x-1, y-1], pixeles[x, y-1], pixeles[x+1, y-1],
                    pixeles[x-1, y],   pixeles[x, y],   pixeles[x+1, y],
                    pixeles[x-1, y+1], pixeles[x, y+1], pixeles[x+1, y+1]
                ]
                
                # Calcular el promedio de los valores RGB de los vecinos
                promedio_color = tuple(
                    sum(p[i] for p in vecinos) // len(vecinos) for i in range(3)
                )
                
                # Asignar el color promedio al píxel actual
                pixeles[x, y] = promedio_color

        mostrar_imagen(imagen_blur)


def motion_blur():
    global imagen
    if imagen:
        # Parámetros del filtro
        blur_amount = 20  # Cantidad de desenfoque (ajusta según sea necesario)
        kernel_size = blur_amount
        kernel = [1] * kernel_size  # Kernel de desenfoque simple
        kernel = [k / sum(kernel) for k in kernel]  # Normalizar el kernel

        # Crear una imagen para el resultado
        imagen_blur = imagen.copy()
        pixeles = imagen_blur.load()
        ancho, alto = imagen_blur.size

        # Aplicar el kernel de motion blur
        for y in range(alto):
            for x in range(ancho):
                r_sum = g_sum = b_sum = 0
                for i in range(kernel_size):
                    offset = x + i - kernel_size // 2
                    if 0 <= offset < ancho:
                        r, g, b = pixeles[offset, y]
                        r_sum += r * kernel[i]
                        g_sum += g * kernel[i]
                        b_sum += b * kernel[i]

                # Asignar el color promedio al píxel actual
                pixeles[x, y] = (int(r_sum), int(g_sum), int(b_sum))

        mostrar_imagen(imagen_blur)

def find_edges():
    global imagen
    if imagen:
        # Definir el kernel
        filter_width = 5
        filter_height = 5
        filter_matrix = np.array([
            [0, 0, -1, 0, 0],
            [0, 0, -1, 0, 0],
            [0, 0,  2, 0, 0],
            [0, 0,  0, 0, 0],
            [0, 0,  0, 0, 0]
        ])
        factor = 1.0
        bias = 0.0

        # Convertir imagen a escala de grises
        imagen_gris = imagen.convert("L")
        pixeles = imagen_gris.load()
        ancho, alto = imagen_gris.size

        # Crear una imagen para el resultado
        imagen_bordes = Image.new("L", (ancho, alto))
        pixeles_bordes = imagen_bordes.load()

        # Aplicar el filtro
        for y in range(filter_height // 2, alto - filter_height // 2):
            for x in range(filter_width // 2, ancho - filter_width // 2):
                r_sum = g_sum = b_sum = 0

                # Aplicar el filtro a la vecindad del píxel (x, y)
                for i in range(-filter_height // 2, filter_height // 2 + 1):
                    for j in range(-filter_width // 2, filter_width // 2 + 1):
                        pixel_value = pixeles[x + j, y + i]
                        r_sum += pixel_value * filter_matrix[i + filter_height // 2, j + filter_width // 2]
                
                # Aplicar factor y sesgo
                valor_filtro = factor * r_sum + bias
                valor_filtro = min(max(int(valor_filtro), 0), 255)  # Asegurar que el valor esté en el rango [0, 255]

                # Asignar el valor a la imagen de salida
                pixeles_bordes[x, y] = valor_filtro

        mostrar_imagen(imagen_bordes)




# Botones y lista
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(pady=20)

cuadro_lista = tk.Listbox(ventana, height=4, width=15, selectmode="single")
cuadro_lista.pack()

filtros = ["Rojo", "Azul", "Verde", "Gris1","Gris2","Gris3","Brillo","Alto Contraste","Inverso","Mosaico","Blur","Motion Blur","Bordes"]

for filtro in filtros:
    cuadro_lista.insert(tk.END, filtro)

cuadro_lista.bind("<<ListboxSelect>>", aplicar_filtro)

label_img = tk.Label(ventana)
label_img.pack()

# Loop de ventana principal
ventana.mainloop()
