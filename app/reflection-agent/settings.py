from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Configuración para cargar variables de entorno desde el archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    # Configuración del modelo de lenguaje Ollama
    ollama_model: str
    ollama_base_url: str
    ollama_api_key: str = "ollama"  # Puedes usar cualquier string como api_key para Ollama
    ollama_temperature: float = 0.7

    # Configuración de LangSmith para trazabilidad
    langsmith_endpoint: str
    langsmith_api_key: str
    langsmith_tracing: bool = True
    langsmith_project: str = "Agente Reflexivo"

settings = Settings()