from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.core import verify_password, hash_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation methods.

    def get_one_by_username(self, db: Session, username: str) -> Optional[User]:
        print(username)
        return db.query(User).filter(User.username == username).first()

    def get_one_by_email(self, db: Session, email: str) -> Optional[User]:
        print(email)
        return db.query(User).filter(User.email == email).first()

    # Overriding create method for hashing password of user
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["password"] = hash_password(obj_in_data["password"])
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Overriding update method for hashing password of user
    def update(self, db: Session, *, db_obj: User, obj_in: UserUpdate) -> User:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if field == "password":
                    setattr(db_obj, field, hash_password(update_data[field]))
                else:
                    setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # Override remove all method to avoid deleting admin user
    def remove_all(self, db: Session) -> int:
        rows_deleted = db.query(self.model).filter(self.model.username != "admin").delete()
        db.commit()
        return rows_deleted

    #  Creating authentication method
    def authenticate(
        self, db: Session, *, username: str, password: str
    ) -> Optional[User]:
        user = self.get_one_by_username(db, username=username)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user = CRUDUser(User)
