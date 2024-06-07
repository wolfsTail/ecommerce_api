from pydantic import BaseModel, Field


class InnerRating(BaseModel):
    value: float = Field(
        ge=0, le=5, description="Max 2 decomal places"
    )