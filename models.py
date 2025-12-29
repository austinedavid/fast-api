from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Create a user model
class UserSchema(BaseModel):
    email: EmailStr
    user_name: str = Field(max_length=30, min_length=3)
    married: Optional[bool] = None


class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    married: Optional[bool] = None
