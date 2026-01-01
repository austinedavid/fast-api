from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routes.users import users
from routes.profile import init as profile
from routes.post import init as post
from db import Base, engine


app = FastAPI(
    title="The first python app",
    description="this app will handle working with best programs",
)

# create all the table immediately
# and also handle database connection too
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(profile.router)
app.include_router(post.router)


@app.get("/", tags=["home"])
async def default_home():
    return "Hello world"
