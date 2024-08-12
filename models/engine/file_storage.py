#!/usr/bin/python3
"""File Storage Class to handle storage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.message import Message
from models.roadmap import Roadmap
from models.course import Course
from models.vendor import Vendor


class FileStorage():
    """File Storage Class to handle storage"""
    __file_path = "TechieMateFS.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        out_dict = {}
        for key, val in self.__objects.items():
            out_dict[key] = val.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(out_dict, f)

    def reload(self):
        try:
            with open(self.__file_path, "r") as f:
                objects = json.load(f)
                for val in objects.values():
                    class_name = val['__class__']
                    del val['__class__']
                    self.new(eval(class_name)(**val))
        except FileNotFoundError:
            return
