#!/usr/bin/python3
"""Vendor Class"""
from models.base_model import BaseModel, Base
from models.course import Course
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Chapter(BaseModel, Base):
    """Chapter Class"""
    __tablename__ = "chapters"
    title = Column(String(256), nullable=False)
    course_id = Column(String(60), ForeignKey("courses.id"), nullable=False)
    order_in_course = Column(Integer, nullable=False) #unique w course_id added
    __table_args__ = (UniqueConstraint('course_id', 'order_in_course', name='chapter_course_id_order_unique'),)
    progresses = relationship("Progress", cascade="all,delete,delete-orphan", backref="chapter")
