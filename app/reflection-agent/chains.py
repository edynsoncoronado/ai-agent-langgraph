"""
Este módulo define los prompts y cadenas de LangChain utilizadas para generar y evaluar publicaciones de LinkedIn mediante un proceso iterativo de reflexión.
Incluye la cadena para generar publicaciones, la cadena para evaluar publicaciones y la cadena para generar nuevas ideas basadas en la evaluación.
Estas cadenas se utilizan en el agente de reflexión para mejorar continuamente la calidad de las publicaciones generadas.
"""

# 1. IMPORTACIONES
# Importamos ChatPrompTemplate para crear las plantillas de prompts estructuradas
# y MessagesPlaceholder para insertar el historial de mensajes en las cadenas de prompts.
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Importamos el modelo de lenguaje de Ollama para ejecutar las cadenas en local. Asegúrate de tener Ollama instalado y configurado.
from langchain_ollama import ChatOllama

# Cargamos la configuración desde settings.py, que incluye los parámetros para conectar con Ollama
from settings import settings

# 2. PLANTILLAS DE PROMPT
# Plantilla de prompt para la fase de generación: el modelo crea o mejora publicaciones
generation_prompt = ChatPromptTemplate.from_messages(
    [
        # Mensaje de sistema: define al modelo como asistente que escribe publicaciones
        (
            "system",
            "Eres un asistente de influencer tecnológico de LinkedIn encargado de escribir excelentes publicaciones. "
            "Genera la mejor publicación posible según la petición del usuario. "
            "Si el usuario aporta crítica, responde con una versión revisada de tus intentos anteriores.",
        ),
        # Marcador para el historial de mensajes
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Plantilla de prompt para la fase de reflexión: el modelo actúa como evaluador
# y genera crítica y recomendaciones sobre la publicación del usuario
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        # Mensaje de sistema: define el rol y comportamiento del modelo
        (
            "system",
            "Eres un influencer viral de LinkedIn que evalúa publicaciones. Genera crítica y recomendaciones para la publicación del usuario. "
            "Siempre proporciona recomendaciones detalladas, incluyendo aspectos como longitud, viralidad, estilo, etc.",
        ),
        # Marcador que se reemplaza por el historial de mensajes de la conversación
        # (petición del usuario, borradores previos, críticas, etc.)
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# 3. CREACIÓN DE CADENAS
# Instancia del modelo de lenguaje (usa configuración por defecto, típicamente desde .env)
print(f"---->settings.ollama_model: {settings.ollama_model}")
llm = ChatOllama(
    model=settings.ollama_model,
    base_url=settings.ollama_base_url,
    # api_key=settings.ollama_api_key,             # cualquier string
    temperature=settings.ollama_temperature
)
# llm = ChatOllama(model="gpt-oss:20b")  # Asegúrate de haber ejecutado antes en cmd: ollama pull gpt-oss:20b o cualquier otro modelo que tengas instalado

#  Cadena para generar publicaciones de LinkedIn utilizando la plantilla de generación
generate_chain = generation_prompt | llm

# Cadena para evaluar publicaciones de LinkedIn utilizando la plantilla de reflexión
reflect_chain = reflection_prompt | llm