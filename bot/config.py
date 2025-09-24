from typing import List
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    Uses Pydantic for validation and type safety.
    """

    # Bot
    BOT_TOKEN: SecretStr
    ADMINS: List[int]

    # AutoUpdate
    UPLOAD_DELAY_MINUTS: int
    LOAD_DELAY_MINUTS: int

    # Google Forms URLs
    DEVELOPMENT_FORM_URL: str
    TRAINING_FORM_URL: str
    FEEDBACK_FORM_URL: str

    # Google Sheets
    CREDENTIALS_PATH: str
    SHEET_NAME: str

    # Worksheets
    REVIEWS_WORKSHEET: str
    USERS_WORKSHEET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()


def get_default_bot_properties() -> DefaultBotProperties:
    """
    Returns default bot properties for Aiogram.
    Currently sets the default parse mode to MARKDOWN.
    """
    return DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
