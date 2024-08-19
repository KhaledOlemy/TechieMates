#!/usr/bin/python3
"""Message Class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """Message Class"""
    __tablename__ = "messages"
    from_user = Column(String(60), ForeignKey("users.id"), nullable=False)
    to_user = Column(String(60), ForeignKey("users.id"), nullable=True)
    to_roadmap = Column(String(60), ForeignKey("roadmaps.id"), nullable=True)
    text = Column(String(4096), nullable=False)
