from datetime import datetime, timezone

from typing import List, Set

from sqlalchemy import DateTime, Column, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(36), unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password: Mapped[str] = mapped_column(String(254))
    
    current_chat_id = mapped_column(ForeignKey("chatlogs.id"))
    current_chat: Mapped["ChatLog"] = relationship(back_populates="connected_users")
    
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
    
class ChatLog(db.Model):
    __tablename__ = "chatlogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(36))
    date_created = Column(DateTime, default=datetime.now(timezone.utc))
    
    connected_users: Mapped[Set["User"]] = relationship(back_populates="current_chat")
    messages: Mapped[List["Message"]] = relationship(back_populates="chatlog")

class Message(db.Model):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_sent = Column(DateTime, default=datetime.now(timezone.utc))
    body: Mapped[str] = mapped_column(String(1000))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="messages")

    chatlog_id: Mapped[int] = mapped_column(ForeignKey("chatlogs.id"))
    chatlog: Mapped["ChatLog"] = relationship(back_populates="messages")
    
