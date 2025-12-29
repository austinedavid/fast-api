from sqlalchemy.orm import Session
from models import UserSchema, UpdateUser
from db import User


def get_user_by_id(db: Session, id: int):
    single_user = db.query(User).filter(User.id == id).first()
    return single_user


async def create_new_user(user_info: UserSchema, db: Session):
    user_json = user_info.model_dump()
    new_user = User(**user_json)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_all_the_user(db: Session):
    all_user = db.query(User).all()
    return all_user


def get_based_on_username_and_marriage(db: Session, user_name):
    result = (
        db.query(User)
        .filter(User.user_name == user_name)
        .filter(User.married == True)
        .all()
    )
    return result


def update_the_user_infos(db: Session, payload: UpdateUser):
    user_update_info = payload.model_dump()
