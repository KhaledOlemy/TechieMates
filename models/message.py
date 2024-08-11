#!/usr/bin/python3
"""Message Class"""
from models.base_model import BaseModel


class Message(BaseModel):
    """Message Class"""
    from_user = ""
    to_user = ""
    text = ""
