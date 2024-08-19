#!/usr/bin/python3
"""Message Class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class ContactUs(BaseModel, Base):
    """Contact Us Class"""
    __tablename__ = "contactus"
    name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False)
    message = Column(String(4096), nullable=False)
