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
