from fastapi import APIRouter, Depends, Body, HTTPException
from models import ProfileModel
from db import get_db, Profile, User, Posts
from sqlalchemy.orm import Session, selectinload
from typing import Annotated


router = APIRouter(prefix="/profile", tags=["profile"])


# starting creating endpoint
# for creating a post
@router.post("/")
async def make_profile(
    payload: Annotated[ProfileModel, Body(title="user profile creation")],
    db: Session = Depends(get_db),
):
    try:
        gotten_user = payload.model_dump()
        profile = Profile(**gotten_user)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return "profile created successfully"
    except Exception as error:
        raise HTTPException(405, detail=error)


# get all the profiles
@router.get("/")
async def get_all_profile(db: Session = Depends(get_db)):
    try:
        profiles = (
            db.query(Profile)
            .options(
                selectinload(Profile.user)
                .load_only(User.id, User.email)
                .selectinload(User.posts)
                .load_only(Posts.id, Posts.title)
            )
            .all()
        )
        return profiles
    except Exception as error:
        raise HTTPException(500, detail=error)
