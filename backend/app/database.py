from sqlalchemy import create_engine

DATABASE_URL = (
    "postgresql://ipl_admin:ipl_password_2026@ipl-postgres:5432/ipl_warehouse"
)

engine = create_engine(DATABASE_URL)