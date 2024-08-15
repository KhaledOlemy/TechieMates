#!/usr/bin/python3
"""Vendor Class"""
from models.base_model import BaseModel, Base
from models.course import Course
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Vendor(BaseModel, Base):
    """Vendor Class"""
    __tablename__ = "vendors"
    name = Column(String(256), nullable=False)
    link = Column(String(4096), nullable=False)
    cost = Column(Integer, nullable=False)
    course_id = Column(String(60), ForeignKey("courses.id"), nullable=False)
