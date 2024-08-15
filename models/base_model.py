#!/usr/bin/python3
"""BaseModel Class for others to build on"""
from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import mapped_column

Base = declarative_base()


class BaseModel():
    """BaseModel Class"""
    ISO_format = "%Y-%m-%dT%H:%M:%S.%f"
    """
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    updated_at = Column(DateTime, nullable=False, default=(datetime.utcnow()))
    """
    id = mapped_column(String(60), unique=True, nullable=False, primary_key=True, sort_order=-3)
    created_at = mapped_column(DateTime, nullable=False, default=(datetime.utcnow()), sort_order=-2)
    updated_at = mapped_column(DateTime, nullable=False, default=(datetime.utcnow()), sort_order=-1)
    def __init__(self, *args, **kwargs):
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], self.ISO_format)
            else:
                kwargs['updated_at'] = datetime.now()
            self.updated_at = kwargs['updated_at']
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], self.ISO_format)
            else:
                kwargs['created_at'] = datetime.now()
            self.created_at = kwargs['created_at']
            if 'id' not in kwargs:
                self.id = str(uuid4())
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        out_str = f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
        return out_str

    def save(self):
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        out_dict = self.__dict__.copy()
        out_dict['created_at'] = self.created_at.isoformat()
        out_dict['updated_at'] = self.updated_at.isoformat()
        out_dict['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in out_dict:
            del out_dict['_sa_instance_state']
        return out_dict

    def delete(self):
        models.storage.delete(self)
