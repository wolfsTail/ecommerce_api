from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None

class ResponseCategory(CreateCategory):
    id: int
