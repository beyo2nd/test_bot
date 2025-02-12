from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

# Здесь загружаются переменные окружения из .env ( бот токен )

class Settings(BaseSettings):
    bot_token: SecretStr
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

config = Settings()