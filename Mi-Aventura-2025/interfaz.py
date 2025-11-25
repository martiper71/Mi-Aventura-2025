# interfaz.py
import tkinter as tk
import os
import motor
import datos

# Variables globales de UI
fondo = None
imagen = None
texto = None
entrada = None
frase_var = None
foto_actual = None

def cargar_imagen_segura(ruta):
    try:
        return tk.PhotoImage(file=ruta)
    except tk.TclError:
        pass
    try:
        base = os.path.dirname(os.path.abspath(__file__))
        ruta_abs = os.path.join(base, ruta)
        return tk.PhotoImage(file=ruta_abs)
    except tk.TclError:
        return None

def refrescar_pantalla(nueva_hab, descripcion_sala, mensaje_extra=None):
    """Redibuja imagen y texto según la sala y mensaje extra (si lo hay)."""
    global foto_actual
    
    # Cargar imagen
    idx = nueva_hab if nueva_hab < len(datos.img) else 1
    foto_actual = cargar_imagen_segura(datos.img[idx])
    
    if foto_actual:
        imagen.config(image=foto_actual, text="")
        imagen.foto_actual = foto_actual
    else:
        imagen.config(image="", text=f"[Imagen {nueva_hab} no disponible]", fg="white", font=("Verdana", 14))

    # Construir texto
    if mensaje_extra:
        # Si hay mensaje extra, mostramos la base + el extra. 
        # Nota: descripcion_sala ya incluye objetos si viene de motor.
        # Pero a veces queremos mostrar solo el mensaje extra si es muy largo?
        # El original hacía: base = txt_base[nueva_hab] + mensaje_extra
        # Aquí usaremos lo que nos pase el motor.
        texto_completo = descripcion_sala + "\n\n" + mensaje_extra
    else:
        texto_completo = descripcion_sala

    texto.config(text=texto_completo)

def cerrar_juego_despues(mensaje_final):
    texto.config(text=mensaje_final)
    fondo.after(3000, fondo.destroy) # Damos 3 segundos para leer antes de cerrar

def limpiar_prompt(contenido):
    limpio = contenido.strip()
    if limpio.startswith(">>"):
        limpio = limpio[2:]
    return limpio.strip()

def procesar_entrada(event):
    bruto = frase_var.get()
    comando = limpiar_prompt(bruto)
    entrada.delete(0, tk.END)

    hab_actual = motor.habitacion_actual

    if comando == "":
        desc = motor.descripcion_con_objetos(hab_actual)
        refrescar_pantalla(hab_actual, desc, None)
        entrada.insert(0, ">> ")
        return

    verbo, objeto = motor.parsear(comando)
    if verbo is None:
        desc = motor.descripcion_con_objetos(hab_actual)
        refrescar_pantalla(hab_actual, desc, "¿Eh?")
        entrada.insert(0, ">> ")
        return

    # Ejecutar en motor
    nueva_hab, descripcion_sala, mensaje_extra, fin_juego = motor.ejecutar_comando(verbo, objeto)
    
    if fin_juego:
        cerrar_juego_despues(mensaje_extra)
        return

    refrescar_pantalla(nueva_hab, descripcion_sala, mensaje_extra)
    entrada.insert(0, ">> ")

def manejar_tecla_inicio(event):
    """Inicia el juego al pulsar cualquier tecla."""
    fondo.unbind("<Key>")
    entrada.config(state="normal")
    try:
        texto.pack_forget()
    except Exception:
        pass
    texto.pack(fill=tk.BOTH, expand=True)
    entrada.pack(fill=tk.BOTH, expand=True)
    
    # Estado inicial
    hab = motor.habitacion_actual
    desc = motor.descripcion_con_objetos(hab)
    refrescar_pantalla(hab, desc, None)
    
    entrada.delete(0, tk.END)
    entrada.insert(0, ">> ")
    entrada.focus_set()

def mostrar_pantalla_inicio():
    """Pantalla inicial con la portada. Pulsa una tecla para comenzar."""
    foto_portada = cargar_imagen_segura(datos.img[0]) if len(datos.img) > 0 else None
    if foto_portada:
        imagen.config(image=foto_portada, text="")
        imagen.foto_actual = foto_portada
    else:
        imagen.config(image="", text="[Portada no disponible]", fg="white", font=("Verdana", 14))

    texto.config(text="Pulsa una tecla para empezar")

    try:
        texto.pack_forget()
    except Exception:
        pass
    texto.pack(fill=tk.X, expand=False, pady=(10, 0))
    try:
        entrada.pack_forget()
    except Exception:
        pass

    entrada.config(state="disabled")
    entrada.delete(0, tk.END)

    fondo.bind("<Key>", manejar_tecla_inicio)

def iniciar_interfaz():
    global fondo, imagen, texto, entrada, frase_var, foto_actual
    
    fondo = tk.Tk()
    fondo.title("Star Quest. Sombras de Korriban")
    fondo.configure(background="black")

    # Centrar ventana 800x640
    ancho_pantalla = fondo.winfo_screenwidth()
    alto_pantalla = fondo.winfo_screenheight()
    x = (ancho_pantalla - 800) // 2
    y = (alto_pantalla - 640) // 2
    fondo.geometry(f"800x640+{x}+{y}")

    frase_var = tk.StringVar()

    # Imagen inicial (placeholder hasta que empiece el juego)
    foto_actual = None 
    
    imagen = tk.Label(
        fondo,
        bg="black",
        image=foto_actual
    )
    imagen.pack(fill=tk.BOTH, expand=True, pady=(20, 10))

    texto = tk.Label(
        fondo,
        text="",
        fg="white",
        bg="black",
        justify="center",
        wraplength=760,
        height=8,
        font=("Verdana", 18)
    )
    texto.pack(fill=tk.BOTH, expand=True)

    entrada = tk.Entry(
        fondo,
        fg="green",
        bg="black",
        justify="left",
        font=("Verdana", 18),
        textvariable=frase_var,
        insertbackground="green"
    )
    entrada.pack(fill=tk.BOTH, expand=True)

    entrada.bind("<Return>", procesar_entrada)
    
    mostrar_pantalla_inicio()
    fondo.mainloop()
