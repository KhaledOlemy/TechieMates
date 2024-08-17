from api.v1.views import app_views
from flask import jsonify, url_for
from models.base_model import BaseModel
from models.roadmap import Roadmap
from models.course import Course
from models.chapter import Chapter
from models.user import User
from models.message import Message
from models.progress import Progress
from models.vendor import Vendor
from models import storage



@app_views.route("/status", strict_slashes=False)
def status_function():
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats_function():
    classes = [Roadmap, Course, Chapter, User, Message, Progress, Vendor]
    out_dict = {}
    for classname in classes:
        out_dict[classname.__tablename__] = storage.count(classname)
    return jsonify(out_dict)

@app_views.route("getit")
def getit():
    iwant = [i.to_dict() for i in storage.all(Message).values()]
    return jsonify(iwant)

@app_views.route('/page1')
def page1():
    # Generate absolute URL for 'page2' route
    page2_url = url_for('app_views.page2', _external=True, id="byeeeeeeeeee")
    return f'The absolute URL for page2 is: {page2_url}'

@app_views.route('/page3/<id>')
def page2(id="hi"):
    return f'This is page 333333 {id}'