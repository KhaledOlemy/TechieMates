#!/usr/bin/python3
"""User Class"""
from models.base_model import BaseModel, Base
import models.message
from models.roadmap import Roadmap
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
# from models.message import Message
import models


class User(BaseModel, Base):
    """User Class"""
    __tablename__ = "users"
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True) # unique added
    phone = Column(String(256), nullable=True)
    roadmap_id = Column(String(60), ForeignKey("roadmaps.id"), nullable=True)
    partner_id = Column(String(60), ForeignKey("users.id"), nullable=True)
    partners = relationship("User")
    messages = relationship("Message", cascade="all,delete,delete-orphan", foreign_keys="[Message.to_user]")
    messages2 = relationship("Message", cascade="all,delete,delete-orphan", foreign_keys="[Message.from_user]")
    progresses = relationship("Progress", cascade="all,delete,delete-orphan", backref="user")
