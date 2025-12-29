from sqlalchemy import create_engine, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase, Session
from typing import Generator
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.dialects.postgresql import UUID

# first lets create our engine
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

sessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# here we create all the neccessary tables needed
# together with the base class
class Base(DeclarativeBase):
    pass


# the user table
class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_name: Mapped[str] = mapped_column(String)
    married: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self) -> str:
        return "the users was created successfully"
