# Entrenador de vocabulario (repetición espaciada)

Una app de línea de comandos para aprender vocabulario de inglés usando
**repetición espaciada** (el algoritmo SM-2, el mismo que usa Anki). En
vez de repasar todas las palabras por igual, el sistema calcula cuándo
te conviene ver cada palabra de nuevo, según qué tan bien la recordaste
la última vez.

## 🚧 Estado del proyecto

**Fase 1 - Completada:** algoritmo SM-2 + interfaz de consola (CLI).

**Fase 2 - Completada:** API REST con Flask, base de datos, y autenticación
(reutilizando el mismo algoritmo SM-2 de la Fase 1 sin modificarlo).

**Estadísticas de progreso - Completado:**
- [x] Racha de días de estudio (actual y la más larga histórica)
- [x] Conteo de tarjetas "dominadas" (intervalo ≥ 21 días, convención de Anki)
- [x] Tarjetas repasadas hoy
- [x] Endpoint `GET /stats`

Próximas fases planeadas:
- [ ] Migrar a PostgreSQL + CI/CD (igual que en mi proyecto anterior)
- [ ] Estadísticas de progreso (palabras dominadas, racha de días estudiando)
- [ ] App móvil en Flutter
- [ ] Notificaciones push recordando repasar

## 🏗️ Arquitectura del proyecto

```
vocab-trainer/
├── core/              -> el algoritmo SM-2, sin depender de nada externo
│   ├── card.py
│   ├── scheduler.py
│   └── deck.py
├── cli.py             -> interfaz de consola (usa core/ directamente)
├── app/               -> interfaz de API REST (también usa core/)
│   ├── main.py
│   ├── models.py
│   ├── card_manager.py
│   └── user_manager.py
└── tests/
```

La idea clave: **el algoritmo (`core/`) no sabe nada de Flask, bases de
datos, ni consola.** Por eso se pudo reutilizar tal cual al pasar de CLI
a API, sin tocarle una línea.

## 📦 Instalación

```bash
git clone <url-de-tu-repo>
cd vocab-trainer
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Cómo usarlo

**Opción A: por consola**
```bash
python cli.py
```

**Opción B: como API**
```bash
python -m app.main
```
Endpoints: `POST /register`, `POST /login`, `GET /cards`, `GET /cards/due`,
`POST /cards`, `POST /cards/<id>/review` (body: `{"quality": 0-5}`),
`GET /stats`.

## 🧠 Cómo funciona el algoritmo (SM-2)

Cada palabra tiene tres valores clave:

- **repetitions**: cuántas veces seguidas la has recordado bien
- **easiness_factor**: qué tan "fácil" es esta palabra para ti (empieza en 2.5)
- **interval**: cuántos días esperar antes del próximo repaso

Cada vez que repasas una palabra, te autocalificas del 0 al 5. Si calificas
menos de 3, se reinicia tu progreso en esa palabra (se repasa pronto de
nuevo). Si calificas 3 o más, el intervalo crece: 1 día -> 6 días -> 6 días
× easiness_factor -> eso otra vez × easiness_factor...

## 🧪 Cómo correr las pruebas

```bash
python -m pytest
```

## 🧠 Qué aprendí en esta fase

- Implementar un algoritmo real a partir de su especificación matemática (SM-2).
- Diseñar clases enfocadas en un solo propósito (`Card`, `Deck`, `review_card`).
- Usar `@dataclass` para clases que solo almacenan datos.
- Serializar y deserializar objetos propios a/desde JSON (`to_dict` / `from_dict`).
- Escribir pruebas que verifican reglas matemáticas/lógicas precisas, no solo "que no truene".