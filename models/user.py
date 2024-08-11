#!/usr/bin/python3
"""User Class"""
from models.base_model import BaseModel


class User(BaseModel):
    """User Class"""
    first_name = ""
    last_name = ""
    password = ""
    email = ""
    phone = ""
    active_roadmap = ""
    partner_id = ""
