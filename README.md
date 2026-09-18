# Entrenador de vocabulario (repetición espaciada)

Una app de línea de comandos para aprender vocabulario de inglés usando
**repetición espaciada** (el algoritmo SM-2, el mismo que usa Anki). En
vez de repasar todas las palabras por igual, el sistema calcula cuándo
te conviene ver cada palabra de nuevo, según qué tan bien la recordaste
la última vez.

## 🚧 Estado del proyecto

**Fase 1 - Completada:** algoritmo SM-2 + interfaz de consola (CLI).

Próximas fases planeadas:

- [ ] Convertir en API REST (reutilizando patrones de mi otro proyecto: Flask + PostgreSQL + JWT)
- [ ] Estadísticas de progreso (palabras dominadas, racha de días estudiando)
- [ ] App móvil en Flutter
- [ ] Notificaciones push recordando repasar

## 📦 Instalación

```bash
git clone <url-de-tu-repo>
cd vocab-trainer
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Cómo usarlo

```bash
python cli.py
```

Vas a ver un menú para:

1. Agregar palabras nuevas (inglés -> español)
2. Repasar las palabras que ya toca ver hoy
3. Ver todas tus palabras y su próxima fecha de repaso
4. Salir (guarda tu progreso automáticamente)

Tu vocabulario se guarda en `data/deck.json` (no se sube a GitHub, es tu progreso personal).

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
