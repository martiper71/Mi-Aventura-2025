import tkinter as tk
import os

# ---------------------------
# 1. DATOS DEL JUEGO (mínimo)
# ---------------------------

# Descripción base fija por sala. El índice es el número de habitación.
txt_base = [
    "",  # 0: portada
    "Te despiertas en una habitación tranquila y vacía.\n"
    "Aquí empieza tu aventura.",  # 1: primera habitación
]

# Rutas de imágenes por índice de habitación.
img = [
    "imagenes/000.png",  # 0: portada
    "imagenes/001.png",  # 1: primera habitación
]

# Objetos iniciales por sala (vacío para empezar).
OBJETOS_INICIALES = {
    1: [],
}

# Descripciones opcionales de objetos (puedes ir rellenando al crear objetos).
DESCRIPCIONES_OBJETOS = {
    # "llave": {"sala": "Una pequeña llave.", "inventario": "Llevas una pequeña llave."},
}


def clonar_objetos_iniciales():
    """Devuelve una copia del estado inicial de objetos."""
    return {hab: list(objs) for hab, objs in OBJETOS_INICIALES.items()}


def restablecer_estado_inicial():
    """Restituye inventario, posición y objetos como si empezara una partida nueva."""
    global habitacion_actual, inventario, objetos_en_sala
    habitacion_actual = 1
    inventario = []
    objetos_en_sala = clonar_objetos_iniciales()


# Inicializamos por primera vez
restablecer_estado_inicial()


def objetos_visibles_en_sala(hab):
    """Devuelve la lista de objetos visibles en una sala (sin condiciones especiales)."""
    return list(objetos_en_sala.get(hab, []))


# ---------------------------
# 2. HELPERS DE TEXTO / OBJETOS
# ---------------------------

def lista_a_texto_natural(lista):
    """
    ["camisa"] -> "camisa"
    ["camisa","pan"] -> "camisa y pan"
    ["a","b","c"] -> "a, b y c"
    """
    if len(lista) == 0:
        return ""
    if len(lista) == 1:
        return lista[0]
    if len(lista) == 2:
        return lista[0] + " y " + lista[1]
    return ", ".join(lista[:-1]) + " y " + lista[-1]


def nombre_visible_inventario(nombre):
    """Cómo se nombra un objeto de forma humana. Por defecto, su nombre literal."""
    return nombre


def normaliza_objeto_usuario(texto_objeto):
    """
    Quita artículos iniciales y devuelve el nombre en minúsculas.
    No valida contra listas; la validación se hace al usarlo.
    """
    if texto_objeto is None:
        return None
    t = texto_objeto.strip().lower()
    for art in ["el ", "la ", "los ", "las ", "un ", "una ", "unos ", "unas ", "mi ", "mis "]:
        if t.startswith(art):
            t = t[len(art):].strip()
            break
    return t


def descripcion_objeto(nombre, origen):
    """Devuelve una descripción del objeto según esté en sala o inventario."""
    info = DESCRIPCIONES_OBJETOS.get(nombre)
    if isinstance(info, dict):
        if origen == "inventario":
            return info.get("inventario") or info.get("sala") or f"Llevas {nombre_visible_inventario(nombre)}."
        return info.get("sala") or f"Observas {nombre_visible_inventario(nombre)}."
    # Texto simple o no definido
    if origen == "inventario":
        return info or f"Llevas {nombre_visible_inventario(nombre)}."
    return info or f"Observas {nombre_visible_inventario(nombre)}."


def inventario_texto():
    if len(inventario) == 0:
        return "No llevas nada encima."
    visibles = [nombre_visible_inventario(o) for o in inventario]
    if len(visibles) == 1:
        return f"Llevas {visibles[0]}."
    return "Llevas " + lista_a_texto_natural(visibles) + "."


def descripcion_con_objetos(hab):
    """Construye la descripción de la sala y añade listado de objetos visibles."""
    base = txt_base[hab]
    objs = objetos_visibles_en_sala(hab)
    if len(objs) == 0:
        return base
    visibles = [nombre_visible_inventario(o) for o in objs]
    extra = f" También puedes observar que hay {lista_a_texto_natural(visibles)}."
    return base + " " + extra.strip()


# ---------------------------
# 3. PARSER
# ---------------------------

def normaliza_direccion(palabra):
    mapa = {
        "n": "n", "norte": "n",
        "s": "s", "sur": "s",
        "e": "e", "este": "e",
        "o": "o", "oeste": "o",
        "subir": "subir", "arriba": "subir",
        "bajar": "bajar", "abajo": "bajar",
    }
    return mapa.get(palabra, None)


def parsear(frase_usuario):
    tokens = frase_usuario.strip().lower().split()
    if len(tokens) == 0:
        return None, None

    if len(tokens) == 1:
        palabra = tokens[0]
        dir_norm = normaliza_direccion(palabra)
        if dir_norm is not None:
            return "ir", dir_norm
        if palabra in ["inventario", "inv", "i"]:
            return "inventario", None
        if palabra in ["mirar", "mira", "examinar", "look", "l"]:
            return "mirar", None
        if palabra in ["fin", "salir", "quit"]:
            return "fin", None
        return palabra, None

    # 2+ palabras
    primera = tokens[0]
    dir_norm = normaliza_direccion(primera)
    if dir_norm is not None:
        return "ir", dir_norm
    if primera in ["inventario", "inv", "i"]:
        return "inventario", None
    verbo = primera
    objeto = " ".join(tokens[1:])
    return verbo, objeto


# ---------------------------
# 4. MOTOR DEL JUEGO (genérico)
# ---------------------------

def ejecutar_comando(verbo, objeto):
    """Devuelve (nueva_hab, descripcion_sala, mensaje_extra)."""
    global habitacion_actual, inventario, objetos_en_sala
    hab = habitacion_actual

    # INVENTARIO
    if verbo == "inventario":
        return hab, descripcion_con_objetos(hab), inventario_texto()

    # MIRAR / EXAMINAR
    if verbo in ["examinar", "mirar"]:
        if objeto:
            nombre = normaliza_objeto_usuario(objeto)
            if nombre in objetos_visibles_en_sala(hab):
                return hab, descripcion_con_objetos(hab), descripcion_objeto(nombre, "sala")
            if nombre in inventario:
                return hab, descripcion_con_objetos(hab), descripcion_objeto(nombre, "inventario")
            return hab, descripcion_con_objetos(hab), "No ves nada especial."
        return hab, descripcion_con_objetos(hab), None

    # COGER
    if verbo in ["coger", "agarrar", "tomar"]:
        if not objeto:
            return hab, descripcion_con_objetos(hab), "¿Coger qué?"
        nombre = normaliza_objeto_usuario(objeto)
        if nombre not in objetos_visibles_en_sala(hab):
            return hab, descripcion_con_objetos(hab), "Eso no está aquí."
        sala_objs = objetos_en_sala.get(hab, [])
        if nombre in sala_objs:
            sala_objs.remove(nombre)
            inventario.append(nombre)
            return hab, descripcion_con_objetos(hab), f"Has cogido {nombre_visible_inventario(nombre)}."
        return hab, descripcion_con_objetos(hab), "Eso no está aquí."

    # DEJAR
    if verbo in ["dejar", "soltar"]:
        if not objeto:
            return hab, descripcion_con_objetos(hab), "¿Dejar qué?"
        nombre = normaliza_objeto_usuario(objeto)
        if nombre in inventario:
            inventario.remove(nombre)
            objetos_en_sala.setdefault(hab, []).append(nombre)
            return hab, descripcion_con_objetos(hab), f"Has dejado {nombre_visible_inventario(nombre)} aquí."
        return hab, descripcion_con_objetos(hab), "No llevas eso."

    # MOVERSE
    if verbo == "ir":
        # Por ahora solo hay una habitación: cualquier dirección es inválida.
        return hab, descripcion_con_objetos(hab), "No puedes ir en esa dirección."

    # FIN DEL JUEGO
    if verbo == "fin":
        mensaje_final = "Gracias por jugar."
        cerrar_juego_despues(mensaje_final)
        return hab, descripcion_con_objetos(hab), mensaje_final

    # Otro comando
    return hab, descripcion_con_objetos(hab), "¿Cómo dices?"


# ---------------------------
# 5. INTERFAZ TKINTER
# ---------------------------

fondo = tk.Tk()
fondo.title("Mi Aventura 2025")
fondo.configure(background="black")

# Centrar ventana 800x640
ancho_pantalla = fondo.winfo_screenwidth()
alto_pantalla = fondo.winfo_screenheight()
x = (ancho_pantalla - 800) // 2
y = (alto_pantalla - 640) // 2
fondo.geometry(f"800x640+{x}+{y}")

frase_var = tk.StringVar()


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


# Imagen inicial asociada a la habitación actual (después de empezar)
foto_actual = cargar_imagen_segura(img[1 if len(img) > 1 else 0])

imagen = tk.Label(
    fondo,
    bg="black",
    image=foto_actual
)
imagen.foto_actual = foto_actual
if foto_actual is None:
    imagen.config(text="(imagen no encontrada)", fg="white", font=("Verdana", 14))
imagen.pack(fill=tk.BOTH, expand=True, pady=(20, 10))

texto = tk.Label(
    fondo,
    text=descripcion_con_objetos(habitacion_actual),
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


def mostrar_pantalla_inicio():
    """Pantalla inicial con la portada. Pulsa una tecla para comenzar."""
    foto_portada = cargar_imagen_segura(img[0]) if len(img) > 0 else None
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
    refrescar_pantalla(habitacion_actual, descripcion_con_objetos(habitacion_actual), None)
    entrada.delete(0, tk.END)
    entrada.insert(0, ">> ")
    entrada.focus_set()


def refrescar_pantalla(nueva_hab, descripcion_sala, mensaje_extra=None):
    """Redibuja imagen y texto según la sala y mensaje extra (si lo hay)."""
    global foto_actual
    idx = nueva_hab if nueva_hab < len(img) else 1
    foto_actual = cargar_imagen_segura(img[idx])
    if foto_actual:
        imagen.config(image=foto_actual, text="")
        imagen.foto_actual = foto_actual
    else:
        imagen.config(image="", text=f"[Imagen {nueva_hab} no disponible]", fg="white", font=("Verdana", 14))

    if mensaje_extra:
        base = txt_base[nueva_hab]
        texto_completo = base + "\n\n" + mensaje_extra
    else:
        texto_completo = descripcion_sala

    texto.config(text=texto_completo)


def cerrar_juego_despues(mensaje_final):
    texto.config(text=mensaje_final)
    fondo.after(500, fondo.destroy)


def limpiar_prompt(contenido):
    limpio = contenido.strip()
    if limpio.startswith(">>"):
        limpio = limpio[2:]
    return limpio.strip()


def motor_juego(event):
    global habitacion_actual
    bruto = frase_var.get()
    comando = limpiar_prompt(bruto)
    entrada.delete(0, tk.END)

    if comando == "":
        refrescar_pantalla(habitacion_actual, descripcion_con_objetos(habitacion_actual), None)
        entrada.insert(0, ">> ")
        return

    verbo, objeto = parsear(comando)
    if verbo is None:
        refrescar_pantalla(habitacion_actual, descripcion_con_objetos(habitacion_actual), "¿Eh?")
        entrada.insert(0, ">> ")
        return

    nueva_hab, descripcion_sala, mensaje_extra = ejecutar_comando(verbo, objeto)
    habitacion_actual = nueva_hab
    refrescar_pantalla(nueva_hab, descripcion_sala, mensaje_extra)
    entrada.insert(0, ">> ")


# ---------------------------
# 6. INICIO DEL JUEGO
# ---------------------------

entrada.bind("<Return>", motor_juego)
mostrar_pantalla_inicio()
fondo.mainloop()

