"""Repository layer: data access helpers."""
from typing import Optional, List
from sqlalchemy import or_, func

from ..extensions import db
from ..models import User, Department, Employee, Asset


class UserRepo:
    @staticmethod
    def by_email(email: str) -> Optional[User]:
        return User.query.filter(func.lower(User.email) == email.lower()).first()

    @staticmethod
    def by_id(uid: int) -> Optional[User]:
        return db.session.get(User, uid)


class DepartmentRepo:
    @staticmethod
    def all() -> List[Department]:
        return Department.query.order_by(Department.name.asc()).all()

    @staticmethod
    def by_id(did: int) -> Optional[Department]:
        return db.session.get(Department, did)

    @staticmethod
    def by_code(code: str) -> Optional[Department]:
        return Department.query.filter(func.lower(Department.code) == code.lower()).first()


class EmployeeRepo:
    @staticmethod
    def search(q: Optional[str] = None) -> List[Employee]:
        query = Employee.query
        if q:
            like = f"%{q.lower()}%"
            query = query.filter(or_(
                func.lower(Employee.first_name).like(like),
                func.lower(Employee.last_name).like(like),
                func.lower(Employee.email).like(like),
                func.lower(Employee.position).like(like),
            ))
        return query.order_by(Employee.last_name.asc(), Employee.first_name.asc()).all()

    @staticmethod
    def by_id(eid: int) -> Optional[Employee]:
        return db.session.get(Employee, eid)

    @staticmethod
    def by_email(email: str) -> Optional[Employee]:
        return Employee.query.filter(func.lower(Employee.email) == email.lower()).first()


class AssetRepo:
    @staticmethod
    def all() -> List[Asset]:
        return Asset.query.order_by(Asset.tag.asc()).all()

    @staticmethod
    def by_id(aid: int) -> Optional[Asset]:
        return db.session.get(Asset, aid)

    @staticmethod
    def by_tag(tag: str) -> Optional[Asset]:
        return Asset.query.filter(func.lower(Asset.tag) == tag.lower()).first()
