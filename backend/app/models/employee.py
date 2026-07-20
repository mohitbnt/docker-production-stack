"""Employee model."""
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel


class Employee(BaseModel):
    __tablename__ = "employees"

    first_name = Column(String(120), nullable=False)
    last_name = Column(String(120), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    position = Column(String(120), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)

    department = relationship("Department", back_populates="employees")
    assets = relationship("Asset", back_populates="assigned_to", foreign_keys="Asset.assigned_to_id")

    def to_dict(self, include_department: bool = True):
        d = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "position": self.position,
            "department_id": self.department_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_department and self.department is not None:
            d["department"] = {"id": self.department.id, "code": self.department.code, "name": self.department.name}
        else:
            d["department"] = None
        return d
