from models import PostModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from db import Posts, engine, get_db
from fastapi import APIRouter, Body, HTTPException, Depends
from typing import Annotated

router = APIRouter(prefix="/post", tags=["posts session"])


# here we created a post
@router.post("/")
async def make_post(
    payload: Annotated[PostModel, Body(title="user creates a post here")],
):

    try:
        with Session(engine) as session:
            post = Posts(**payload.model_dump())
            session.add(post)
            session.commit()
            session.refresh(post)
        return "post was created successfully"
    except Exception as error:
        print(error)
        raise HTTPException(
            400, detail="something went wrong handling the post creationm"
        )


# here, we handle get all the post created so far
@router.get("/")
async def get_all_post(db: Session = Depends(get_db)):
    try:
        all_post = db.query(Posts).all()
        return all_post
    except Exception as error:
        print(error)
        raise HTTPException(501, detail="this is not working well as expected")
