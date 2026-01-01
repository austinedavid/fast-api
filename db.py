from sqlalchemy import create_engine, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    sessionmaker,
    DeclarativeBase,
    Session,
    relationship,
)
from typing import Generator, List
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID, uuid4

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

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    user_name: Mapped[str] = mapped_column(String)
    married: Mapped[bool] = mapped_column(Boolean)
    profile: Mapped["Profile"] = relationship(
        back_populates="user", cascade="all, delete-orphan", uselist=False
    )
    posts: Mapped[List["Posts"]] = relationship(back_populates="user", uselist=True)


# the user profile below
# for one to one relationship
class Profile(Base):
    __tablename__ = "Profile"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    state: Mapped[str] = mapped_column(String)
    lga: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    userid: Mapped[str] = mapped_column(ForeignKey("Users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="profile")


class Posts(Base):
    __tablename__ = "Posts"
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    userId: Mapped[str] = mapped_column(ForeignKey("Users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
