from datetime import datetime

from sqlalchemy import Integer, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.backend.db import Base


class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    comment: Mapped[str] = mapped_column(Text)
    comment_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id'))

    rating = relationship("Rating", back_populates="review", uselist=False, lazy='select')