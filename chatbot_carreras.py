from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 1. Crear FastAPI
app = FastAPI(
    title="Chatbot de Orientación Vocacional Básico",
    description="Un chatbot simple para ayudar a elegir carrera universitaria",
    version="1.0.0"
)

# 2. Dataset expandido (preguntas sobre gustos e intereses)
data = pd.DataFrame([
    # Pregunta 1: Números y cálculos
    {
        "pregunta": "¿Te gusta trabajar con números y cálculos?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Matemáticas, Ingeniería, Contabilidad, Estadística",
        "area": "Ciencias Exactas",
        "descripcion": "Tienes aptitud para carreras que requieren pensamiento lógico y matemático."
    },
    {
        "pregunta": "¿Te gusta trabajar con números y cálculos?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Humanidades, Arte, Comunicación, Literatura",
        "area": "Ciencias Sociales",
        "descripcion": "Prefieres carreras más creativas y sociales."
    },
    {
        "pregunta": "¿Te gusta trabajar con números y cálculos?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Economía, Administración, Marketing",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes un balance entre lógica y creatividad."
    },
    
    # Pregunta 2: Ayudar a otros
    {
        "pregunta": "¿Te gusta ayudar a otras personas?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Medicina, Psicología, Trabajo Social, Enfermería",
        "area": "Ciencias de la Salud",
        "descripcion": "Tienes vocación de servicio, ideal para carreras de ayuda humanitaria."
    },
    {
        "pregunta": "¿Te gusta ayudar a otras personas?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Ingeniería, Tecnología, Ciencias, Investigación",
        "area": "Ciencias Exactas",
        "descripcion": "Prefieres carreras más técnicas y especializadas."
    },
    {
        "pregunta": "¿Te gusta ayudar a otras personas?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Educación, Recursos Humanos, Consultoría",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes habilidades sociales moderadas."
    },
    
    # Pregunta 3: Creatividad
    {
        "pregunta": "¿Te gusta crear cosas nuevas?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Diseño, Arquitectura, Arte, Música, Publicidad",
        "area": "Arte y Diseño",
        "descripcion": "Tienes creatividad, perfecto para carreras artísticas y de diseño."
    },
    {
        "pregunta": "¿Te gusta crear cosas nuevas?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Administración, Derecho, Economía, Contabilidad",
        "area": "Ciencias Sociales",
        "descripcion": "Prefieres carreras más estructuradas y tradicionales."
    },
    {
        "pregunta": "¿Te gusta crear cosas nuevas?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Marketing, Comunicación, Periodismo",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes un balance entre creatividad y estructura."
    },
    
    # Pregunta 4: Trabajo en equipo
    {
        "pregunta": "¿Te gusta trabajar en equipo?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Medicina, Enfermería, Educación, Trabajo Social",
        "area": "Ciencias de la Salud",
        "descripcion": "Tienes habilidades sociales, ideal para carreras colaborativas."
    },
    {
        "pregunta": "¿Te gusta trabajar en equipo?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Programación, Investigación, Escritura, Arte",
        "area": "Tecnología",
        "descripcion": "Prefieres trabajar de forma independiente."
    },
    {
        "pregunta": "¿Te gusta trabajar en equipo?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Ingeniería, Arquitectura, Consultoría",
        "area": "Ciencias Exactas",
        "descripcion": "Tienes flexibilidad para trabajar solo o en equipo."
    },
    
    # Pregunta 5: Tecnología
    {
        "pregunta": "¿Te gusta la tecnología y computadoras?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Ingeniería en Sistemas, Informática, Ciberseguridad, Robótica",
        "area": "Tecnología",
        "descripcion": "Tienes afinidad con la tecnología, perfecto para carreras IT."
    },
    {
        "pregunta": "¿Te gusta la tecnología y computadoras?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Medicina, Derecho, Psicología, Arte",
        "area": "Ciencias Sociales",
        "descripcion": "Prefieres carreras más humanísticas y tradicionales."
    },
    {
        "pregunta": "¿Te gusta la tecnología y computadoras?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Marketing Digital, Comunicación, Diseño Gráfico",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes interés moderado en tecnología."
    },
    
    # Pregunta 6: Lectura y estudio
    {
        "pregunta": "¿Te gusta leer y estudiar mucho?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Medicina, Derecho, Filosofía, Historia",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes disciplina para carreras que requieren mucho estudio."
    },
    {
        "pregunta": "¿Te gusta leer y estudiar mucho?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Arte, Música, Deportes, Gastronomía",
        "area": "Arte y Diseño",
        "descripcion": "Prefieres carreras más prácticas y creativas."
    },
    {
        "pregunta": "¿Te gusta leer y estudiar mucho?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Psicología, Educación, Comunicación",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes un balance entre estudio y práctica."
    },
    
    # Pregunta 7: Naturaleza
    {
        "pregunta": "¿Te gusta estar en contacto con la naturaleza?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Biología, Veterinaria, Agronomía, Ecología",
        "area": "Ciencias Naturales",
        "descripcion": "Tienes conexión con la naturaleza, ideal para carreras ambientales."
    },
    {
        "pregunta": "¿Te gusta estar en contacto con la naturaleza?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Ingeniería, Tecnología, Medicina, Derecho",
        "area": "Ciencias Exactas",
        "descripcion": "Prefieres ambientes urbanos y tecnológicos."
    },
    {
        "pregunta": "¿Te gusta estar en contacto con la naturaleza?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Arquitectura, Turismo, Geografía",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes interés moderado en la naturaleza."
    },
    
    # Pregunta 8: Liderazgo
    {
        "pregunta": "¿Te gusta liderar y dirigir a otros?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Administración, Política, Negocios, Recursos Humanos",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes habilidades de liderazgo, ideal para carreras directivas."
    },
    {
        "pregunta": "¿Te gusta liderar y dirigir a otros?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Investigación, Arte, Programación, Ciencias",
        "area": "Ciencias Exactas",
        "descripcion": "Prefieres trabajar de forma independiente."
    },
    {
        "pregunta": "¿Te gusta liderar y dirigir a otros?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Psicología, Educación, Consultoría",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes habilidades de liderazgo moderadas."
    },
    
    # Pregunta 9: Viajes
    {
        "pregunta": "¿Te gusta viajar y conocer nuevos lugares?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Turismo, Relaciones Internacionales, Periodismo",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes espíritu aventurero, ideal para carreras que involucran viajes."
    },
    {
        "pregunta": "¿Te gusta viajar y conocer nuevos lugares?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Medicina, Derecho, Ingeniería, Arte",
        "area": "Ciencias Exactas",
        "descripcion": "Prefieres carreras más estables y locales."
    },
    {
        "pregunta": "¿Te gusta viajar y conocer nuevos lugares?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Comunicación, Marketing, Arquitectura",
        "area": "Ciencias Sociales",
        "descripcion": "Tienes interés moderado en viajar."
    },
    
    # Pregunta 10: Deportes
    {
        "pregunta": "¿Te gusta hacer deporte y actividad física?",
        "respuesta_usuario": "si",
        "carrera_sugerida": "Educación Física, Medicina Deportiva, Nutrición",
        "area": "Ciencias de la Salud",
        "descripcion": "Tienes pasión por el deporte, ideal para carreras relacionadas con la actividad física."
    },
    {
        "pregunta": "¿Te gusta hacer deporte y actividad física?",
        "respuesta_usuario": "no",
        "carrera_sugerida": "Programación, Arte, Literatura, Ciencias",
        "area": "Ciencias Exactas",
        "descripcion": "Prefieres carreras más intelectuales y sedentarias."
    },
    {
        "pregunta": "¿Te gusta hacer deporte y actividad física?",
        "respuesta_usuario": "tal vez",
        "carrera_sugerida": "Psicología, Enfermería, Trabajo Social",
        "area": "Ciencias de la Salud",
        "descripcion": "Tienes un balance entre actividad física e intelectual."
    }
])

# 3. Modelo simple
X = data["respuesta_usuario"]
y = data["carrera_sugerida"]

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

model = MultinomialNB()
model.fit(X_vec, y)

# 4. Esquema de entrada
class RespuestaEntrada(BaseModel):
    pregunta: str
    respuesta_usuario: str

# 5. Ruta principal
@app.post("/sugerir_carrera/")
def sugerir_carrera(entrada: RespuestaEntrada):
    # Buscar la pregunta en el dataset
    fila = data[data["pregunta"] == entrada.pregunta]
   
    if fila.empty:
        return {"error": "Pregunta no encontrada en el dataset."}

    # Buscar respuesta exacta primero
    respuesta_exacta = fila[fila["respuesta_usuario"].str.lower() == entrada.respuesta_usuario.strip().lower()]
    
    if not respuesta_exacta.empty:
        return {
            "carrera_sugerida": respuesta_exacta["carrera_sugerida"].iloc[0],
            "area": respuesta_exacta["area"].iloc[0],
            "descripcion": respuesta_exacta["descripcion"].iloc[0]
        }
    
    # Si no hay coincidencia exacta, usar el modelo
    entrada_vec = vectorizer.transform([entrada.respuesta_usuario])
    carrera_predicha = model.predict(entrada_vec)[0]
   
    # Buscar la descripción de la carrera predicha
    descripcion = data[data["carrera_sugerida"] == carrera_predicha]["descripcion"].iloc[0]
    area = data[data["carrera_sugerida"] == carrera_predicha]["area"].iloc[0]
   
    return {
        "carrera_sugerida": carrera_predicha,
        "area": area,
        "descripcion": descripcion
    }

# 6. Ruta para obtener preguntas disponibles
@app.get("/preguntas/")
def obtener_preguntas():
    preguntas_unicas = data["pregunta"].unique().tolist()
    return {"preguntas": preguntas_unicas}

# 7. Ruta de bienvenida
@app.get("/")
def bienvenida():
    return {
        "mensaje": "¡Hola! Soy un chatbot básico para ayudarte a encontrar tu carrera ideal.",
        "instrucciones": "Usa /preguntas/ para ver las preguntas disponibles y /sugerir_carrera/ para obtener sugerencias.",
        "version": "1.0.0",
        "endpoints": {
            "preguntas": "/preguntas/",
            "sugerir_carrera": "/sugerir_carrera/",
            "documentacion": "/docs"
        }
    }

# 8. Health check para Render
@app.get("/health")
def health_check():
    return {"status": "OK", "message": "Chatbot funcionando correctamente"}
