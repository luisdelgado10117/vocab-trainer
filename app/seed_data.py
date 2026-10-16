"""
Paquete de vocabulario inicial: los verbos irregulares más comunes del
inglés, con sus 3 formas (presente, pasado, participio) y traducción.

Cada entrada ahora incluye:
    - group: identifica a qué verbo pertenece (ej. "go"), para poder
      agrupar sus 3 formas juntas en la app.
    - tense: cuál forma es esta ("infinitivo", "pasado", "participio").

MANTENER LOS DATOS SEPARADOS DE LA LÓGICA es una buena práctica: si mañana
quieres agregar más verbos, o un paquete distinto, solo tocas este archivo.
"""

IRREGULAR_VERBS_PACK = [
    # be
    {"word": "be", "translation": "ser / estar", "group": "be", "tense": "infinitivo"},
    {
        "word": "was/were",
        "translation": "fui / fue / eras",
        "group": "be",
        "tense": "pasado",
    },
    {
        "word": "been",
        "translation": "sido / estado",
        "group": "be",
        "tense": "participio",
    },
    # have
    {
        "word": "have",
        "translation": "tener / haber",
        "group": "have",
        "tense": "infinitivo",
    },
    {
        "word": "had",
        "translation": "tuve / tuvo / había",
        "group": "have",
        "tense": "pasado",
    },
    {"word": "had", "translation": "tenido", "group": "have", "tense": "participio"},
    # do
    {"word": "do", "translation": "hacer", "group": "do", "tense": "infinitivo"},
    {"word": "did", "translation": "hice / hizo", "group": "do", "tense": "pasado"},
    {"word": "done", "translation": "hecho", "group": "do", "tense": "participio"},
    # go
    {"word": "go", "translation": "ir", "group": "go", "tense": "infinitivo"},
    {"word": "went", "translation": "fui / fue", "group": "go", "tense": "pasado"},
    {"word": "gone", "translation": "ido", "group": "go", "tense": "participio"},
    # get
    {
        "word": "get",
        "translation": "obtener / conseguir",
        "group": "get",
        "tense": "infinitivo",
    },
    {
        "word": "got",
        "translation": "obtuve / consiguió",
        "group": "get",
        "tense": "pasado",
    },
    {
        "word": "gotten",
        "translation": "obtenido",
        "group": "get",
        "tense": "participio",
    },
    # make
    {
        "word": "make",
        "translation": "hacer / fabricar",
        "group": "make",
        "tense": "infinitivo",
    },
    {"word": "made", "translation": "hice / hizo", "group": "make", "tense": "pasado"},
    {
        "word": "made",
        "translation": "hecho/fabricado",
        "group": "make",
        "tense": "participio",
    },
    # know
    {
        "word": "know",
        "translation": "saber / conocí",
        "group": "know",
        "tense": "infinitivo",
    },
    {
        "word": "knew",
        "translation": "supe / conocí",
        "group": "know",
        "tense": "pasado",
    },
    {
        "word": "known",
        "translation": "sabido / conocido",
        "group": "know",
        "tense": "participio",
    },
    # take
    {"word": "take", "translation": "tomar", "group": "take", "tense": "infinitivo"},
    {"word": "took", "translation": "tomé / tomó", "group": "take", "tense": "pasado"},
    {"word": "taken", "translation": "tomado", "group": "take", "tense": "participio"},
    # see
    {"word": "see", "translation": "ver", "group": "see", "tense": "infinitivo"},
    {"word": "saw", "translation": "vi / vio", "group": "see", "tense": "pasado"},
    {"word": "seen", "translation": "visto", "group": "see", "tense": "participio"},
    # come
    {"word": "come", "translation": "venir", "group": "come", "tense": "infinitivo"},
    {"word": "came", "translation": "vine / vino", "group": "come", "tense": "pasado"},
    {"word": "come", "translation": "venido", "group": "come", "tense": "participio"},
    # give
    {"word": "give", "translation": "dar", "group": "give", "tense": "infinitivo"},
    {"word": "gave", "translation": "di / dio", "group": "give", "tense": "pasado"},
    {"word": "given", "translation": "dado", "group": "give", "tense": "participio"},
    # find
    {
        "word": "find",
        "translation": "encontrar",
        "group": "find",
        "tense": "infinitivo",
    },
    {
        "word": "found",
        "translation": "encontré / encontró",
        "group": "find",
        "tense": "pasado",
    },
    {
        "word": "found",
        "translation": "encontrado",
        "group": "find",
        "tense": "participio",
    },
    # tell
    {
        "word": "tell",
        "translation": "decir / contar",
        "group": "tell",
        "tense": "infinitivo",
    },
    {"word": "told", "translation": "dije / dijo", "group": "tell", "tense": "pasado"},
    {"word": "told", "translation": "dicho", "group": "tell", "tense": "participio"},
    # think
    {"word": "think", "translation": "pensar", "group": "think", "tense": "infinitivo"},
    {
        "word": "thought",
        "translation": "pensé / pensó",
        "group": "think",
        "tense": "pasado",
    },
    {
        "word": "thought",
        "translation": "pensado",
        "group": "think",
        "tense": "participio",
    },
    # feel
    {"word": "feel", "translation": "sentir", "group": "feel", "tense": "infinitivo"},
    {
        "word": "felt",
        "translation": "sentí / sintió",
        "group": "feel",
        "tense": "pasado",
    },
    {"word": "felt", "translation": "sentido", "group": "feel", "tense": "participio"},
]

# Se llena en el paso 3 (30 phrasal verbs). Cada entrada usa:
# word = "give up", translation = "rendirse", group = "give", tense = None
PHRASAL_VERBS_PACK = [
    # give
    {
        "word": "give up",
        "translation": "rendirse / dejar de",
        "group": "give",
        "tense": None,
    },
    {"word": "give in", "translation": "ceder", "group": "give", "tense": None},
    {
        "word": "give away",
        "translation": "regalar / revelar",
        "group": "give",
        "tense": None,
    },
    # get
    {"word": "get up", "translation": "levantarse", "group": "get", "tense": None},
    {
        "word": "get along",
        "translation": "llevarse bien",
        "group": "get",
        "tense": None,
    },
    {"word": "get over", "translation": "superar", "group": "get", "tense": None},
    # look
    {"word": "look for", "translation": "buscar", "group": "look", "tense": None},
    {"word": "look after", "translation": "cuidar", "group": "look", "tense": None},
    {
        "word": "look up",
        "translation": "buscar (en un diccionario)",
        "group": "look",
        "tense": None,
    },
    # turn
    {"word": "turn on", "translation": "encender", "group": "turn", "tense": None},
    {"word": "turn off", "translation": "apagar", "group": "turn", "tense": None},
    {
        "word": "turn down",
        "translation": "rechazar / bajar el volumen",
        "group": "turn",
        "tense": None,
    },
    # take
    {
        "word": "take off",
        "translation": "despegar / quitarse",
        "group": "take",
        "tense": None,
    },
    {
        "word": "take care of",
        "translation": "encargarse de / cuidar",
        "group": "take",
        "tense": None,
    },
    {
        "word": "take over",
        "translation": "tomar el control",
        "group": "take",
        "tense": None,
    },
    # put
    {"word": "put on", "translation": "ponerse (ropa)", "group": "put", "tense": None},
    {"word": "put off", "translation": "posponer", "group": "put", "tense": None},
    {"word": "put out", "translation": "apagar (fuego)", "group": "put", "tense": None},
    # come
    {"word": "come back", "translation": "regresar", "group": "come", "tense": None},
    {
        "word": "come up with",
        "translation": "idear / se le ocurre",
        "group": "come",
        "tense": None,
    },
    {
        "word": "come across",
        "translation": "encontrarse con",
        "group": "come",
        "tense": None,
    },
    # go
    {
        "word": "go on",
        "translation": "continuar / suceder",
        "group": "go",
        "tense": None,
    },
    {"word": "go out", "translation": "salir", "group": "go", "tense": None},
    {"word": "go back", "translation": "volver", "group": "go", "tense": None},
    # set
    {
        "word": "set up",
        "translation": "configurar / establecer",
        "group": "set",
        "tense": None,
    },
    {
        "word": "set off",
        "translation": "partir / activar",
        "group": "set",
        "tense": None,
    },
    # break
    {
        "word": "break down",
        "translation": "averiarse / desglosar",
        "group": "break",
        "tense": None,
    },
    {
        "word": "break up",
        "translation": "terminar (una relación)",
        "group": "break",
        "tense": None,
    },
    # run
    {
        "word": "run out of",
        "translation": "quedarse sin",
        "group": "run",
        "tense": None,
    },
    {"word": "run into", "translation": "toparse con", "group": "run", "tense": None},
]

# Clave = nombre de la categoría (se guarda en Card.category).
# Para agregar una categoría nueva en el futuro: crear su lista y sumarla aquí.
SEED_PACKS = {
    "irregular_verbs": IRREGULAR_VERBS_PACK,
    "phrasal_verbs": PHRASAL_VERBS_PACK,
}
