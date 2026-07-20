"""Department model."""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    employees = relationship("Employee", back_populates="department", passive_deletes=False)

    def to_dict(self, include_count: bool = True):
        d = {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_count:
            d["employee_count"] = len(self.employees) if self.employees is not None else 0
        return d
