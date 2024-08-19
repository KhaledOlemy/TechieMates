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
from models.contact_us import ContactUs
from models.bindrequests import BindRequest
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
            classes = [Roadmap, User, Message, Course, Vendor, Chapter, Progress, ContactUs, BindRequest]
        for class_name in classes:
            class_instances = self.__session.query(class_name).order_by(class_name.updated_at)
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


    def get_user_by_email(self, email):
        """gets user details by email"""
        if not email:
            return None
        instances = models.storage.all(User)
        desired_instance = None
        for _, instance in instances.items():
            if instance.email == email:
                desired_instance = instance
                break
        return desired_instance
    
    def get_user_progress(self, user_id, filterc=0):
        """gets user's progress details by user_id and filterc"""
        if not user_id:
            return None
        if filterc == 0:
            users_progress = self.__session.query(Progress).filter_by(user_id=user_id).filter_by(completed_roadmap=0).first()
        else:
            users_progress = self.__session.query(Progress).filter_by(user_id=user_id).filter_by(completed_roadmap=1).all()
            print(users_progress)
        return users_progress

    def get_roadmap_courses(self, roadmap_id):
        """gets roadmap cources by roadmap_id"""
        if not roadmap_id:
            return None
        courses_in_roadmap = self.__session.query(Course).filter_by(roadmap_id=roadmap_id).order_by(Course.order_in_roadmap).all()
        return courses_in_roadmap
    
    def get_available_partners(self, roadmap_id):
        """gets available partners by roadmap_id"""
        if not roadmap_id:
            return None
        available_partners = self.__session.query(User).filter_by(roadmap_id=roadmap_id).filter_by(partner_id=None).all()
        return available_partners

    def get_active_course_by_roadmap_and_order(self, roadmap_id=None, order=1):
        """gets active course by roadmap_id and order"""
        if not roadmap_id:
            return None
        active_course = self.__session.query(Course).filter_by(roadmap_id=roadmap_id).filter_by(order_in_roadmap=order).first()
        return active_course
    
    def get_active_chapter_by_course_and_order(self, course_id=None, order=1):
        """gets active chapter by course_id and order"""
        if not course_id:
            return None
        active_chapter = self.__session.query(Chapter).filter_by(course_id=course_id).filter_by(order_in_course=order).first()
        return active_chapter

    def get_course_order(self, course_id=None):
        """gets course order in the roadmap by course_id"""
        if not course_id:
            return None
        order = self.__session.query(Course).filter_by(course_id=course_id).first().to_dict()["order_in_roadmap"]
        return order

    def get_chapter_order(self, chapter_id=None):
        """gets chapter order in the course"""
        if not chapter_id:
            return None
        order = self.__session.query(Chapter).filter_by(chapter_id=chapter_id).first().to_dict()["order_in_course"]
        return order

    def get_course_chapters(self, course_id=None):
        """gets chapters of a course by course_id"""
        if not course_id:
            return None
        chapters = self.__session.query(Chapter).filter_by(course_id=course_id).order_by(Chapter.order_in_course).all()
        return chapters

    def get_course_vendors(self, course_id=None):
        """gets course vendors by course_id"""
        if not course_id:
            return None
        vendors = self.__session.query(Vendor).filter_by(course_id=course_id).order_by(Vendor.cost).all()
        return vendors

    def get_user_last_messages(self, user_id=None):
        """gets user's last messages by user_id"""
        if not user_id:
            return None
        messages = models.storage.all(Message).values()
        messages = [msg.to_dict() for msg in messages if (msg.to_dict()['from_user'] == user_id or msg.to_dict()['to_user'] == user_id) and not msg.to_dict()['to_roadmap']]
        last_messages = {}
        for msg in messages:
            from_user = msg['from_user']
            to_user = msg['to_user']
            other_user = from_user if from_user != user_id else to_user
            other_user_name = models.storage.get(User, other_user).to_dict()
            other_user_photo = other_user_name["photo"]
            other_user_name = other_user_name['first_name'] + ' ' + other_user_name['last_name']
            text = msg['text']
            time = msg['updated_at']
            
            from datetime import datetime
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            day_with_suffix = str(time.day)
            if 4 <= time.day <= 20 or 24 <= time.day <= 30:
                day_with_suffix += "th"
            else:
                day_with_suffix += ["st", "nd", "rd"][time.day % 10 - 1]
            time = time.strftime(f"%I:%M%p {day_with_suffix} %B")
            # time = time.strftime("%I:%M%p %d %B")
            if from_user == user_id:
                sender_same_user = True
            else:
                sender_same_user = False
            out_dict = {
                "other_user_name": other_user_name,
                "last_message_sent": text,
                "time": time,
                "other_user_id": other_user,
                "sender_same_user": sender_same_user,
                "other_user_photo": other_user_photo
            }
            last_messages[other_user] = out_dict
        last_messages = sorted(list(last_messages.values()), key=lambda x: x["time"])
        return last_messages

    def get_single_messaging(self, our_user, other_user):
        """gets user's messages between one user and another"""
        messages = models.storage.all(Message).values()
        messages = [msg.to_dict() for msg in messages]
        messages = [msg for msg in messages if (msg["from_user"] == our_user and msg["to_user"] == other_user) or (msg["to_user"] == our_user and msg["from_user"] == other_user)]
        for msg in messages:
            if msg["from_user"] == our_user:
                msg["sender_same_user"] = True
            else:
                msg["sender_same_user"] = False
        return messages

    def get_community_messaging(self, our_user, to_roadmap):
        """gets messages inside a roadmap community messages"""
        messages = models.storage.all(Message).values()
        messages = [msg.to_dict() for msg in messages]
        messages = [msg for msg in messages if msg["to_roadmap"] == to_roadmap]
        for msg in messages:
            if msg["from_user"] == our_user:
                msg["sender_same_user"] = True
            else:
                msg["sender_same_user"] = False
            sender = models.storage.get(User, msg['from_user']).to_dict()
            photo = sender["photo"]
            msg['sender'] = sender['first_name'] + ' ' + sender['last_name']
            msg['photo'] = photo
        return messages
    
    def get_sent_requests(self, user_id):
        """gets sent binding requests"""
        if not user_id:
            return None
        sent_requests = self.__session.query(BindRequest).filter_by(from_user=user_id).all()
        return sent_requests
    
    def get_received_requests(self, user_id):
        """gets received binding requests"""
        if not user_id:
            return None
        received_requests = self.__session.query(BindRequest).filter_by(to_user=user_id).all()
        return received_requests
