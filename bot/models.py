from pydantic import BaseModel, Field


class User(BaseModel):
    chat_id: int
    first_name: str | None
    last_name: str | None
    username: str | None
    last_activity: str