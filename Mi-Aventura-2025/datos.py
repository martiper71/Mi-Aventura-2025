# datos.py
# Contiene los datos estáticos del juego: textos, mapa, objetos.

# Descripción base fija por sala. El índice es el número de habitación.
txt_base = [
    "Portada\n\nSTAR QUEST: SOMBRAS DE KORRIBAN",
    # 1
    "Te despiertas entre chispas y humo dentro de la cápsula de escape de tu carguero. "
    "El cristal delantero está roto y, fuera, solo ves un océano de arena rojiza.",
    # 2
    "Estás ante los restos humeantes de la cápsula. El calor es sofocante. "
    "Al norte se divisan unas ruinas antiguas.",
    # 3
    "Caminas por el desierto. La arena se te mete en las botas. "
    "Al norte, las ruinas parecen más grandes. Al sur, la cápsula.",
    # 4
    "Llegas a la entrada de un valle rocoso. Estatuas gigantescas de Lores Sith "
    "te observan desde las alturas. Hay una entrada oscura al norte.",
    # 5
    "Estás en la antecámara de un templo antiguo. El aire es frío y viciado. "
    "Hay pasillos al este y al oeste. Al norte, una gran puerta cerrada.",
    # 6
    "Un pasillo lateral con jeroglíficos borrados por el tiempo. "
    "Al final del pasillo ves una antigua torre de señalización republicana, "
    "probablemente de una expedición anterior fallida.",
    # 7
    "Un pasillo oscuro que desciende hacia las profundidades. "
    "Huele a humedad y a algo metálico.",
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
    "Una sala de meditación Sith. Hay cojines podridos y un altar bajo en el centro.",
    # 13
    "La armería del templo. Estanterías vacías, salvo por algunos restos oxidados.",
    # 14
    "Una biblioteca antigua. Los pergaminos se deshacen al tocarlos, pero hay un datapad que parece intacto.",
    # 15
    "La cámara del tesoro. El brillo del oro es tentador, pero tu objetivo es otro.",
    # 16
    "Un pasadizo secreto, estrecho y polvoriento. Apenas cabes por él.",
    # 17
    "Una cripta funeraria. Sarcófagos de piedra se alinean en las paredes.",
    # 18
    "Un laboratorio Sith. Frascos con líquidos extraños y diagramas de anatomía alienígena.",
    # 19
    "La sala del trono. Un asiento de piedra negra domina la estancia.",
    # 20
    "Pantallas, consolas y un gran transmisor apuntando al cielo. Se oyen débiles voces imperiales por los altavoces.\n"
    "Tal vez puedas CONTACTAR con la flota Rebelde desde aquí.",
    # 21
    "Un generador rugiente llena la sala con un zumbido constante. Varias conducciones energéticas salen de él.\n"
    "Si lo SABOTEAS podrías desactivar parte de las defensas imperiales.",
    # 22
    "Celdas de energía. La mayoría están vacías, pero en una ves a un prisionero con uniforme Rebelde.\n"
    "Podrías LIBERAR al prisionero.",
    # 23
    "Un hangar imperial. Cazas TIE están aparcados en filas, pero buscas algo con hiperimpulsor.",
    # 24
    "El puesto de mando. Oficiales imperiales van y vienen (o lo harían si no estuviera todo desierto por la alarma).",
    # 25
    "Un almacén de suministros. Cajas con el logo imperial se apilan hasta el techo.",
    # 26
    "La enfermería. Droides médicos desactivados y olor a bacta.",
    # 27
    "Dormitorios de la tropa. Literas perfectamente hechas.",
    # 28
    "La cantina. Mesas volcadas y comida a medio terminar.",
    # 29
    "Un pasillo de acceso al nivel superior. Las luces rojas de emergencia parpadean.",
    # 30
    "La plataforma de aterrizaje exterior. El viento aúlla y la arena golpea tu cara.",
    # 31
    "Un transporte imperial de tipo Lambda espera en la plataforma, con la rampa de acceso bajada.\n"
    "Cuando lo tengas todo listo, escribe DESPEGAR.",
    # 32
    "Te elevas sobre el planeta, dejando atrás el templo, la base imperial y los ecos del Lado Oscuro."
]

# Rutas de imágenes por índice de habitación (000..032).
img = [f"imagenes/{i:03d}.png" for i in range(33)]

# Mapa de conexiones entre habitaciones
# n=norte, s=sur, e=este, o=oeste
# subir, bajar
SALIDAS = {
    1: {"n": 2},
    2: {"s": 1, "n": 3},
    3: {"s": 2, "n": 4},
    4: {"s": 3, "n": 5},
    5: {"s": 4, "e": 6, "o": 8, "n": 10},
    6: {"o": 5},
    7: {"subir": 8},
    8: {"e": 5, "bajar": 7, "n": 9},
    9: {"s": 8},
    10: {"s": 5, "n": 11},  # "e": 16 (oculto, se abre con evento)
    11: {"s": 10, "e": 12, "o": 13, "n": 14},
    12: {"o": 11},
    13: {"e": 11},
    14: {"s": 11, "e": 15},
    15: {"o": 14},
    16: {"o": 10, "e": 17},
    17: {"o": 16, "n": 18},
    18: {"s": 17, "n": 19},
    19: {"s": 18, "e": 20}, # Conexión a base imperial
    20: {"o": 19, "n": 21, "e": 24},
    21: {"s": 20, "e": 22},
    22: {"o": 21, "e": 23},
    23: {"o": 22, "n": 25},
    24: {"o": 20, "e": 29},
    25: {"s": 23, "e": 26},
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
        "sala": "Un módulo de reparación estándar, medio enterrado en la arena.",
        "inventario": "Un módulo de reparación universal. Podría servir para arreglar tecnología antigua."
    },
    "cuerda": {
        "sala": "Una cuerda sintética resistente abandonada.",
        "inventario": "Una cuerda fuerte y ligera."
    },
    "kyber": {
        "sala": "Un pequeño cristal brilla débilmente entre las rocas. Parece un cristal Kyber.",
        "inventario": "Un fragmento de cristal Kyber. Sientes una leve vibración al tocarlo."
    },
    "raciones": {
        "sala": "Un paquete de raciones de emergencia.",
        "inventario": "Raciones de supervivencia. No saben a nada, pero nutren."
    },
    "simbolo": {
        "sala": "Un medallón de metal con un extraño símbolo grabado.",
        "inventario": "Un medallón con un símbolo Sith. Parece una llave."
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
        "sala": "Un uniforme de oficial imperial, doblado en un rincón.",
        "inventario": "Un uniforme de oficial imperial. Podría servirte para pasar desapercibido."
    },
    "tarjeta": {
        "sala": "Una tarjeta de acceso de seguridad nivel 1.",
        "inventario": "Una tarjeta de acceso imperial."
    },
    "combustible": {
        "sala": "Un bidón de combustible para naves estelares.",
        "inventario": "Combustible refinado de alto grado. Pesado, pero necesario."
    },
    "artefacto": {
        "sala": "Un artefacto Sith de diseño intrincado. Sientes que algo dentro de ti reacciona a su presencia.",
        "inventario": "Llevas el artefacto Sith. Su poder es inquietante, pero podría cambiar el rumbo de la guerra."
    },
}


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
