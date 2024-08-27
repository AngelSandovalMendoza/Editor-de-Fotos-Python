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
        elif filtro_seleccionado == "Brillo":
            brillo()
        elif filtro_seleccionado == "Alto Contraste":
            alto_contraste()
        elif filtro_seleccionado == "Inverso":
            inverso()
        elif filtro_seleccionado == "Mosaico":
            mosaico()

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





                        
        

# Botones y lista
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(pady=20)

cuadro_lista = tk.Listbox(ventana, height=4, width=15, selectmode="single")
cuadro_lista.pack()

filtros = ["Rojo", "Azul", "Verde", "Gris1","Gris2","Gris3","Brillo","Alto Contraste","Inverso","Mosaico"]

for filtro in filtros:
    cuadro_lista.insert(tk.END, filtro)

cuadro_lista.bind("<<ListboxSelect>>", aplicar_filtro)

label_img = tk.Label(ventana)
label_img.pack()

# Loop de ventana principal
ventana.mainloop()
