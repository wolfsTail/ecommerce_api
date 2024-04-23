from sqlalchemy import Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.backend.db import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    value: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))
    review_id: Mapped[int] = mapped_column(Integer, ForeignKey('reviews.id'))
    
    review = relationship("Review", back_populates="rating", lazy='select')