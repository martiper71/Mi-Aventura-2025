# motor.py
import datos

# Variables de estado global
habitacion_actual = 1
inventario = []
objetos_en_sala = {}
estado = {}

def clonar_objetos_iniciales():
    """Devuelve una copia del estado inicial de objetos."""
    copia = {}
    for k, v in datos.OBJETOS_INICIALES.items():
        copia[k] = list(v)
    return copia

def restablecer_estado_inicial():
    """Restituye inventario, posición y objetos como si empezara una partida nueva."""
    global habitacion_actual, inventario, objetos_en_sala, estado
    habitacion_actual = 1
    inventario = []
    objetos_en_sala = clonar_objetos_iniciales()
    estado = {}

# Inicializamos por primera vez
restablecer_estado_inicial()

def objetos_visibles_en_sala(hab):
    """Devuelve la lista de objetos visibles en una sala (sin condiciones especiales)."""
    return objetos_en_sala.get(hab, [])

# ---------------------------
# HELPERS DE TEXTO / OBJETOS
# ---------------------------

def lista_a_texto_natural(lista):
    """
    ["camisa"] -> "camisa"
    ["camisa","pan"] -> "camisa y pan"
    ["a","b","c"] -> "a, b y c"
    """
    if not lista:
        return ""
    if len(lista) == 1:
        return lista[0]
    return ", ".join(lista[:-1]) + " y " + lista[-1]

def nombre_visible_inventario(nombre):
    """Cómo se nombra un objeto de forma humana. Por defecto, su nombre literal."""
    return nombre

def _articulo_indefinido(genero):
    if genero == "m": return "un"
    if genero == "f": return "una"
    if genero == "mp": return "unos"
    if genero == "fp": return "unas"
    return "un"

def nombre_visible_sala(nombre):
    """Nombre del objeto en sala con articulo indefinido adecuado."""
    gen = datos.GENERO_OBJETOS.get(nombre, "m")
    art = _articulo_indefinido(gen)
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
    info = datos.DESCRIPCIONES_OBJETOS.get(nombre)
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
    base = datos.txt_base[hab]
    objs = objetos_visibles_en_sala(hab)
    if len(objs) == 0:
        return base
    visibles = [nombre_visible_sala(o) for o in objs]
    extra = f" También puedes observar que hay {lista_a_texto_natural(visibles)}."
    return base + " " + extra.strip()

# ---------------------------
# PARSER
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
# MOTOR DEL JUEGO
# ---------------------------

def ejecutar_comando(verbo, objeto):
    """
    Devuelve (nueva_hab, descripcion_sala, mensaje_extra, fin_juego).
    fin_juego es un booleano o string con mensaje final.
    """
    global habitacion_actual, inventario, objetos_en_sala, estado
    hab = habitacion_actual

    # INVENTARIO
    if verbo == "inventario":
        return hab, descripcion_con_objetos(hab), inventario_texto(), False

    # MIRAR / EXAMINAR
    if verbo in ["examinar", "mirar"]:
        if objeto:
            nombre = normaliza_objeto_usuario(objeto)
            if nombre in objetos_visibles_en_sala(hab):
                return hab, descripcion_con_objetos(hab), descripcion_objeto(nombre, "sala"), False
            if nombre in inventario:
                return hab, descripcion_con_objetos(hab), descripcion_objeto(nombre, "inventario"), False
            return hab, descripcion_con_objetos(hab), "No ves nada especial.", False
        return hab, descripcion_con_objetos(hab), None, False

    # COGER
    if verbo in ["coger", "agarrar", "tomar"]:
        if not objeto:
            return hab, descripcion_con_objetos(hab), "¿Coger qué?", False
        nombre = normaliza_objeto_usuario(objeto)
        if nombre not in objetos_visibles_en_sala(hab):
            return hab, descripcion_con_objetos(hab), "Eso no está aquí.", False
        sala_objs = objetos_en_sala.get(hab, [])
        if nombre in sala_objs:
            sala_objs.remove(nombre)
            inventario.append(nombre)
            return hab, descripcion_con_objetos(hab), f"Has cogido {nombre_visible_inventario(nombre)}.", False
        return hab, descripcion_con_objetos(hab), "Eso no está aquí.", False

    # DEJAR
    if verbo in ["dejar", "soltar"]:
        if not objeto:
            return hab, descripcion_con_objetos(hab), "¿Dejar qué?", False
        nombre = normaliza_objeto_usuario(objeto)
        if nombre in inventario:
            inventario.remove(nombre)
            objetos_en_sala.setdefault(hab, []).append(nombre)
            return hab, descripcion_con_objetos(hab), f"Has dejado {nombre_visible_inventario(nombre)} aquí.", False
        return hab, descripcion_con_objetos(hab), "No llevas eso.", False

    # MOVERSE
    if verbo == "ir":
        dir_norm = objeto
        if dir_norm not in ["n", "s", "e", "o", "subir", "bajar"]:
            return hab, descripcion_con_objetos(hab), "No puedes ir en esa dirección.", False

        salidas_hab = datos.SALIDAS.get(hab, {})
        destino = salidas_hab.get(dir_norm)
        if destino is None:
            return hab, descripcion_con_objetos(hab), "No puedes ir en esa dirección.", False

        # Restricciones especiales
        if hab == 7 and dir_norm == "bajar" and "simbolo" not in inventario:
            return hab, descripcion_con_objetos(hab), (
                "La puerta de piedra no reacciona; quizá necesites algún símbolo Sith."
            ), False
        if hab == 10 and dir_norm == "e" and not estado.get("pasadizo_eco_abierto", False):
            return hab, descripcion_con_objetos(hab), (
                "El eco te devuelve tus pasos, pero la pared este sigue cerrada."
            ), False

        return destino, descripcion_con_objetos(destino), None, False

    # GRITAR en sala del eco (abre pasadizo)
    if verbo in ["gritar"] and hab == 10:
        estado["pasadizo_eco_abierto"] = True
        return hab, descripcion_con_objetos(hab), (
            "Tu grito retumba una y otra vez hasta que oyes un clic en la pared este."
        ), False

    # CONTACTAR con la flota en centro de comunicaciones
    if verbo in ["contactar", "comunicar", "transmitir"] and hab == 20:
        if not estado.get("contacto_flota", False):
            estado["contacto_flota"] = True
            return hab, descripcion_con_objetos(hab), (
                "Logras enviar un mensaje codificado a la flota Rebelde. "
                "Una voz te confirma la recepción y promete apoyo."
            ), False
        else:
            return hab, descripcion_con_objetos(hab), "Ya has establecido contacto con la flota Rebelde.", False

    # SABOTEAR generador
    if verbo in ["sabotear"] and hab == 21:
        if not estado.get("generador_sabotado", False):
            estado["generador_sabotado"] = True
            return hab, descripcion_con_objetos(hab), (
                "Manipulas los controles del generador hasta que comienzan a saltar chispas. "
                "El campo de energía de la base falla."
            ), False
        else:
            return hab, descripcion_con_objetos(hab), "El generador ya está inestable y a punto de colapsar.", False

    # LIBERAR prisionero
    if verbo in ["liberar"] and hab == 22:
        if not estado.get("prisionero_libre", False):
            estado["prisionero_libre"] = True
            return hab, descripcion_con_objetos(hab), (
                "Forzas el cierre de la celda y el prisionero Rebelde queda libre. "
                "Te agradece la ayuda y te promete apoyo desde las sombras."
            ), False
        else:
            return hab, descripcion_con_objetos(hab), "Las celdas ya están abiertas y vacías.", False

    # REPARAR torre de señal con el módulo
    if verbo in ["reparar"] and hab == 6:
        if "modulo" in inventario and not estado.get("torre_reparada", False):
            estado["torre_reparada"] = True
            inventario.remove("modulo")
            return hab, descripcion_con_objetos(hab), (
                "Acoplas el módulo a la torre de señal. Varias luces se encienden: "
                "las comunicaciones de largo alcance vuelven a funcionar. El módulo queda integrado y ya no lo llevas."
            ), False
        elif estado.get("torre_reparada", False):
            return hab, descripcion_con_objetos(hab), "La torre de señal ya está reparada.", False
        else:
            return hab, descripcion_con_objetos(hab), "No tienes nada con lo que reparar la torre.", False

    # DESPEGAR desde la nave Lambda (final del juego)
    if verbo == "despegar":
        if hab != 31:
            return hab, descripcion_con_objetos(hab), "Aquí no hay ninguna nave desde la que puedas despegar.", False
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
            ), False

        mensaje_final = (
            "Cargas el combustible, programas las coordenadas y elevas la nave Lambda hacia el cielo de Korriban.\n\n"
            "Has escapado con el artefacto Sith y has dejado la base imperial al borde del colapso.\n"
            "La flota Rebelde te espera para analizar el objeto y decidir su destino.\n\n"
            "¡HAS COMPLETADO LA AVENTURA!"
        )
        return hab, descripcion_con_objetos(hab), mensaje_final, True

    # FIN DEL JUEGO manual
    if verbo == "fin":
        mensaje_final = "Gracias por jugar."
        return hab, descripcion_con_objetos(hab), mensaje_final, True

    # Otro comando
    return hab, descripcion_con_objetos(hab), "¿Cómo dices?", False
