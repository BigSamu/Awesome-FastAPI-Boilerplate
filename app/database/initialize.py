
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.base import Base
from app.database.session import SessionLocal, engine
from app import models, schemas, crud
from app.core import settings

def create_tables() -> None:
    """
    Create database tables from SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)

def create_admin_user(db: Session):
    # Try to create the admin user

    admin_user_in = schemas.UserCreate(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        password=settings.ADMIN_PASSWORD,
        role="admin"
    )
    # Check if the user already exists
    user = db.query(models.User).filter(models.User.username == admin_user_in.username).first()
    if not user:
        crud.user.create(db, obj_in=admin_user_in)

def init_database():
    # This is the function called from main.py to initialize the whole database
    # Create a new database session
    db = SessionLocal()

    # Create tables
    create_tables()

    # Initialize default values
    create_admin_user(db)

    # Close the session
    db.close()
