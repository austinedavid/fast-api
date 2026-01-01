from fastapi.requests import Request
from typing import Callable, Awaitable, Annotated
from fastapi.responses import Response
from fastapi import Query, HTTPException, Header, Path
from models import UserSchema


# universal middleware for all the endpoint
async def first_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
):
    response = await call_next(request)
    return response


# middleware to check for authentication
async def get_auth_token(
    authorization: Annotated[
        str | None, Header(description="the header authorization is needed")
    ] = None,
) -> str:

    if not authorization:
        raise HTTPException(status_code=405, detail="no authorization code provided")
    return authorization


async def limit_present(
    limit: Annotated[
        int | None, Query(description="the users filter informationm")
    ] = None,
) -> int:
    if not limit or limit == 0:
        raise HTTPException(status_code=400, detail="limit should be present")
    return limit


class CommonBuyQuries:
    def __init__(
        self,
        q: int | None = None,
        limit: int | None = None,
        skip: int | None = None,
        authorization: Annotated[str | None, Header()] = None,
    ):
        self.q = q
        self.limit = limit
        self.skip = skip


class CommonInput:
    def __init__(self, payload: UserSchema):
        body = payload.model_dump()
        body.update({"extra": "mesoma with extra names"})
        self.payload = body


async def path_operator_decorator(
    limit: Annotated[int | None, Query(title="something about path operators")] = None,
):
    if not limit or limit < 20:
        raise HTTPException(404, detail="please enter a valid limit here")


class PathFunc:
    def __init__(self, id: Annotated[str, Path(title="path information here")]):
        if int(id) < 20:
            raise HTTPException(404, detail="something went wrong here")
