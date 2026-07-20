"""Standalone seed script. Run with `python -m app.seed` inside the backend venv."""
import logging
import os
from datetime import date

from . import create_app
from .extensions import db
from .models import User, Department, Employee, Asset, AssetStatus

logger = logging.getLogger(__name__)


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        # Seed admin user
        admin_email = app.config["SEED_ADMIN_EMAIL"]
        admin = User.query.filter(User.email == admin_email).first()
        if not admin:
            admin = User(email=admin_email, name=app.config["SEED_ADMIN_NAME"], role="admin", is_active=True)
            admin.set_password(app.config["SEED_ADMIN_PASSWORD"])
            db.session.add(admin)
            print(f"[seed] created admin user: {admin_email}")
        else:
            print(f"[seed] admin user already exists: {admin_email}")

        # Departments
        dept_data = [
            ("ENG", "Engineering", "Software engineering department"),
            ("HR", "Human Resources", "People operations"),
            ("FIN", "Finance", "Finance and accounting"),
            ("OPS", "Operations", "Business operations"),
        ]
        depts = {}
        for code, name, desc in dept_data:
            d = Department.query.filter(Department.code == code).first()
            if not d:
                d = Department(code=code, name=name, description=desc)
                db.session.add(d)
                print(f"[seed] created department: {code}")
            depts[code] = d
        db.session.flush()

        # Employees
        emp_data = [
            ("Alice", "Anderson", "alice@opsportal.local", "+1-555-1001", "Senior Engineer", "ENG"),
            ("Bob", "Brown", "bob@opsportal.local", "+1-555-1002", "DevOps Engineer", "ENG"),
            ("Carol", "Clark", "carol@opsportal.local", "+1-555-1003", "HR Manager", "HR"),
            ("David", "Davis", "david@opsportal.local", "+1-555-1004", "Accountant", "FIN"),
            ("Eve", "Evans", "eve@opsportal.local", "+1-555-1005", "Operations Lead", "OPS"),
        ]
        emps = {}
        for fn, ln, email, phone, pos, dcode in emp_data:
            e = Employee.query.filter(Employee.email == email).first()
            if not e:
                e = Employee(first_name=fn, last_name=ln, email=email, phone=phone,
                             position=pos, department_id=depts[dcode].id)
                db.session.add(e)
                print(f"[seed] created employee: {email}")
            emps[email] = e
        db.session.flush()

        # Assets
        asset_data = [
            ("LT-0001", "MacBook Pro 16\"", "Laptop", AssetStatus.assigned, "alice@opsportal.local", date(2024, 3, 15)),
            ("LT-0002", "Dell XPS 15", "Laptop", AssetStatus.assigned, "bob@opsportal.local", date(2024, 4, 20)),
            ("MN-0001", "LG UltraFine 27\"", "Monitor", AssetStatus.assigned, "alice@opsportal.local", date(2024, 3, 15)),
            ("KB-0001", "Logitech MX Keys", "Peripheral", AssetStatus.available, None, date(2024, 1, 10)),
            ("PH-0001", "iPhone 15", "Phone", AssetStatus.assigned, "carol@opsportal.local", date(2024, 6, 1)),
            ("SV-0001", "Dell PowerEdge R750", "Server", AssetStatus.in_repair, None, date(2023, 11, 12)),
        ]
        for tag, name, cat, status, owner_email, purchased in asset_data:
            a = Asset.query.filter(Asset.tag == tag).first()
            if not a:
                a = Asset(tag=tag, name=name, category=cat, status=status,
                          assigned_to_id=emps[owner_email].id if owner_email else None,
                          purchased_at=purchased)
                db.session.add(a)
                print(f"[seed] created asset: {tag}")

        db.session.commit()
        print("[seed] done.")


if __name__ == "__main__":
    seed()
