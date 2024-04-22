from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.backend.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(32))
    slug: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column(Integer)
    image_url: Mapped[str] = mapped_column(String)
    stock: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=True)
    category: Mapped["Category"] = relationship("Category", back_populates="products")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    print(CreateTable(Product.__table__))