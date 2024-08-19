#!/usr/bin/python3
"""Vendor Class"""
from models.base_model import BaseModel, Base
from models.user import User
from models.roadmap import Roadmap
from models.course import Course
from models.chapter import Chapter
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint, BOOLEAN
from sqlalchemy.orm import relationship


class Progress(BaseModel, Base):
    """Progress Class"""
    __tablename__ = "progresses"
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    roadmap_id = Column(String(60), ForeignKey("roadmaps.id"), nullable=False)
    course_id = Column(String(60), ForeignKey("courses.id"), nullable=False)
    chapter_id = Column(String(60), ForeignKey("chapters.id"), nullable=False)
    completed_roadmap = Column(Integer, nullable=False, default=0)
    __table_args__ = (UniqueConstraint('user_id', 'roadmap_id', name='progress_user_id_roadmap_id_unique'),)
