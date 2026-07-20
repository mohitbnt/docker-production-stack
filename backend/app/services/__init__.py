"""Service layer."""
import logging
from datetime import datetime, timezone
from typing import Optional
from flask import current_app
from sqlalchemy import func

from ..extensions import db
from ..models import User, Department, Employee, Asset, AssetStatus
from ..repositories import UserRepo, DepartmentRepo, EmployeeRepo, AssetRepo
from ..cache import cache
from ..errors import NotFoundError, ConflictError, UnauthorizedError

logger = logging.getLogger(__name__)

DASHBOARD_CACHE_KEY = "opsportal:dashboard:stats"


class AuthService:
    @staticmethod
    def authenticate(email: str, password: str) -> User:
        user = UserRepo.by_email(email)
        if not user or not user.is_active or not user.check_password(password):
            raise UnauthorizedError("Invalid email or password")
        return user


class DepartmentService:
    @staticmethod
    def list_all():
        return DepartmentRepo.all()

    @staticmethod
    def get(did: int) -> Department:
        d = DepartmentRepo.by_id(did)
        if not d:
            raise NotFoundError("Department not found")
        return d

    @staticmethod
    def create(data: dict) -> Department:
        if DepartmentRepo.by_code(data["code"]):
            raise ConflictError("Department code already exists")
        d = Department(**data)
        db.session.add(d)
        db.session.commit()
        DashboardService.invalidate()
        return d

    @staticmethod
    def update(did: int, data: dict) -> Department:
        d = DepartmentService.get(did)
        if "code" in data and data["code"].lower() != d.code.lower():
            if DepartmentRepo.by_code(data["code"]):
                raise ConflictError("Department code already exists")
        for k, v in data.items():
            setattr(d, k, v)
        db.session.commit()
        DashboardService.invalidate()
        return d

    @staticmethod
    def delete(did: int) -> None:
        d = DepartmentService.get(did)
        if d.employees:
            raise ConflictError("Cannot delete a department that has employees")
        db.session.delete(d)
        db.session.commit()
        DashboardService.invalidate()


class EmployeeService:
    @staticmethod
    def search(q: Optional[str] = None):
        return EmployeeRepo.search(q)

    @staticmethod
    def get(eid: int) -> Employee:
        e = EmployeeRepo.by_id(eid)
        if not e:
            raise NotFoundError("Employee not found")
        return e

    @staticmethod
    def create(data: dict) -> Employee:
        if EmployeeRepo.by_email(data["email"]):
            raise ConflictError("Employee email already exists")
        if data.get("department_id"):
            DepartmentService.get(data["department_id"])
        e = Employee(**data)
        db.session.add(e)
        db.session.commit()
        DashboardService.invalidate()
        return e

    @staticmethod
    def update(eid: int, data: dict) -> Employee:
        e = EmployeeService.get(eid)
        if "email" in data and data["email"].lower() != e.email.lower():
            if EmployeeRepo.by_email(data["email"]):
                raise ConflictError("Employee email already exists")
        if data.get("department_id"):
            DepartmentService.get(data["department_id"])
        for k, v in data.items():
            setattr(e, k, v)
        db.session.commit()
        DashboardService.invalidate()
        return e

    @staticmethod
    def delete(eid: int) -> None:
        e = EmployeeService.get(eid)
        db.session.delete(e)
        db.session.commit()
        DashboardService.invalidate()


class AssetService:
    @staticmethod
    def list_all():
        return AssetRepo.all()

    @staticmethod
    def get(aid: int) -> Asset:
        a = AssetRepo.by_id(aid)
        if not a:
            raise NotFoundError("Asset not found")
        return a

    @staticmethod
    def create(data: dict) -> Asset:
        if AssetRepo.by_tag(data["tag"]):
            raise ConflictError("Asset tag already exists")
        if data.get("assigned_to_id"):
            EmployeeService.get(data["assigned_to_id"])
        a = Asset(**data)
        db.session.add(a)
        db.session.commit()
        DashboardService.invalidate()
        return a

    @staticmethod
    def update(aid: int, data: dict) -> Asset:
        a = AssetService.get(aid)
        if "tag" in data and data["tag"].lower() != a.tag.lower():
            if AssetRepo.by_tag(data["tag"]):
                raise ConflictError("Asset tag already exists")
        if data.get("assigned_to_id"):
            EmployeeService.get(data["assigned_to_id"])
        for k, v in data.items():
            setattr(a, k, v)
        db.session.commit()
        DashboardService.invalidate()
        return a

    @staticmethod
    def delete(aid: int) -> None:
        a = AssetService.get(aid)
        db.session.delete(a)
        db.session.commit()
        DashboardService.invalidate()


class DashboardService:
    @staticmethod
    def stats() -> dict:
        cached = cache.get(DASHBOARD_CACHE_KEY)
        if cached:
            cached["cached"] = True
            return cached

        total_employees = db.session.query(func.count(Employee.id)).scalar() or 0
        total_departments = db.session.query(func.count(Department.id)).scalar() or 0
        total_assets = db.session.query(func.count(Asset.id)).scalar() or 0

        payload = {
            "total_employees": int(total_employees),
            "total_departments": int(total_departments),
            "total_assets": int(total_assets),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "cached": False,
        }
        ttl = current_app.config.get("REDIS_CACHE_TTL_SECONDS", 60)
        cache.set(DASHBOARD_CACHE_KEY, payload, ttl=ttl)
        return payload

    @staticmethod
    def invalidate() -> None:
        cache.delete(DASHBOARD_CACHE_KEY)


class ProfileService:
    @staticmethod
    def update(user: User, data: dict) -> User:
        if data.get("name") is not None:
            user.name = data["name"]
        if data.get("password"):
            user.set_password(data["password"])
        db.session.commit()
        return user
