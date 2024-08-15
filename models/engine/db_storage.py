#!/usr/bin/python3
"""DB storage"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
import models
from models.roadmap import Roadmap
from models.user import User
from models.message import Message
from models.course import Course
from models.vendor import Vendor
from models.chapter import Chapter
from models.progress import Progress


class DBStorage:
    """This class manages storage of hbnb models in db storage format"""
    __engine = None
    __session = None
    """
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    """
    def __init__(self):
        """
        init db storage
        """
        user = os.getenv('TM_MYSQL_USER')
        pswd = os.getenv('TM_MYSQL_PWD')
        host = os.getenv('TM_MYSQL_HOST')
        db = os.getenv('TM_MYSQL_DB')
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(user, pswd, host, db),
                                      pool_pre_ping=True)
        if os.getenv('TM_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        return all instances /or/ cls instances
        """
        out_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            classes = [cls]
        else:
            classes = [Roadmap, User, Message, Course, Vendor, Chapter, Progress]
        for class_name in classes:
            class_instances = self.__session.query(class_name)
            for ins in class_instances:
                out_dict["{}.{}".format(type(ins).__name__, ins.id)] = ins
        return out_dict

    def new(self, obj):
        """
        create new obj
        """
        self.__session.add(obj)

    def save(self):
        """
        save and commit to db
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete obj of db
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        reload objs from db
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """calls remove func"""
        self.__session.close()

    def get(self, cls, id):
        """returns an instance of a class"""
        if not cls or not id:
            return None
        instances = models.storage.all(cls)
        desired_instance = None
        for _, instance in instances.items():
            if instance.id == id:
                desired_instance = instance
                break
        return desired_instance

    def count(self, cls=None):
        """counts the number of objects in storage"""
        if cls:
            return len(models.storage.all(cls))
        else:
            return len(models.storage.all())
