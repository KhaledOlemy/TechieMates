#!/usr/bin/python3
"""Course Class"""
from models.base_model import BaseModel


class Course(BaseModel):
    """Course Class"""
    title = ""
    short_description = ""
    long_description = ""
    roadmap_id = ""
    order_in_roadmap = 0
