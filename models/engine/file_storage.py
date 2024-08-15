#!/usr/bin/python3
"""File Storage Class to handle storage"""
import json
import models
from models.base_model import BaseModel
from models.user import User
from models.message import Message
from models.roadmap import Roadmap
from models.course import Course
from models.vendor import Vendor
from models.chapter import Chapter
from models.progress import Progress


class FileStorage():
    """File Storage Class to handle storage"""
    __file_path = "TechieMateFS.json"
    __objects = {}

    def all(self, cls=None):
        if cls:
            out_dict = {}
            for key, val in FileStorage.__objects.items():
                if f"{cls}." in key:
                    out_dict[key] = val
            return out_dict
        else:
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

    def delete(self, obj=None):
        if obj:
            search_key = f"{obj.to_dict()['__class__']}.{obj.to_dict()['id']}"
            if search_key in FileStorage.__objects:
                del (FileStorage.__objects[search_key])
                self.save

    def close(self):
        """
        calls reload for deserializing the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        if not cls or not id:
            return None
        instances = self.all(cls)
        desired_instance = None
        for _, instance in instances.items():
            if instance.id == id:
                desired_instance = instance
                break
        return desired_instance

    def count(self, cls=None):
        if cls:
            return len(models.storage.all(cls))
        else:
            return len(models.storage.all())
