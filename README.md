# Chatbot de Orientación Vocacional Básico

Un chatbot súper simple para ayudar a decidir qué carrera universitaria estudiar según tus gustos e intereses.

## Características

- Chatbot básico y sencillo (como hecho por un principiante)
- Preguntas simples sobre gustos e intereses
- Sugerencias de carreras basadas en respuestas
- API REST con FastAPI
- Desplegado en Render

## Instalación Local

1. Instala las dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta el servidor:

```bash
uvicorn chatbot_carreras:app --reload
```

## Despliegue en Render

1. Conecta tu repositorio de GitHub a Render
2. Render detectará automáticamente que es una aplicación Python
3. Usará el archivo `render.yaml` para la configuración
4. El chatbot estará disponible en la URL proporcionada por Render

## Uso

### Local

1. Ve a `http://localhost:8000` para ver la bienvenida
2. Usa `http://localhost:8000/preguntas/` para ver las preguntas disponibles
3. Envía respuestas a `http://localhost:8000/sugerir_carrera/`

### En Producción (Render)

1. Ve a `https://tu-app.onrender.com` para ver la bienvenida
2. Usa `https://tu-app.onrender.com/preguntas/` para ver las preguntas disponibles
3. Envía respuestas a `https://tu-app.onrender.com/sugerir_carrera/`

## Formato de Request

```json
{
  "pregunta": "¿Te gusta trabajar con números y cálculos?",
  "respuesta_usuario": "si"
}
```

## Ejemplo de uso

```python
import requests

# Obtener preguntas
preguntas = requests.get("https://tu-app.onrender.com/preguntas/").json()

# Enviar respuesta
respuesta = requests.post("https://tu-app.onrender.com/sugerir_carrera/", json={
    "pregunta": "¿Te gusta trabajar con números y cálculos?",
    "respuesta_usuario": "si"
}).json()

print(respuesta)
```

## Preguntas disponibles

- ¿Te gusta trabajar con números y cálculos?
- ¿Te gusta ayudar a otras personas?
- ¿Te gusta crear cosas nuevas?
- ¿Te gusta trabajar en equipo?
- ¿Te gusta la tecnología y computadoras?
- ¿Te gusta leer y estudiar mucho?
- ¿Te gusta estar en contacto con la naturaleza?
- ¿Te gusta liderar y dirigir a otros?
- ¿Te gusta viajar y conocer nuevos lugares?
- ¿Te gusta hacer deporte y actividad física?

## Respuestas válidas

- "si" - Respuesta afirmativa
- "no" - Respuesta negativa
- "tal vez" - Respuesta intermedia

## Endpoints

- `GET /` - Página de bienvenida
- `GET /preguntas/` - Lista de preguntas disponibles
- `POST /sugerir_carrera/` - Obtener sugerencia de carrera
- `GET /health` - Health check
- `GET /docs` - Documentación automática de la API
