from fastapi import APIRouter, Body, Depends, HTTPException, status
from models import UserSchema, UserLogin
from typing import Annotated
from db import get_db
from sqlalchemy.orm import Session
from db import User
from .user_service import (
    create_new_user,
    get_all_the_user,
    get_based_on_username_and_marriage,
    get_user_by_id,
)
from models import UpdateUser
from middlewares.middlewares import (
    get_auth_token,
    limit_present,
    CommonBuyQuries,
    CommonInput,
    path_operator_decorator,
    PathFunc,
)
from utils.password import verify_password
from jose import jwt, JWTError
import os
from datetime import datetime, timedelta


# create the Apirouter function
router = APIRouter(prefix="/user", tags=["User info"])


# default endpoint to create a user below
@router.post("/")
async def make_user(
    payload: Annotated[
        UserSchema, Body(description="users basic information for creating a new user")
    ],
    db: Session = Depends(get_db),
):
    try:
        return await create_new_user(payload, db)
    except Exception as e:

        raise HTTPException(404, f" message: {e}")


@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    try:
        return get_all_the_user(db)
    except Exception as e:
        raise HTTPException(404, detail={"message": f"message: {e}"})


# @router.get("/{username}")
# async def get_single_user(username: str, db: Session = Depends(get_db)):
#     try:
#         return get_based_on_username_and_marriage(db, username)
#     except Exception as e:
#         raise HTTPException(400, f"message: {e}")


@router.put("/{id}")
async def update_user(
    id: int,
    payload: Annotated[UpdateUser, Body(description="the user info to update")],
    db: Session = Depends(get_db),
):
    try:
        # get the single user first
        previous_user_info = get_user_by_id(db, id)
        # then check all the fields and update neccessary part
        if payload.user_name is not None:
            previous_user_info.user_name = payload.user_name
        if payload.married is not None:
            previous_user_info.married = payload.married
        # commit the change now
        db.commit()
        db.refresh(previous_user_info)
        return previous_user_info
    except Exception as e:
        return HTTPException(500, f"message: {e}")


@router.delete("/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        # get the user based on the id
        user_info = get_user_by_id(db, id)
        if not user_info:
            return "there is no user"
        db.delete(user_info)
        db.commit()
        return f"{user_info.user_name} is deleted successfully!!!"
    except Exception as e:
        return HTTPException(505, f"message: {e}")


@router.get("/middle-ware")
async def check_dependency(
    common: Annotated[CommonBuyQuries, Depends(CommonBuyQuries)],
):
    return common


@router.post(
    "/common-user/{id}",
    dependencies=[Depends(path_operator_decorator), Depends(PathFunc)],
)
async def common_users(id: str, payload: Annotated[dict, Depends(CommonInput)]):
    print(payload)
    return payload


# here we login a user
@router.post("/login")
async def login_user(
    payload: Annotated[UserLogin, Body()], db: Session = Depends(get_db)
):
    # get the user and check if it actually exists
    user_info = db.query(User).filter(User.email == payload.email).first()
    print(user_info)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # check if the password matches now
    if not verify_password(payload.password, user_info.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # now we move ahead and perform creation of jwt
    expires = datetime.utcnow() + timedelta(minutes=30)
    print(expires)
    token = jwt.encode(
        {"username": user_info.user_name, "email": user_info.email, "exp": expires},
        os.getenv("JWT_SECRETE"),
        os.getenv("JWT_ALGO"),
    )
    return {"token": token, "type": "Bearer"}
