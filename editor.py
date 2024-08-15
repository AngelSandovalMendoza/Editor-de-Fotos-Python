import tkinter as tk
from tkinter import filedialog
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

# Boton para cargar imagenes

def cargar_imagen():
    global imagen
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*png;")]
    )

    if file_path:
        imagen = Image.open(file_path)
        mostrar_imagen(imagen)

def mostrar_imagen(imagen):
    imagen.thumbnail((400,600))
    imagen_tk = ImageTk.PhotoImage(imagen)  
    label_img.config(image=imagen_tk)
    label_img.image = imagen_tk
    

def tonos_gris1():
    global imagen
    if imagen:
        imagen_gris = imagen.convert("RGB")
        gris = [(r*1 + g*0 + b*0) for (r,g,b) in imagen_gris.getdata()]
        imagen_gris.putdata(gris)
        mostrar_imagen(imagen_gris)

def tonos_rojos():
    global imagen
    if imagen:
        imagen_rojo = imagen.convert("RGB")
        rojo = [(r*1,g*0,b*0) for (r,g,b) in imagen_rojo.getdata()]
        imagen_rojo.putdata(rojo)
        mostrar_imagen(imagen_rojo)

def tonos_verdes():
    global imagen
    if imagen:
        imagen_verde = imagen.convert("RGB")
        verde = [(r*0, g*1 , b*0) for (r,g,b) in imagen_verde.getdata()]
        imagen_verde.putdata(verde)
        mostrar_imagen(imagen_verde)

def tonos_azules():
    global imagen
    if imagen:
        imagen_azul = imagen.convert("RGB")
        azul = [(r*0, g*0 , b*1) for (r,g,b) in imagen_azul.getdata()]
        imagen_azul.putdata(azul)
        mostrar_imagen(imagen_azul)


boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_imagen)
boton_cargar.pack(pady=20)

boton_rojo = tk.Button(ventana, text="Rojo", command=tonos_rojos)
boton_rojo.pack(pady=20)

boton_verde = tk.Button(ventana, text="Verde", command=tonos_azules)
boton_verde.pack(pady=20)

boton_azul = tk.Button(ventana, text="Azul", command=tonos_azules)
boton_verde.pack(pady=20)



label_img = tk.Label(ventana)
label_img.pack()

#Loop de ventana principal

ventana.mainloop()


