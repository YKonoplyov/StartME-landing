from typing import List
from sqlalchemy import ForeignKey, String, Integer, Table, Column
from sqlalchemy.orm import mapped_column, Mapped, relationship

from fastapi_users.db import SQLAlchemyBaseUserTable
from db.engine import Base


users_in_founds = Table(
    "users_founds",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("founds_id", ForeignKey("founds.id"), primary_key=True),
)

managers_in_founds = Table(
    "managers_founds",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("founds_id", ForeignKey("founds.id"), primary_key=True),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    nickname: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String())
    first_name: Mapped[str] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    by_fathers_name: Mapped[str] = mapped_column(String())
    contact_fields: Mapped[str] = mapped_column(String())
    address: Mapped[str] = mapped_column(String())

    founds: Mapped[List["Found"]] = relationship(
        secondary=users_in_founds,
        back_populates="users",
    )
    managers_founds: Mapped[List["Found"]] = relationship(
        secondary=managers_in_founds,
        back_populates="users",
    )


class Found(Base):
    __tablename__ = "founds"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    discord: Mapped[str] = mapped_column(String())
    link: Mapped[str] = mapped_column(String())

    users: Mapped[List["User"]] = relationship(
        secondary=users_in_founds,
        back_populates="founds",
    )
    managers: Mapped[List["User"]] = relationship(
        secondary=managers_in_founds,
        back_populates="founds",
    )

class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    found_id: Mapped[int] = mapped_column(ForeignKey("founds.id"))