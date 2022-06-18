from pydantic import BaseModel


class Vocabulary(BaseModel):
    text_a: str = ""
    text_b: str = ""


class User(BaseModel):
    id: str  # noqa
