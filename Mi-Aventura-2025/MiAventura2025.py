import tkinter as tk
import os
# ------------------------------
# FECHA MODIFICACIÓN: 2025-11-14
# ------------------------------
# ---------------------------
# 1. DATOS DEL JUEGO
# ---------------------------

# Descripción base fija por sala. El índice es el número de habitación.
txt_base = [
    "Portada\n\nSTAR QUEST: SOMBRAS DE KORRIBAN",
    # 1
    "Te despiertas entre chispas y humo dentro de la cápsula de escape de tu carguero. "
    "El cristal delantero está roto y, fuera, solo ves un océano de arena rojiza.",
    # 2
    "Has salido de la cápsula. Restos humeantes del fuselaje están dispersos por la arena. "
    "El viento del desierto azota con fuerza.",
    # 3
    "Un estrecho desfiladero de roca negra se abre ante ti. Más abajo intuyes la entrada de una cueva.",
    # 4
    "La oscuridad te envuelve. Cristales rojizos incrustados en la roca emiten un brillo débil.",
    # 5
    "Restos de un pequeño campamento: tiendas rasgadas, huellas medio borradas y una hoguera apagada hace días.",
    # 6
    "Una delgada torre de comunicaciones imperial sobresale sobre la roca. Está dañada y chisporrotea.\n"
    "Tal vez podrías REPARAR la torre si encuentras algún módulo adecuado.",
    # 7
    "Un arco de piedra negra, tallado con símbolos antiguos, marca la entrada a un templo subterráneo.\n"
    "Al fondo se adivina una puerta de piedra que parece reaccionar a símbolos Sith.",
    # 8
    "Columnas derrumbadas y trozos de estatuas antiguas rodean la zona. El silencio es casi absoluto.",
    # 9
    "Estatuas Sith alineadas a ambos lados del pasillo parecen observar cada uno de tus movimientos.",
    # 10
    "Una cámara circular de piedra. Cada sonido se repite una y otra vez, como si el propio templo escuchara.\n"
    "Quizá si GRITAS ocurra algo.",
    # 11
    "Un pasillo cargado de energía oscura. La piedra vibra levemente bajo tus pies.",
    # 12
    "Un pequeño recinto silencioso, con un círculo tallado en el suelo, pensado para la contemplación.",
    # 13
    "Pilares manchados, cadenas antiguas y un altar central. El ambiente es opresivo.",
    # 14
    "Estanterías de datos, reliquias y holocrones sellados. Algún dispositivo aún parpadea.\n"
    "Quizá EXAMINAR el DATAPAD te dé información útil.",
    # 15
    "En el centro, sobre un pedestal, descansa un artefacto de diseño Sith que emite un zumbido grave.",
    # 16
    "Una rampa ascendente lleva hacia la luz. Aire caliente del desierto se cuela por una rendija.",
    # 17
    "Paneles metálicos y antenas sobresalen de la roca: una instalación imperial camuflada en el desierto.",
    # 18
    "Un hangar pequeño con restos de cazas TIE desmontados y contenedores de carga apilados.",
    # 19
    "Una mesa metálica, una consola encendida y varias holopantallas con informes tácticos.",
    # 20
    "Pantallas, consolas y un gran transmisor apuntando al cielo. Se oyen débiles voces imperiales por los altavoces.\n"
    "Tal vez puedas CONTACTAR con la flota Rebelde desde aquí.",
    # 21
    "Un generador rugiente llena la sala con un zumbido constante. Varias conducciones energéticas salen de él.\n"
    "Si lo SABOTEAS podrías desactivar parte de las defensas imperiales.",
    # 22
    "Pequeñas celdas alineadas. En una de ellas, un prisionero Rebelde te observa con esperanza.\n"
    "Quizá puedas LIBERAR al prisionero.",
    # 23
    "Mesas llenas de instrumentos, contenedores y restos de tecnología Sith analizada.",
    # 24
    "Un ascensor imperial conecta esta zona con una plataforma por encima del templo.",
    # 25
    "Desde aquí se domina el desierto de Korriban. El viento sopla con fuerza entre los restos de estatuas.",
    # 26
    "Una estrecha pasarela metálica cruza un profundo cañón. Cruje con cada paso.",
    # 27
    "Una bestia k’lor’slug descansa entre huesos y armaduras destrozadas. Mejor no molestarla.",
    # 28
    "Inscripciones en las paredes relatan hazañas de un maestro Sith olvidado hace siglos.",
    # 29
    "Un túnel parcialmente derrumbado conduce hacia una zona imperial fuertemente reforzada.",
    # 30
    "Soldadura reciente, cajas marcadas con el emblema imperial y una nave Lambda en reposo.",
    # 31
    "Un transporte imperial de tipo Lambda espera en la plataforma, con la rampa de acceso bajada.\n"
    "Cuando lo tengas todo listo, escribe DESPEGAR.",
    # 32
    "Te elevas sobre el planeta, dejando atrás el templo, la base imperial y los ecos del Lado Oscuro."
]

# Rutas de imágenes por índice de habitación (000..032).
# Puedes ir creando los PNG correspondientes en la carpeta imagenes/.
img = [f"imagenes/{i:03d}.png" for i in range(33)]

# Mapa de conexiones entre habitaciones
# Claves: nº de sala; valores: dict de dirección normalizada -> nº de sala destino.
# Direcciones válidas: n, s, e, o, subir, bajar
SALIDAS = {
    1:  {"n": 2},
    2:  {"s": 1, "e": 3, "n": 5},
    3:  {"o": 2, "bajar": 4},
    4:  {"subir": 3},
    5:  {"s": 2, "e": 6, "n": 8},
    6:  {"o": 5, "n": 7},

    7:  {"s": 6, "o": 8, "bajar": 9},
    8:  {"s": 5, "e": 7},

    9:  {"subir": 7, "e": 10, "o": 11},
    10: {"o": 9, "e": 13},
    11: {"e": 9, "s": 12},
    12: {"n": 11, "e": 14},
    13: {"o": 10, "e": 15},
    14: {"o": 12, "e": 16},
    15: {"o": 13},
    16: {"o": 14, "subir": 17},

    17: {"e": 18, "n": 25, "bajar": 16},
    18: {"o": 17, "e": 23, "s": 21},
    19: {"o": 23, "s": 20},
    20: {"n": 19},
    21: {"n": 18},
    22: {"n": 23},
    23: {"o": 18, "s": 22, "n": 24, "e": 19},
    24: {"s": 23, "e": 29},

    25: {"s": 17, "e": 26},
    26: {"o": 25, "n": 27},
    27: {"s": 26, "e": 28},
    28: {"o": 27},
    29: {"o": 24, "e": 30},
    30: {"o": 29, "e": 31},
    31: {"o": 30},
# 32 (cielo) no se usa como sala visitable; es solo descriptiva para el final.
}


# Objetos iniciales por sala
OBJETOS_INICIALES = {
    1: ["comunicador"],
    2: ["modulo"],
    3: ["cuerda"],
    4: ["kyber"],
    5: ["raciones"],
    8: ["simbolo"],
    9: ["sable"],
    14: ["datapad"],
    18: ["disfraz"],
    19: ["tarjeta"],
    23: ["combustible"],
    15: ["artefacto"],
}

# Descripciones de objetos
DESCRIPCIONES_OBJETOS = {
    "comunicador": {
        "sala": "Un pequeño comunicador portátil, cubierto de polvo rojizo.",
        "inventario": "Tu comunicador portátil, con el canal rebelde memorizado."
    },
    "modulo": {
        "sala": "Un módulo de circuitos medio fundido, arrancado de algún panel imperial.",
        "inventario": "Un módulo de circuitos que quizá puedas acoplar a alguna máquina estropeada."
    },
    "cuerda": {
        "sala": "Una resistente cuerda de fibra, algo deshilachada pero útil.",
        "inventario": "Una cuerda de fibra que podría ayudarte a subir o bajar por algún lugar peligroso."
    },
    "kyber": {
        "sala": "Un pequeño cristal kyber rojizo, que vibra suavemente en tu mano.",
        "inventario": "Llevas contigo un cristal kyber impregnado del Lado Oscuro."
    },
    "raciones": {
        "sala": "Un paquete de raciones de campaña casi intacto.",
        "inventario": "Un paquete de raciones de campaña; no es sabroso, pero alimenta."
    },
    "simbolo": {
        "sala": "Un medallón de metal oscuro con el emblema de un antiguo linaje Sith.",
        "inventario": "Llevas un medallón Sith que podría abrir puertas antiguas."
    },
    "sable": {
        "sala": "Un viejo sable láser inservible; solo queda la empuñadura quemada.",
        "inventario": "La empuñadura de un sable láser sin energía, más simbólica que útil."
    },
    "datapad": {
        "sala": "Un datapad imperial con informes sobre el templo y el artefacto.",
        "inventario": "El datapad imperial; en él se detallan planes sobre el artefacto y la base."
    },
    "disfraz": {
        "sala": "Una armadura de soldado de asalto, algo dañada pero utilizable como disfraz.",
        "inventario": "Llevas puesto (o cargando) un disfraz de soldado imperial bastante convincente."
    },
    "tarjeta": {
        "sala": "Una tarjeta de acceso imperial con alto nivel de autorización.",
        "inventario": "Una tarjeta de acceso que abre puertas protegidas de la base."
    },
    "combustible": {
        "sala": "Un contenedor de combustible compatible con naves Lambda.",
        "inventario": "Un contenedor de combustible listo para cargar en una nave Lambda."
    },
    "artefacto": {
        "sala": "Un artefacto Sith de diseño intrincado. Sientes que algo dentro de ti reacciona a su presencia.",
        "inventario": "Llevas el artefacto Sith. Su poder es inquietante, pero podría cambiar el rumbo de la guerra."
    },
}


def clonar_objetos_iniciales():
    """Devuelve una copia del estado inicial de objetos."""
    return {hab: list(objs) for hab, objs in OBJETOS_INICIALES.items()}


# Estado global adicional (condiciones de la aventura)
estado = {}


def restablecer_estado_inicial():
    """Restituye inventario, posición y objetos como si empezara una partida nueva."""
    global habitacion_actual, inventario, objetos_en_sala, estado
    habitacion_actual = 1
    inventario = []
    objetos_en_sala = clonar_objetos_iniciales()
    estado = {
        "torre_reparada": False,
        "pasadizo_eco_abierto": False,
        "prisionero_libre": False,
        "generador_sabotado": False,
        "contacto_flota": False,
    }


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
    return nombre_visible_sala(nombre)


# Articles and gender/number map for objects shown in rooms
GENERO_OBJETOS = {
    # Singular masculino
    "comunicador": "m",
    "modulo": "m",
    "kyber": "m",
    "simbolo": "m",
    "sable": "m",
    "datapad": "m",
    "disfraz": "m",
    "combustible": "m",
    "artefacto": "m",
    # Singular femenino
    "cuerda": "f",
    "tarjeta": "f",
    # Plural femenino
    "raciones": "fp",
}

def _articulo_indefinido(genero):
    if genero == "m":
        return "un"
    if genero == "f":
        return "una"
    if genero == "mp":
        return "unos"
    if genero == "fp":
        return "unas"
    return "un"

def nombre_visible_sala(nombre):
    """Nombre del objeto en sala con articulo indefinido adecuado."""
    genero = GENERO_OBJETOS.get(nombre)
    if genero is None:
        n = nombre.lower()
        if n.endswith("as"):
            genero = "fp"
        elif n.endswith("os"):
            genero = "mp"
        elif n.endswith("a"):
            genero = "f"
        else:
            genero = "m"
    art = _articulo_indefinido(genero)
    return f"{art} {nombre}"

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
    visibles = [nombre_visible_sala(o) for o in objs]
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
# 4. MOTOR DEL JUEGO
# ---------------------------

def ejecutar_comando(verbo, objeto):
    """Devuelve (nueva_hab, descripcion_sala, mensaje_extra)."""
    global habitacion_actual, inventario, objetos_en_sala, estado
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
        dir_norm = objeto
        if dir_norm not in ["n", "s", "e", "o", "subir", "bajar"]:
            return hab, descripcion_con_objetos(hab), "No puedes ir en esa dirección."

        salidas_hab = SALIDAS.get(hab, {})
        destino = salidas_hab.get(dir_norm)
        if destino is None:
            return hab, descripcion_con_objetos(hab), "No puedes ir en esa dirección."

        # Restricciones especiales
        if hab == 7 and dir_norm == "bajar" and "simbolo" not in inventario:
            return hab, descripcion_con_objetos(hab), (
                "La puerta de piedra no reacciona; quizá necesites algún símbolo Sith."
            )
        if hab == 10 and dir_norm == "e" and not estado.get("pasadizo_eco_abierto", False):
            return hab, descripcion_con_objetos(hab), (
                "El eco te devuelve tus pasos, pero la pared este sigue cerrada."
            )

        return destino, descripcion_con_objetos(destino), None

    # GRITAR en sala del eco (abre pasadizo)
    if verbo in ["gritar"] and hab == 10:
        estado["pasadizo_eco_abierto"] = True
        return hab, descripcion_con_objetos(hab), (
            "Tu grito retumba una y otra vez hasta que oyes un clic en la pared este."
        )

    # CONTACTAR con la flota en centro de comunicaciones
    if verbo in ["contactar", "comunicar", "transmitir"] and hab == 20:
        if not estado.get("contacto_flota", False):
            estado["contacto_flota"] = True
            return hab, descripcion_con_objetos(hab), (
                "Logras enviar un mensaje codificado a la flota Rebelde. "
                "Una voz te confirma la recepción y promete apoyo."
            )
        else:
            return hab, descripcion_con_objetos(hab), "Ya has establecido contacto con la flota Rebelde."

    # SABOTEAR generador
    if verbo in ["sabotear"] and hab == 21:
        if not estado.get("generador_sabotado", False):
            estado["generador_sabotado"] = True
            return hab, descripcion_con_objetos(hab), (
                "Manipulas los controles del generador hasta que comienzan a saltar chispas. "
                "El campo de energía de la base falla."
            )
        else:
            return hab, descripcion_con_objetos(hab), "El generador ya está inestable y a punto de colapsar."

    # LIBERAR prisionero
    if verbo in ["liberar"] and hab == 22:
        if not estado.get("prisionero_libre", False):
            estado["prisionero_libre"] = True
            return hab, descripcion_con_objetos(hab), (
                "Forzas el cierre de la celda y el prisionero Rebelde queda libre. "
                "Te agradece la ayuda y te promete apoyo desde las sombras."
            )
        else:
            return hab, descripcion_con_objetos(hab), "Las celdas ya están abiertas y vacías."

    # REPARAR torre de señal con el módulo
    if verbo in ["reparar"] and hab == 6:
        if "modulo" in inventario and not estado.get("torre_reparada", False):
            estado["torre_reparada"] = True
            return hab, descripcion_con_objetos(hab), (
                "Acoplas el módulo a la torre de señal. Varias luces se encienden: "
                "las comunicaciones de largo alcance vuelven a funcionar."
            )
        elif estado.get("torre_reparada", False):
            return hab, descripcion_con_objetos(hab), "La torre de señal ya está reparada."
        else:
            return hab, descripcion_con_objetos(hab), "No tienes nada con lo que reparar la torre."

    # DESPEGAR desde la nave Lambda (final del juego)
    if verbo == "despegar":
        if hab != 31:
            return hab, descripcion_con_objetos(hab), "Aquí no hay ninguna nave desde la que puedas despegar."
        faltan = []
        if "artefacto" not in inventario:
            faltan.append("el artefacto Sith")
        if "combustible" not in inventario:
            faltan.append("combustible para la nave")
        if not estado.get("contacto_flota", False):
            faltan.append("contactar con la flota Rebelde")
        if not estado.get("generador_sabotado", False):
            faltan.append("sabotar el generador imperial")

        if faltan:
            return hab, descripcion_con_objetos(hab), (
                "Aún no puedes despegar: te falta " + lista_a_texto_natural(faltan) + "."
            )

        mensaje_final = (
            "Cargas el combustible, programas las coordenadas y elevas la nave Lambda hacia el cielo de Korriban.\n\n"
            "Has escapado con el artefacto Sith y has dejado la base imperial al borde del colapso.\n"
            "La flota Rebelde te espera para analizar el objeto y decidir su destino.\n\n"
            "¡HAS COMPLETADO LA AVENTURA!"
        )
        cerrar_juego_despues(mensaje_final)
        return hab, descripcion_con_objetos(hab), mensaje_final

    # FIN DEL JUEGO manual
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
fondo.title("Star Quest. Sombras de Korriban")
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
