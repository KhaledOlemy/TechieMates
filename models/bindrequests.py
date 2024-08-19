#!/usr/bin/python3
"""Bind Request Class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class BindRequest(BaseModel, Base):
    """Bind Request Class"""
    __tablename__ = "bindrequests"
    from_user = Column(String(60), ForeignKey("users.id"), nullable=False)
    to_user = Column(String(60), ForeignKey("users.id"), nullable=False)
