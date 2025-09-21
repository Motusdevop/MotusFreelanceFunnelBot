import sys
from typing import List

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from loguru import logger

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Настройка логирования
logger.remove()

# Логи в консоль
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "{name}:{function}:{line} - {message}",
    level="INFO",
)

# Логи в файл (ротация каждый день, хранение 7 дней)
logger.add("logs/bot.log", rotation="1 day", retention="7 days", encoding="utf-8")


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    ADMINS: List[int]

    # Google Forms
    DEVELOPMENT_FORM_URL: str
    TRAINING_FORM_URL: str
    FEEDBACK_FORM_URL: str

    # Google Sheets
    CREDENTIALS_PATH: str
    SHEET_NAME: str

    # worksheets
    REVIEWS_WORKSHEET: str
    USERS_WORKSHEET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()

default_bot_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
