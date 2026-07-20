"""Base model mixin providing common columns."""
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer

from ..extensions import db


def _utcnow():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False)


class BaseModel(db.Model, TimestampMixin):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
