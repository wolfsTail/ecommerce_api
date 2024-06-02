from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None\
    

class ResponseCategory(BaseModel):
    id: int
    name: str
    slug: str
    

class UpdateCategory(BaseModel):
    id: int
    name: str
    is_active: bool
    parent_id: int | None = None
