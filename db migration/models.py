from enum import Enum as PythonEnum
from typing import Any, List, Optional
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Table,
    Column,
    JSON,
    Enum,
    DateTime,
    Text,
    Boolean
)
from sqlalchemy.orm import mapped_column, Mapped, relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
import json
from engine import Base


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
    login: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(256), nullable=True)
    discord: Mapped[str] = mapped_column(String(256), nullable=True)
    role: Mapped[str] = mapped_column(Enum(Roles))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )
    founds: Mapped[List["Found"]] = relationship(
        secondary=users_in_founds, back_populates="users"
    )
    managed_founds: Mapped[List["Found"]] = relationship(
        secondary=managers_in_founds, back_populates="managers"
    )
    old_id: Mapped[str] = mapped_column(String(), nullable=True)


class Found(Base):
    __tablename__ = "founds"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=True)
    discord: Mapped[str] = mapped_column(String(), nullable=True)
    link: Mapped[str] = mapped_column(String(), nullable=True)
    users: Mapped[List["User"]] = relationship(
        secondary=users_in_founds, back_populates="founds"
    )
    managers: Mapped[List["User"]] = relationship(
        secondary=managers_in_founds, back_populates="managed_founds"
    )
    owner: Mapped[User] = relationship()
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    old_id: Mapped[str] = mapped_column(String(), nullable=True)


class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    middlname: Mapped[str] = mapped_column(String(64), nullable=True)
    nicknames: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON(none_as_null=True), nullable=True)
    gipsyteam: Mapped[str] = mapped_column(Text(), nullable=True)
    pokerstrategy: Mapped[str] = mapped_column(Text(), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    amount: Mapped[str] = mapped_column(Text(), nullable=True)
    google: Mapped[str] = mapped_column(Text(), nullable=True)
    mail: Mapped[str] = mapped_column(Text(), nullable=True)
    vk: Mapped[str] = mapped_column(Text(), nullable=True)
    facebook: Mapped[str] = mapped_column(Text(), nullable=True)
    blog: Mapped[str] = mapped_column(Text(), nullable=True)
    instagram: Mapped[str] = mapped_column(Text(), nullable=True)
    forum: Mapped[str] = mapped_column(Text(), nullable=True)
    neteller: Mapped[str] = mapped_column(Text(), nullable=True)
    skrill: Mapped[str] = mapped_column(Text(), nullable=True)
    ecopayz: Mapped[str] = mapped_column(Text(), nullable=True)
    old: Mapped[bool] = mapped_column(Boolean(), default=False)
    fundName: Mapped[str] = mapped_column(Text(), nullable=True)
    nicknameOld: Mapped[str] = mapped_column(Text(), nullable=True)
    comments: Mapped[str] = mapped_column(Text(), nullable=True)
    country: Mapped[str] = mapped_column(Text(), nullable=True)
    town: Mapped[str] = mapped_column(Text(), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by: Mapped["User"] = relationship()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    webmoney_id: Mapped[str] = mapped_column(Text(), nullable=True)
    wallets: Mapped[str] = mapped_column(Text(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    previous_versions: Mapped[List["RecordHistory"]] = relationship()
    old_id: Mapped[str] = mapped_column(String(), nullable=True)

class RecordHistory(Base):
    __tablename__ = "records_history"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True)
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    middlname: Mapped[str] = mapped_column(String(64), nullable=True)
    nicknames: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON(none_as_null=True), nullable=True)
    gipsyteam: Mapped[str] = mapped_column(Text(), nullable=True)
    pokerstrategy: Mapped[str] = mapped_column(Text(), nullable=True)
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    amount: Mapped[str] = mapped_column(Text(), nullable=True)
    google: Mapped[str] = mapped_column(Text(), nullable=True)
    mail: Mapped[str] = mapped_column(Text(), nullable=True)
    vk: Mapped[str] = mapped_column(Text(), nullable=True)
    facebook: Mapped[str] = mapped_column(Text(), nullable=True)
    blog: Mapped[str] = mapped_column(Text(), nullable=True)
    instagram: Mapped[str] = mapped_column(Text(), nullable=True)
    forum: Mapped[str] = mapped_column(Text(), nullable=True)
    neteller: Mapped[str] = mapped_column(Text(), nullable=True)
    skrill: Mapped[str] = mapped_column(Text(), nullable=True)
    ecopayz: Mapped[str] = mapped_column(Text(), nullable=True)
    old: Mapped[bool] = mapped_column(Boolean(), default=False)
    fundName: Mapped[str] = mapped_column(Text(), nullable=True)
    nicknameOld: Mapped[str] = mapped_column(Text(), nullable=True)
    comments: Mapped[str] = mapped_column(Text(), nullable=True)
    country: Mapped[str] = mapped_column(Text(), nullable=True)
    town: Mapped[str] = mapped_column(Text(), nullable=True)
    address: Mapped[str] = mapped_column(Text(), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_by: Mapped["User"] = relationship()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now()
    )
    webmoney_id: Mapped[str] = mapped_column(Text(), nullable=True)
    wallets: Mapped[str] = mapped_column(Text(), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    current_version: Mapped[int] = mapped_column(ForeignKey("records.id"))
    old_id: Mapped[str] = mapped_column(String(), nullable=True)