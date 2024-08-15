#!/usr/bin/python3
"""Course Class"""
from models.base_model import BaseModel, Base
from models.roadmap import Roadmap
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Course(BaseModel, Base):
    """Course Class"""
    __tablename__ = "courses"
    title = Column(String(256), nullable=False)
    description = Column(String(4096), nullable=False)
    roadmap_id = Column(String(60), ForeignKey("roadmaps.id"), nullable=False)
    order_in_roadmap = Column(Integer, nullable=False) #unique w roadmap_id added
    __table_args__ = (UniqueConstraint('order_in_roadmap', 'roadmap_id', name='course_roadmap_id_order_unique'), )
    vendors = relationship("Vendor", cascade="all,delete,delete-orphan", backref="course")
    chapters = relationship("Chapter", cascade="all,delete,delete-orphan", backref="course")
    progresses = relationship("Progress", cascade="all,delete,delete-orphan", backref="course")
