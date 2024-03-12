"""Модуль констант проекта."""

from pydantic_settings import BaseSettings

# Глобальные настройки логгера
BACKUP_COUNT = 5
ENCODING = "UTF-8"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
LOGGING_LEVEL = "INFO"
LOGS_FOLDER = "logs"
LOGS_FILE = "logfile.log"
MAX_BYTES = 50_000_000

# URL API серверра WB
URL_API_WB = (
    "https://card.wb.ru/cards/v1/detail?"
    "appType=1&curr=rub&dest=-1257786&spp=30&nm={}"
)


# Загрузка секретов из .env
class Settings(BaseSettings):
    database_url: str
    bot_token: str


settings = Settings()
