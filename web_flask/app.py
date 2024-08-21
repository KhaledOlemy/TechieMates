from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
api_host = getenv("TM_API_HOST", "0.0.0.0")
api_port = getenv("TM_API_PORT", "5000")
CORS(app, resources={"/*": {"origins": api_host}})
app.secret_key = getenv("SECRET_KEY")

@app.teardown_appcontext
def tear_down(exc):
    """Close the storage session at the end of the request."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by rendering a custom 404 page."""
    # return make_response(jsonify({'error': 'Not found'}), 404)
    return render_template("404.html", session=session)

##############################################################
from models.user import User
from models.roadmap import Roadmap
from models.course import Course
from models.chapter import Chapter
from models.message import Message
from models.progress import Progress
from models.vendor import Vendor
from models.contact_us import ContactUs
from models.bindrequests import BindRequest
from models import storage
from flask import request, render_template, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/login", methods=["GET", "POST"], strict_slashes=False)
def login():
    """Handle user login by checking credentials and managing session."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "you are already logged in"
        return redirect(url_for("get_current_user"))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        print(password)
        user = storage.get_user_by_email(email)
        if not user or not check_password_hash(user.to_dict()["password"], password):
            session["redirected"] = True
            session["error_message"] = "Invalid email/password combination. Please try again."
            return redirect(url_for('login'))
        session["error_message"] = None
        session["logged_in"] = True
        session["user_id"] = user.to_dict().get('id')
        session["user"] = user.to_dict()
        session["redirected"] = True
        session["success_message"] = "You successfully logged in"
        return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("login.html", session=session, success_message=success_message, error_message=error_message)

@app.route("/profile", methods=["GET"], strict_slashes=False)
def get_current_user():
    """Retrieve the profile information of the currently logged-in user."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for('login'))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    user = session["user"]
    data = {"user_name": user["first_name"] + " " + user["last_name"]}
    if user["roadmap_id"]:
        user_progress = storage.get_user_progress(user_id=user["id"])
        if user_progress:
            user_progress = user_progress.to_dict()
            current_roadmap = storage.get(Roadmap, user_progress["roadmap_id"]).to_dict()
            data["current_roadmap"] = current_roadmap["title"]
            roadmap_courses = storage.get_roadmap_courses(user_progress["roadmap_id"])
            current_course = storage.get(Course, user_progress["course_id"]).to_dict()
            data["current_course"] = current_course["title"]
            completed_courses = []
            for c in roadmap_courses[:int(current_course["order_in_roadmap"]) - 1]:
                completed_courses.append(c.to_dict()["title"])
            data["completed_courses"] = completed_courses
            if user["partner_id"]:
                partner = storage.get(User, user["partner_id"]).to_dict()
                partner_name = partner["first_name"] + " " + partner["last_name"]
                partner_link = url_for("get_another_user", user_id=partner['id'])
            else:
                partner_name = None
                partner_link = None
            data["partner_name"] = partner_name
            data["partner_link"] = partner_link
            user_name = user["first_name"] + " " + user["last_name"]
            data["user_name"] = user_name
    if storage.get_user_progress(user["id"], 1):
        completed_roadmaps = []
        roadmaps = storage.get_user_progress(user["id"], 1)
        for r in roadmaps:
            completed_roadmaps.append(storage.get(Roadmap, r.to_dict()["roadmap_id"]).to_dict()["title"])
    else:
        completed_roadmaps = None
    data["completed_roadmaps"] = completed_roadmaps
    data["photo"] = url_for("static", filename=f'images/{session["user"]["photo"]}', _external=True)
    return render_template("profile.html", data=data, session=session, message_link=None, error_message=error_message)

@app.route("/profile/<user_id>", methods=["GET"], strict_slashes=False)
def get_another_user(user_id):
    """Retrieve the profile information of another user."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for('login'))
    if not storage.get(User, user_id):
        session["redirected"] = True
        session["error_message"] = "Invalid user!"
        return redirect(url_for("get_current_user"))
    if session.get("user_id") == user_id:
        return redirect(url_for('get_current_user'))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    user = storage.get(User, user_id).to_dict()
    data = {"user_name": user["first_name"] + " " + user["last_name"]}
    if user["roadmap_id"]:
        user_progress = storage.get_user_progress(user_id=user["id"])
        if user_progress:
            user_progress = user_progress.to_dict()
            current_roadmap = storage.get(Roadmap, user_progress["roadmap_id"]).to_dict()
            data["current_roadmap"] = current_roadmap["title"]
            roadmap_courses = storage.get_roadmap_courses(user_progress["roadmap_id"])
            current_course = storage.get(Course, user_progress["course_id"]).to_dict()
            data["current_course"] = current_course["title"]
            completed_courses = []
            for c in roadmap_courses[:int(current_course["order_in_roadmap"]) - 1]:
                completed_courses.append(c.to_dict()["title"])
            data["completed_courses"] = completed_courses
            if user["partner_id"]:
                partner = storage.get(User, user["partner_id"]).to_dict()
                partner_name = partner["first_name"] + " " + partner["last_name"]
                partner_link = url_for("get_another_user", user_id=partner['id'])
            else:
                partner_name = None
                partner_link = None
            data["partner_name"] = partner_name
            data["partner_link"] = partner_link
            user_name = user["first_name"] + " " + user["last_name"]
            data["user_name"] = user_name
    if storage.get_user_progress(user["id"], 1):
        completed_roadmaps = []
        roadmaps = storage.get_user_progress(user["id"], 1)
        for r in roadmaps:
            completed_roadmaps.append(storage.get(Roadmap, r.to_dict()["roadmap_id"]).to_dict()["title"])
    else:
        completed_roadmaps = None
    f_user = storage.get(User, user_id).to_dict()
    s_user = storage.get(User, session["user_id"]).to_dict()
    if not f_user["partner_id"] and not s_user["partner_id"] and f_user["roadmap_id"] and f_user["roadmap_id"] == s_user["roadmap_id"]:
        bind_button = url_for("send_binding", roadmap_id=f_user["roadmap_id"], partner_id=user_id)
        unbind_button = None
    elif f_user["partner_id"] and f_user["partner_id"] == s_user["id"] and s_user["partner_id"] == f_user["id"]:
        unbind_button = url_for("unbind_partners", roadmap_id=f_user["roadmap_id"], partner_id=user_id)
        bind_button = None
    else:
        bind_button = None
        unbind_button = None
    data["bind_button"] = bind_button
    data["unbind_button"] = unbind_button
    data["completed_roadmaps"] = completed_roadmaps
    message_link = url_for("single_messaging", user_id=user_id, _external=True)
    user_photo = storage.get(User, user_id).to_dict()['photo']
    data["photo"] = url_for("static", filename=f'images/{user_photo}', _external=True)
    return render_template("profile.html", data=data, session=session, message_link=message_link)

@app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
def create_user():
    """Handle user signup by collecting user data and creating a new account."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    if session.get("logged_in"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
        session["redirected"] = True
        session["error_message"] = "You are already logged in!"
        return redirect(url_for("get_current_user"))
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        phone = request.form.get('phone')
        photo = request.form.get('photo')
        if not email:
            session["redirected"] = True
            session["error_message"] = "Email field is mandatory"
        if not first_name:
            session["redirected"] = True
            session["error_message"] = "First Name field is mandatory"
        if not last_name:
            session["redirected"] = True
            session["error_message"] = "Last Name field is mandatory"
        if not password:
            session["redirected"] = True
            session["error_message"] = "Password field is mandatory"
        else:
            session["redirected"] = False
            session["error_message"] = None
        exists = storage.get_user_by_email(email)
        if exists:
            session["redirected"] = True
            session["error_message"] = "Email already in use!"
            return redirect(url_for('create_user'))
        password = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(email=email, first_name=first_name, last_name=last_name, phone=phone, password=password, photo=photo) 
        new_user.save()
        storage.save()
        session["redirected"] = True
        session["success_message"] = "Account created successfully"
        return redirect(url_for("login"))
    elif request.method == "GET":
        profile_pics = [
            {"name": "Angry Eye", "loc": url_for("static", filename="images/angryeye.png")},
            {"name": "Cool Eye", "loc": url_for("static", filename="images/cooleye.png")},
            {"name": "Happy Eye", "loc": url_for("static", filename="images/happyeye.png")},
            {"name": "Hug Eye", "loc": url_for("static", filename="images/hugeye.png")},
            {"name": "Love Eye", "loc": url_for("static", filename="images/loveeye.png")},
            {"name": "Star Eye", "loc": url_for("static", filename="images/stareye.png")},
            {"name": "Thinking Eye", "loc": url_for("static", filename="images/thinkingeye.png")},
            {"name": "Wow Eye", "loc": url_for("static", filename="images/woweye.png")}
        ]
        return render_template("signup.html", session=session, error_message=error_message, profile_pics=profile_pics)

@app.route("/logout", methods=["GET"], strict_slashes=False)
def logout():
    """Log the user out and clear session data."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to view this content!"
        return redirect(url_for("login"))
    session["logged_in"] = False
    session["user_id"] = None
    session["user"] = None
    session["redirected"] = True
    session["success_message"] = "You logged out successfully!"
    return redirect(url_for("home"))

@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """Render the home page with appropriate session messages."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if session.get("user"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
    return render_template("home.html", session=session, success_message=success_message, error_message=error_message)

@app.route("/contact-us", methods=["GET", "POST"], strict_slashes=False)
def contact_us():
    """Handle contact us form submissions and display the contact us page."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if session.get("user"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        if not name or not email or not message.strip():
            session["redirected"] = True
            session["error_message"] = "You need to fill all fields in Contact Us form"
            return redirect(url_for("contact_us"))
        new_user = ContactUs(name=name, email=email, message=message)
        new_user.save()
        storage.save()
        send_message = "Your request has been filed successfully, and will be addressed ASAP. Thank you"
        session["redirected"] = True
        session["success_message"] = send_message
        return redirect(url_for("contact_us"))
    else:
        return render_template("contact-us.html", session=session, success_message=success_message, error_message=error_message)

@app.route("/about", methods=["GET"], strict_slashes=False)
def about():
    """Render the about page."""
    if session.get("user"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
    return render_template("about.html", session=session)

@app.route("/roadmaps", methods=["GET"], strict_slashes=False)
def get_all_roadmaps():
    """Retrieve and display all available roadmaps."""
    if session.get("user"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    all_roadmaps = [r.to_dict() for r in storage.all(Roadmap).values()]
    for r in all_roadmaps:
        r['link'] = url_for("get_single_roadmap", roadmap_id=r['id'], _external=True)
    return render_template("roadmaps.html", session=session, roadmaps=all_roadmaps, error_message=error_message)

@app.route("/roadmaps/<roadmap_id>", methods=["GET"], strict_slashes=False)
def get_single_roadmap(roadmap_id):
    """Retrieve and display the details of a single roadmap."""
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap! Please choose from here."
        return redirect(url_for("get_all_roadmaps"))
    if session.get("user"):
        session["user"] = storage.get(User, session["user_id"]).to_dict()
    other_roadmaps = [r.to_dict() for r in storage.all(Roadmap).values()]
    roadmap = storage.get(Roadmap, roadmap_id).to_dict()
    other_roadmaps.remove(roadmap)
    for r in other_roadmaps:
        r["link"] = url_for("get_single_roadmap", roadmap_id=r["id"], _external=True)
    courses = [c.to_dict() for c in storage.get_roadmap_courses(roadmap_id)]
    for c in courses:
        c['link'] = url_for("course_details", course_id=c['id'], _external=True)
    show_enroll_check = session.get("logged_in") and not session.get("user", {}).get("roadmap_id") and roadmap_id not in [r.to_dict()['roadmap_id'] for r in storage.get_user_progress(session["user_id"], 1)]
    return render_template("single_roadmap.html", session=session, roadmap=roadmap, other_roadmaps=other_roadmaps, courses=courses, show_enroll_check=show_enroll_check)

@app.route("/roadmaps/<roadmap_id>/enroll", methods=["GET"], strict_slashes=False)
def enroll_in_roadmap(roadmap_id):
    """Enroll the logged-in user in a selected roadmap."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for("login"))
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id"):
        passed = storage.get_user_progress(session["user_id"], 1)
        if not passed:
            session["redirected"] = True
            session["error_message"] = "You already have an active roadmap"
            return redirect(url_for("progress"))
    user = storage.get(User, session["user_id"])
    if storage.get_user_progress(session["user_id"], 1):
        passed = storage.get_user_progress(session["user_id"], 1)
        if passed:
            progress = storage.get_user_progress(session["user_id"], 1)
            setattr(user, "roadmap_id", None)
    setattr(user, "roadmap_id", roadmap_id)
    storage.save()
    user_id = session["user_id"]
    active_roadmap = storage.get(Roadmap, roadmap_id).to_dict()['id']
    active_course = storage.get_active_course_by_roadmap_and_order(roadmap_id).to_dict()['id']
    active_chapter = storage.get_active_chapter_by_course_and_order(active_course).to_dict()['id']
    new_progress = Progress(user_id=user_id, roadmap_id=active_roadmap, course_id=active_course, chapter_id=active_chapter, completed_roadmap=0)
    new_progress.save()
    storage.save()
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    session["redirected"] = True
    session["success_message"] = f"Successfully enrolled in {storage.get(Roadmap, roadmap_id).to_dict()['title']} Roadmap, please choose a partner to accompany eachother in your journey!"
    return redirect(url_for("get_roadmap_partners", roadmap_id=roadmap_id))

@app.route("/roadmaps/<roadmap_id>/partners", methods=["GET"], strict_slashes=False)
def get_roadmap_partners(roadmap_id):
    """Retrieve and display potential partners for the roadmap."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("partner_id", ""):
        session["redirected"] = True
        session["error_message"] = "One partner is enough"
        return redirect(url_for("progress"))
    if session.get("user", {}).get("roadmap_id", "") != roadmap_id:
        session["redirected"] = True
        session["error_message"] = "Wrong roadmap"
        return redirect(url_for("get_all_roadmaps"))
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    roadmap = storage.get(Roadmap, roadmap_id).to_dict()
    roadmap_title = roadmap["title"] + ": Available Partners"
    partners = [r.to_dict() for r in storage.get_available_partners(roadmap_id) if r.to_dict()['id'] != session.get('user')['id']]
    send_partners = []
    for p in partners:
        p['fullname'] = p['first_name'] + " " + p['last_name']
        p['link'] = url_for("get_another_user", user_id=p['id'], _external=True)
        p['button'] = url_for("send_binding", roadmap_id=roadmap_id, partner_id=p['id'])
        sent_earlier = storage.get_sent_requests(user_id=session["user_id"])
        if sent_earlier:
            sent_earlier = [i for i in sent_earlier if i.to_dict()['to_user'] == p['id']]
            if sent_earlier:
                continue
        send_partners.append(p)
    return render_template("partners.html", session=session, roadmap_title=roadmap_title, partners=send_partners, success_message=success_message, error_message=error_message)

@app.route("/roadmaps/<roadmap_id>/partners/<partner_id>/send-bind-request", methods=["GET", "POST"], strict_slashes=False)
def send_binding(roadmap_id, partner_id):
    """Send a binding request to another user to become partners in a roadmap."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id", "") != roadmap_id:
        session["redirected"] = True
        session["error_message"] = "Wrong roadmap"
        return redirect(url_for("get_all_roadmaps"))
    if session.get("user", {}).get("partner_id", ""):
        session["redirected"] = True
        session["error_message"] = "One partner is enough"
        return redirect(url_for("progress"))
    partner = storage.get(User, partner_id)
    if not partner:
        session["redirected"] = True
        session["error_message"] = "Invalid User!"
        return redirect(url_for("get_roadmap_partners", roadmap_id=roadmap_id))
    if partner.to_dict().get('partner_id'):
        session["redirected"] = True
        session["error_message"] = "Partner already binded"
        return redirect(url_for("get_roadmap_partners", roadmap_id=roadmap_id))
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    user = storage.get(User, session.get('user_id'))
    partner = storage.get(User, partner_id)
    sent_again = storage.get_sent_requests(user_id=session["user_id"])
    if sent_again:
        sent_again = [i for i in sent_again if i.to_dict()["to_user"] == partner_id]
        if sent_again:
            session["redirected"] = True
            session["error_message"] = "You have already sent to this user a binding request!!!"
            return redirect(url_for("binding_requests"))
    sent_earlier = storage.get_received_requests(user_id=session["user_id"])
    if sent_earlier:
        sent_earlier = [i for i in sent_earlier if i.to_dict()["from_user"] == partner_id]
        if sent_earlier:
            sender_sent_requests = storage.get_sent_requests(partner_id)
            sender_received_requests = storage.get_received_requests(partner_id)
            receiver_sent_requests = storage.get_sent_requests(session["user_id"])
            receiver_received_requests = storage.get_received_requests(session["user_id"])
            for g in [sender_sent_requests, sender_received_requests, receiver_sent_requests, receiver_received_requests]:
                for req in g:
                    storage.delete(req)
                    storage.save()
            storage.save()
            partner = storage.get(User, partner_id)
            user = storage.get(User, session["user_id"])
            setattr(user, "partner_id", partner.to_dict()["id"])
            setattr(partner, "partner_id", user.to_dict()["id"])
            user.save()
            partner.save()
            storage.save()
            partner_name = partner.to_dict()['first_name'].capitalize() + " " + partner.to_dict()['last_name'].capitalize()
            user_name = user.to_dict()['first_name'].capitalize() + " " + user.to_dict()['last_name'].capitalize()
            f_message = f"Successfully Binded with {partner_name}"
            s_message = f"Successfully Binded with {user_name}"
            msg_2 = Message(from_user=partner.to_dict()['id'], to_user=user.to_dict()['id'], text=s_message)
            msg_2.save()
            msg_1 = Message(from_user=user.to_dict()['id'], to_user=partner.to_dict()['id'], text=f_message)
            msg_1.save()
            storage.save()
            session["user"] = storage.get(User, session["user_id"]).to_dict()
            session["redirected"] = True
            session["success_message"] = f_message
            return redirect(url_for("progress"))
    new_binding_request = BindRequest(from_user=user.to_dict()["id"], to_user=partner.to_dict()["id"])
    new_binding_request.save()
    storage.save()
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    session["redirected"] = True
    session["success_message"] = "Bind Request sent!"
    return redirect(url_for("binding_requests"))

@app.route("/accept-bind-request/<partner_id>", methods=["POST"], strict_slashes=False)
def accept_binding(partner_id):
    """Accept a binding request from another user to become partners in a roadmap."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content"
        return redirect(url_for("login"))
    if not storage.get(User, partner_id):
        session["redirected"] = True
        session["error_message"] = "User doesn't exist"
        return redirect(url_for("binding_requests"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id", "") != storage.get(User, partner_id).to_dict()["roadmap_id"]:
        session["redirected"] = True
        session["error_message"] = "Wrong Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    if not storage.get(Roadmap, session["user"].get("roadmap_id")):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    if session.get("user", {}).get("partner_id", ""):
        session["redirected"] = True
        session["error_message"] = "One partner is enough!"
        return redirect(url_for("progress"))
    if storage.get(User, partner_id).to_dict()['partner_id']:
        session["redirected"] = True
        session["error_message"] = "User already has a partner!"
        return redirect(url_for("binding_requests"))
    
    target_request = storage.get_sent_requests(partner_id)
    target_request = [i.to_dict()["to_user"] for i in target_request]
    if session["user_id"] not in target_request:
        session["redirected"] = True
        session["error_message"] = "User didn't even send binding request! How did you reach there!"
        return redirect(url_for("binding_requests"))
    sender_sent_requests = storage.get_sent_requests(partner_id)
    sender_received_requests = storage.get_received_requests(partner_id)
    receiver_sent_requests = storage.get_sent_requests(session["user_id"])
    receiver_received_requests = storage.get_received_requests(session["user_id"])
    for g in [sender_sent_requests, sender_received_requests, receiver_sent_requests, receiver_received_requests]:
        for req in g:
            storage.delete(req)
            storage.save()
    storage.save()
    partner = storage.get(User, partner_id)
    user = storage.get(User, session["user_id"])
    setattr(user, "partner_id", partner.to_dict()["id"])
    setattr(partner, "partner_id", user.to_dict()["id"])
    user.save()
    partner.save()
    storage.save()
    partner_name = partner.to_dict()['first_name'].capitalize() + " " + partner.to_dict()['last_name'].capitalize()
    user_name = user.to_dict()['first_name'].capitalize() + " " + user.to_dict()['last_name'].capitalize()
    f_message = f"Successfully Binded with {partner_name}"
    s_message = f"Successfully Binded with {user_name}"
    msg_2 = Message(from_user=partner.to_dict()['id'], to_user=user.to_dict()['id'], text=s_message)
    msg_2.save()
    msg_1 = Message(from_user=user.to_dict()['id'], to_user=partner.to_dict()['id'], text=f_message)
    msg_1.save()
    storage.save()
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    session["redirected"] = True
    session["success_message"] = f_message
    return redirect(url_for("progress"))

@app.route("/retract-bind-request/<partner_id>", methods=["POST"], strict_slashes=False)
def retract_binding(partner_id):
    """Retract a sent binding request."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    if not storage.get(User, partner_id):
        session["redirected"] = True
        session["error_message"] = "User doesn't exist!"
        return redirect(url_for("binding_requests"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id", "") != storage.get(User, partner_id).to_dict()["roadmap_id"]:
        session["redirected"] = True
        session["error_message"] = "Wrong Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    if not storage.get(Roadmap, session["user"].get("roadmap_id")):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    if session.get("user", {}).get("partner_id", ""):
        session["redirected"] = True
        session["error_message"] = "One partner is enough!"
        return redirect(url_for("progress"))
    if storage.get(User, partner_id).to_dict()['partner_id']:
        session["redirected"] = True
        session["error_message"] = "User already has a partner!"
        return redirect(url_for("binding_requests"))
    target_request = storage.get_sent_requests(session["user_id"])
    target_request = [i.to_dict()["to_user"] for i in target_request]
    if partner_id not in target_request:
        session["redirected"] = True
        session["error_message"] = "You didn't send binding request!"
        return redirect(url_for("binding_requests"))
    target_request = storage.get_sent_requests(session["user_id"])
    target_request = [i for i in target_request if i.to_dict()["to_user"] == partner_id][0]
    storage.delete(target_request)
    storage.save()
    session["redirected"] = True
    session["success_message"] = "Successfully retracted bind request!"
    return redirect(url_for("binding_requests"))

@app.route("/roadmaps/<roadmap_id>/partners/<partner_id>/unbind", methods=["GET"], strict_slashes=False)
def unbind_partners(roadmap_id, partner_id):
    """Unbind the partners in a roadmap."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id", "") != roadmap_id:
        session["redirected"] = True
        session["error_message"] = "Wrong Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    if not session.get("user", {}).get("partner_id", ""):
        session["redirected"] = True
        session["error_message"] = "You already don't have a partner!"
        return redirect(url_for("progress"))
    partner = storage.get(User, partner_id)
    if not partner:
        session["redirected"] = True
        session["error_message"] = "Invalid user!"
        return redirect(url_for("home"))
    if not partner.to_dict().get('partner_id'):
        session["redirected"] = True
        session["error_message"] = "You aren't even binded!"
        return redirect(url_for("get_roadmap_partners", roadmap_id=roadmap_id))
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("get_all_roadmaps"))
    user = storage.get(User, session.get('user_id'))
    setattr(user, "partner_id", None)
    setattr(partner, "partner_id", None)
    user.save()
    partner.save()
    storage.save()
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    partner_name = partner.to_dict()['first_name'].capitalize() + " " + partner.to_dict()['last_name'].capitalize()
    f_message = f"Successfully Unbinded with {partner_name}"
    msg_1 = Message(from_user=user.to_dict()['id'], to_user=partner.to_dict()['id'], text=f_message)
    msg_1.save()
    storage.save()
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    session["redirected"] = True
    session["success_message"] = f_message
    return redirect(url_for("progress"))

@app.route("/progress", methods=["GET", "POST"], strict_slashes=False)
def progress():
    """Display and update the user's progress through their roadmap and courses."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if not session.get("user", {}).get("roadmap_id") and not storage.get_user_progress(session["user_id"], 1):
        session["redirected"] = True
        session["error_message"] = "Choose a roadmap first, to be able to see your progress!"
        return redirect(url_for("get_all_roadmaps"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if request.method == "GET":
        if storage.get_user_progress(session["user_id"], 0):
            my_progress_current = storage.get_user_progress(session["user_id"], 0).to_dict()
            all_courses = storage.get_roadmap_courses(my_progress_current["roadmap_id"])
            active_course = storage.get(Course, my_progress_current["course_id"]).to_dict()
            all_chapters = storage.get_course_chapters(my_progress_current["course_id"])
            active_chapter = storage.get(Chapter, my_progress_current["chapter_id"]).to_dict()
            completed_courses = []
            upcoming_courses = []
            for c in all_courses[:active_course["order_in_roadmap"]-1]:
                completed_courses.append(c.to_dict())
            for c in all_courses[active_course["order_in_roadmap"]:]:
                upcoming_courses.append(c.to_dict())
            completed_chapters = []
            upcoming_chapters = []
            for c in all_chapters[:active_chapter["order_in_course"]-1]:
                completed_chapters.append(c.to_dict())
            for c in all_chapters[active_chapter["order_in_course"]:]:
                upcoming_chapters.append(c.to_dict())
            if all_chapters[-1].to_dict()["order_in_course"] == active_chapter["order_in_course"]:
                message = "Great, start the following course"
                if all_courses[-1].to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"]:
                    roadmap_name = storage.get(Roadmap, my_progress_current["roadmap_id"]).to_dict()["title"]
                    message = "Great Job, Finishing the {} Roadmap, You may now take a break".format(roadmap_name)
                message = message
        else:
            completed_courses = []
            upcoming_courses = []
            completed_chapters = []
            upcoming_chapters = []
            active_course = []
            active_chapter = []
        ############ partner's progress
        if session["user"].get("partner_id") and storage.get_user_progress(session["user"].get("partner_id"), 0):
            partner_progress_current = storage.get_user_progress(session["user"].get("partner_id"), 0).to_dict()
            partner_all_courses = storage.get_roadmap_courses(partner_progress_current["roadmap_id"])
            partner_active_course = storage.get(Course, partner_progress_current["course_id"]).to_dict()
            partner_all_chapters = storage.get_course_chapters(partner_progress_current["course_id"])
            partner_active_chapter = storage.get(Chapter, partner_progress_current["chapter_id"]).to_dict()
            partner_completed_courses = []
            partner_upcoming_courses = []
            for c in partner_all_courses[:partner_active_course["order_in_roadmap"]-1]:
                partner_completed_courses.append(c.to_dict())
            for c in partner_all_courses[partner_active_course["order_in_roadmap"]:]:
                partner_upcoming_courses.append(c.to_dict())
            partner_completed_chapters = []
            partner_upcoming_chapters = []
            for c in partner_all_chapters[:partner_active_chapter["order_in_course"]-1]:
                partner_completed_chapters.append(c.to_dict())
            for c in partner_all_chapters[partner_active_chapter["order_in_course"]:]:
                partner_upcoming_chapters.append(c.to_dict())
        else:
            partner_completed_courses = []
            partner_upcoming_courses = []
            partner_completed_chapters = []
            partner_upcoming_chapters = []
            partner_active_course = []
            partner_active_chapter = []
        ############ partner's progress
        if storage.get_user_progress(session["user_id"], 1):
            completed_roadmaps = []
            roadmaps = storage.get_user_progress(session["user_id"], 1)
            for r in roadmaps:
                completed_roadmaps.append(storage.get(Roadmap, r.to_dict()["roadmap_id"]).to_dict()["title"])
        else:
            completed_roadmaps = None

        return render_template("progress.html", session=session, completed_courses=completed_courses, upcoming_courses=upcoming_courses, completed_chapters=completed_chapters, upcoming_chapters=upcoming_chapters, active_course=active_course, active_chapter=active_chapter, completed_roadmaps=completed_roadmaps, partner_completed_courses=partner_completed_courses,partner_upcoming_courses=partner_upcoming_courses,partner_completed_chapters=partner_completed_chapters,partner_upcoming_chapters=partner_upcoming_chapters,partner_active_course=partner_active_course,partner_active_chapter=partner_active_chapter, success_message=success_message, error_message=error_message)
        # completed_courses         [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as greeny to mark completed
        # upcoming_courses          [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as whitey to mark not yet completed
        # completed_chapters        [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as greeny to mark completed
        # upcoming_chapters         [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as whitey to mark not yet completed
        # active_course             [dictionary]                || take title
        # active_chapter            [dictionary]                || take title
        # add a button on this page to send an empty form POST to url_for(( progress )) with POST

    elif request.method == "POST":
        session["user"] = storage.get(User, session["user_id"]).to_dict()
        my_progress = storage.get_user_progress(session["user_id"])
        all_chapters = storage.get_course_chapters(my_progress.to_dict()["course_id"])
        active_chapter = storage.get(Chapter, my_progress.to_dict()["chapter_id"]).to_dict()
        if all_chapters[-1].to_dict()["order_in_course"] == active_chapter["order_in_course"]:
            all_courses = storage.get_roadmap_courses(my_progress.to_dict()["roadmap_id"])
            active_course = storage.get(Course, my_progress.to_dict()["course_id"]).to_dict()
            if all_courses[-1].to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"]:
                setattr(my_progress, "completed_roadmap", 1)
                my_progress.save()
                storage.save()
                user = storage.get(User, session['user_id'])
                partner_id = user.to_dict()["partner_id"]
                roadmap_title = storage.get(Roadmap, my_progress.to_dict()['roadmap_id']).to_dict()['title']
                message = f"Congratulations on finishing {roadmap_title} Roadmap!"
                if partner_id:
                    partner = storage.get(User, partner_id)
                    setattr(partner, "partner_id", None)
                    partner.save()
                    setattr(user, "partner_id", None)
                    user.save()
                    new_msg = Message(from_user=session.get("user_id"), to_user=partner_id, text="Successfully completed the Roadmap together.")
                    new_msg.save()
                    storage.save()
                setattr(user, "roadmap_id", None)
                user.save()
                storage.save()
            else:
                next_course = [c.to_dict() for c in all_courses if c.to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"] + 1]
                next_course_id = next_course[0]["id"]
                all_chapters = storage.get_course_chapters(next_course_id)
                active_chapter = [c for c in all_chapters if c.to_dict()['order_in_course'] == 1][0]
                next_chapter_id = active_chapter.to_dict()['id']
                setattr(my_progress, "course_id", next_course_id)
                setattr(my_progress, "chapter_id", next_chapter_id)
                my_progress.save()
                storage.save()
                message = f"Congratulations on finishing Course: {active_course['title']}!"
        else:
            desired_chapter = [c.to_dict() for c in all_chapters if c.to_dict()["order_in_course"] == active_chapter["order_in_course"] + 1][0]
            setattr(my_progress, "chapter_id", desired_chapter["id"])
            my_progress.save()
            storage.save()
            message = f"Congratulations on finishing Chapter: {active_chapter['title']}!"
        session["user"] = storage.get(User, session["user_id"]).to_dict()
        session["redirected"] = True
        session["success_message"] = message
        return redirect(url_for("progress"))

@app.route("/course/<course_id>", methods=["GET"], strict_slashes=False)
def course_details(course_id):
    """Retrieve and display the details of a single course."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    if not storage.get(Course, course_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Course!"
        return redirect(url_for("get_all_roadmaps"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    course = storage.get(Course, course_id).to_dict()
    chapters = storage.get_course_chapters(course_id)
    chapters = [chapter.to_dict() for chapter in chapters]
    vendors = storage.get_course_vendors(course_id)
    vendors = [vendor.to_dict() for vendor in vendors]
    return render_template("course.html", session=session, course=course, vendors=vendors, chapters=chapters)

@app.route("/messages", methods=["GET"], strict_slashes=False)
def messages():
    """Retrieve and display the user's messages."""
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    last_messages = storage.get_user_last_messages(session["user_id"])
    for msg in last_messages:
        msg['link'] = url_for('single_messaging', user_id=msg['other_user_id'])
        msg['other_user_photo'] = url_for("static", filename=f'images/{msg["other_user_photo"]}', _external=True)
    return render_template("messages.html", session=session, last_messages=last_messages)

@app.route("/messages/<user_id>", methods=["GET", "POST"], strict_slashes=False)
def single_messaging(user_id):
    """Retrieve and display a single messaging thread with another user."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    if not storage.get(User, user_id):
        session["redirected"] = True
        session["error_message"] = "Invalid user!"
        return redirect(url_for("home"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if request.method == "GET":
        other_user_name = storage.get(User, user_id).to_dict()
        other_user_name = other_user_name["first_name"] + " " + other_user_name["last_name"]
        our_user = session["user_id"]
        messages = storage.get_single_messaging(our_user, user_id)
        my_photo = url_for("static", filename=f'images/{session["user"].get("photo")}', _external=True)
        other_photo = storage.get(User, user_id).to_dict()["photo"]
        other_photo = url_for("static", filename=f'images/{other_photo}', _external=True)
        return render_template("single_messaging.html", session=session, messages=messages, other_user_name=other_user_name, user_id=user_id, my_photo=my_photo, other_photo=other_photo, error_message=error_message)

    elif request.method == "POST":
        text = request.form.get('text')
        if not text:
            session["redirected"] = True
            session["error_message"] = "Message text cannot be empty!"
            return redirect(url_for("single_messaging", user_id=user_id))
        our_user = session["user_id"]
        new_message = Message(from_user=our_user, to_user=user_id, text=text)
        new_message.save()
        storage.save()
        return redirect(url_for("single_messaging", user_id=user_id))

@app.route("/community", methods=["GET"], strict_slashes=False)
def community():
    """Retrieve and display all available communities."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    roadmaps_communities = storage.all(Roadmap).values()
    roadmaps_communities = [c.to_dict() for c in roadmaps_communities]
    for c in roadmaps_communities:
        c['link'] = url_for('single_community', roadmap_id=c['id'], _external=True)
    return render_template("communities.html", session=session, roadmaps_communities=roadmaps_communities, error_message=error_message)

@app.route("/community/<roadmap_id>", methods=["GET", "POST"], strict_slashes=False)
def single_community(roadmap_id):
    """Retrieve and display a single community and its messages."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        session.pop('redirected', None)
        session.pop('error_message', None)
    else:
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    if not storage.get(Roadmap, roadmap_id):
        session["redirected"] = True
        session["error_message"] = "Invalid Roadmap!"
        return redirect(url_for("community"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    if session.get("user", {}).get("roadmap_id") == roadmap_id:
        ability_to_send = True
    elif storage.get_user_progress(session["user_id"], 1):
        last_roadmap = storage.get_user_progress(session["user_id"], 1)[-1].to_dict()["roadmap_id"] == roadmap_id
        if last_roadmap:
            ability_to_send = True
        else:
            ability_to_send = False
    else:
        ability_to_send = False
    if request.method == "GET":
        our_user = session['user_id']
        community_messages = storage.get_community_messaging(our_user, roadmap_id)
        for msg in community_messages:
            msg['profile_link'] = url_for("get_another_user", user_id=msg["from_user"])
            msg['photo'] = url_for("static", filename=f'images/{msg["photo"]}', _external=True)
        page_title = storage.get(Roadmap, roadmap_id).to_dict()['title']
        return render_template("single-community-messaging.html", session=session, messages=community_messages, page_title=page_title, ability_to_send=ability_to_send, roadmap_id=roadmap_id, error_message=error_message)

    elif request.method == "POST":
        if not ability_to_send:
            if session.get("user", {}).get("roadmap_id"):
                return redirect(url_for("single_community", roadmap_id=session.get("user", {}).get("roadmap_id")))
            else:
                session["redirected"] = True
                session["error_message"] = "You can't participate in this roadmap conversion. Please choose your desired roadmap first!"
                return redirect(url_for("get_all_roadmaps"))
        text = request.form.get('text')
        if not text:
            session["redirected"] = True
            session["error_message"] = "Message text cannot be empty!"
            return redirect(url_for("single_community", roadmap_id=roadmap_id))
        our_user = session['user_id']
        new_message = Message(from_user=our_user, to_roadmap=roadmap_id, text=text)
        new_message.save()
        storage.save()
        return redirect(url_for("single_community", roadmap_id=roadmap_id))

@app.route("/binding-requests", methods=["GET"], strict_slashes=False)
def binding_requests():
    """Retrieve and display all binding requests (sent and received)."""
    if 'redirected' in session and session.get("error_message"):
        error_message = session.get("error_message")
        success_message = None
        session.pop('redirected', None)
        session.pop('error_message', None)
    elif 'redirected' in session and session.get("success_message"):
        success_message = session.get("success_message")
        error_message = None
        session.pop('redirected', None)
        session.pop('success_message', None)
    else:
        success_message = None
        error_message = None
    if not session.get("logged_in"):
        session["redirected"] = True
        session["error_message"] = "You must be logged in to access this content!"
        return redirect(url_for("login"))
    session["user"] = storage.get(User, session["user_id"]).to_dict()
    sent_request = storage.get_sent_requests(session["user_id"])
    sent_requests = []
    for req in sent_request:
        req = req.to_dict()
        other_user = storage.get(User, req["to_user"]).to_dict()
        req["user_name"] = other_user["first_name"] + " " + other_user["last_name"]
        req["retract"] = url_for("retract_binding", partner_id=other_user["id"])
        sent_requests.append(req)
    received_request = storage.get_received_requests(session["user_id"])
    received_requests = []
    for req in received_request:
        req = req.to_dict()
        other_user = storage.get(User, req["from_user"]).to_dict()
        req["user_name"] = other_user["first_name"] + " " + other_user["last_name"]
        req["accept"] = url_for("accept_binding", partner_id=other_user["id"])
        received_requests.append(req)
    return render_template("bindrequests.html", sent_requests=sent_requests, received_requests=received_requests, success_message=success_message, error_message=error_message)
    

if __name__ == "__main__":
    app.run(host=api_host, port=api_port
            , debug=True
            , threaded=True)
