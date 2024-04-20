from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.backend.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped["Category"] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")