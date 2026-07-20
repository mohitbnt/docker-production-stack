"""User (authentication) model."""
import bcrypt
from sqlalchemy import Column, String, Boolean

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False, default="")
    role = Column(String(50), nullable=False, default="admin")
    is_active = Column(Boolean, nullable=False, default=True)

    def set_password(self, raw: str) -> None:
        self.password_hash = bcrypt.hashpw(raw.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")

    def check_password(self, raw: str) -> bool:
        try:
            return bcrypt.checkpw(raw.encode("utf-8"), self.password_hash.encode("utf-8"))
        except Exception:
            return False

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
