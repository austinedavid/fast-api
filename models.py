from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Create a user model
class UserSchema(BaseModel):
    email: EmailStr
    user_name: str = Field(max_length=30, min_length=3)
    married: Optional[bool] = None
    password: str = Field(max_length=10)


class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    married: Optional[bool] = None


# creating pydantic model for the profile
class ProfileModel(BaseModel):
    state: str
    lga: str
    age: int = Field(ge=18)
    userid: str


class PostModel(BaseModel):
    title: str = Field(min_length=10, max_length=50)
    description: str = Field(min_length=10, max_length=300)
    userId: str


class UserLogin(BaseModel):
    email: str
    password: str
