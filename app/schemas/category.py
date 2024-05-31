from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None

class ResponseCategory(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
