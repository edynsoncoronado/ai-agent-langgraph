from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración del modelo de lenguaje Ollama
    ollama_model: str
    ollama_base_url: str
    ollama_api_key: str = "ollama"  # Puedes usar cualquier string como api_key para Ollama
    ollama_temperature: float = 0.7

    class Config:
        env_file = ".env"  # Archivo de entorno para cargar las variables

settings = Settings()