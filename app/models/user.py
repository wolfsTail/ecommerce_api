from app.backend.db import Base
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    username: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(64))
    hashed_password: Mapped[str] = mapped_column(String(64))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_suplier: Mapped[bool] = mapped_column(Boolean, default=False)
    is_customer: Mapped[bool] = mapped_column(Boolean, default=True)
    