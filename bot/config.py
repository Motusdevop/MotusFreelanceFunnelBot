import logging

from aiogram.enums import ParseMode
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from aiogram.client.default import DefaultBotProperties


class Settings(BaseSettings):
    token: SecretStr
    admins: list[int]

    development_form_url: str
    training_form_url: str
    feedback_form_url: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

default_bot_properties = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
