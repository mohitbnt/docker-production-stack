"""Asset model."""
import enum
from sqlalchemy import Column, String, ForeignKey, Integer, Date, Enum as SAEnum
from sqlalchemy.orm import relationship

from .base import BaseModel


class AssetStatus(str, enum.Enum):
    available = "available"
    assigned = "assigned"
    in_repair = "in_repair"
    retired = "retired"


class Asset(BaseModel):
    __tablename__ = "assets"

    tag = Column(String(80), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(120), nullable=True)
    status = Column(SAEnum(AssetStatus, name="asset_status"), nullable=False, default=AssetStatus.available)
    assigned_to_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
    purchased_at = Column(Date, nullable=True)

    assigned_to = relationship("Employee", back_populates="assets", foreign_keys=[assigned_to_id])

    def to_dict(self, include_assignee: bool = True):
        d = {
            "id": self.id,
            "tag": self.tag,
            "name": self.name,
            "category": self.category,
            "status": self.status.value if isinstance(self.status, AssetStatus) else self.status,
            "assigned_to_id": self.assigned_to_id,
            "purchased_at": self.purchased_at.isoformat() if self.purchased_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_assignee and self.assigned_to is not None:
            d["assigned_to"] = {
                "id": self.assigned_to.id,
                "first_name": self.assigned_to.first_name,
                "last_name": self.assigned_to.last_name,
                "email": self.assigned_to.email,
            }
        else:
            d["assigned_to"] = None
        return d
