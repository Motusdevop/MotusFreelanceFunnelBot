from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    chat_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    last_activity: datetime
    command: str
    callback_data: str | None


class Review(BaseModel):
    date: datetime
    name: str
    service: str
    grade: int
    review: str
    additionally: str | None
