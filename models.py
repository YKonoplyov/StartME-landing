import json
from enum import Enum as PythonEnum
from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, String, Integer, Table, Column, JSON, Enum, DateTime, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable

from db.engine import Base

class Roles(PythonEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    READ_ONLY = "read_only"

users_in_founds = Table(
    "users_founds",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("founds_id", ForeignKey("founds.id"), primary_key=True),
)

managers_in_founds = Table(
    "managers_founds",
    Base.metadata,
    Column("manager_id", ForeignKey("users.id"), primary_key=True),
    Column("founds_id", ForeignKey("founds.id"), primary_key=True),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    by_fathers_name: Mapped[str] = mapped_column(String(64), nullable=True)
    contact_fields: Mapped[dict] = mapped_column(JSON(none_as_null=True), nullable=True)
    nicknames: Mapped[dict] = mapped_column(JSON(none_as_null=True), nullable=True)
    gipsy_team: Mapped[str] = mapped_column(String(256), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    role: Mapped[str] = mapped_column(Enum(Roles))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")
    
    founds: Mapped[List["Found"]] = relationship(
        secondary=users_in_founds,
        back_populates="users"
    )
    managed_founds: Mapped[List["Found"]] = relationship(
        secondary=managers_in_founds,
        back_populates="managers"
    )


class Found(Base):
    __tablename__ = "founds"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    discord: Mapped[str] = mapped_column(String(), nullable=True)
    link: Mapped[str] = mapped_column(String())

    users: Mapped[List["User"]] = relationship(
        secondary=users_in_founds,
        back_populates="founds"
    )
    managers: Mapped[List["User"]] = relationship(
        secondary=managers_in_founds,
        back_populates="managed_founds"
    )

class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship()
    found_id: Mapped[int] = mapped_column(ForeignKey("founds.id"))
    found: Mapped["Found"] =  relationship()
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    arbitrage: Mapped[str] = mapped_column(String(64), nullable=True)
    comment: Mapped[str] = mapped_column(Text(), nullable=True)
    previous_versions: Mapped[List["RecordHistory"]] = relationship()

class RecordHistory(Base):
    __tablename__ = "records_history"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User")
    found_id: Mapped[int] = mapped_column(ForeignKey("founds.id"))
    found: Mapped["Found"] = relationship("Found")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    arbitrage: Mapped[str] = mapped_column(String(64), nullable=True)
    comment: Mapped[str] = mapped_column(Text(), nullable=False)
    current_version: Mapped[int] = mapped_column(ForeignKey("records.id"))
