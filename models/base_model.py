#!/usr/bin/python3
"""BaseModel Class for others to build on"""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel():
    """BaseModel Class"""
    ISO_format = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, val in kwargs.items():
                if key != "__class__":
                    if key in ["created_at", "updated_at"]:
                        self.__dict__[key] = datetime.strptime(val,
                                                               self.ISO_format)
                    else:
                        self.__dict__[key] = val
        else:
            models.storage.new(self)

    def __str__(self):
        out_str = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return out_str

    def save(self):
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        out_dict = self.__dict__.copy()
        out_dict['created_at'] = self.created_at.isoformat()
        out_dict['updated_at'] = self.updated_at.isoformat()
        out_dict['__class__'] = self.__class__.__name__
        return out_dict
