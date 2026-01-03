from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# function to hash the password
def hash_password(plain_password: str) -> str:
    hashed_password = password_context.hash(plain_password)
    return hashed_password


# verify your password
def verify_password(plain_password, hashed_password) -> bool:
    is_verified = password_context.verify(plain_password, hashed_password)
    return is_verified
