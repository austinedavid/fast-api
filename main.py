from fastapi import FastAPI
from routes.users import users
from db import Base, engine


app = FastAPI(
    title="The first python app",
    description="this app will handle working with best programs",
)

# create all the table immediately
Base.metadata.create_all(bind=engine)


app.include_router(users.router)


@app.get("/", tags=["home"])
async def default_home():
    return "Hello world"
