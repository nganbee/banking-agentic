from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://gsvhu-34-147-68-150.run.pinggy-free.link"
    
    # Models
    GENERATION_MODEL: str = "gpt-oss:20b" 
    FINETUNED_MODEL: str = "banking-intent"
    
    # Finetuned intent model
    INTENT_MODEL_PATH: str = "imbee510/bank-intent-qwen-unsloth"

    # Project Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # App Settings
    APP_NAME: str = "Banking Agentic"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        
settings = Settings()