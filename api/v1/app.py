# from flask import Flask, make_response, jsonify
# from models import  storage
# # from api.v1.views import app_views
# from os import getenv
# from flask_cors import CORS

# app = Flask(__name__)
# api_host = getenv("TM_API_HOST", "0.0.0.0")
# api_port = getenv("TM_API_PORT", "5000")
# CORS(app, resources={"/*": {"origins": api_host}})

# # app.register_blueprint(app_views)

# @app.teardown_appcontext
# def tear_down(exc):
#     storage.close()
# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
# ##############################################################
# from models.user import User
# from models.roadmap import Roadmap
# from models.course import Course
# from models.chapter import Chapter
# from models.message import Message
# from models.progress import Progress
# from models.vendor import Vendor
# from models.contact_us import ContactUs
# from models import storage
# from flask import request, render_template, redirect, session, url_for, flash
# from werkzeug.security import generate_password_hash, check_password_hash

# @app.route("/login", methods=["GET", "POST"], strict_slashes=False)
# def login():
#     # if session.get("logged_in"):
#     #     flash("You must be logged in to access this content")
#     #     return redirect(url_for("get_current_user"))
#     if request.method == "POST":
#         email = request.form.get('email')
#         password = request.form.get('password')
#         user = storage.get_user_by_email(email)
#         if not user or not check_password_hash(user.password, password):
#             flash("Please check your login details and try again.")
#             return redirect(url_for('login'))
#         session["logged_in"] = True
#         session["user_id"] = user.to_dict().get('id')
#         session["user"] = user.to_dict()
#         return redirect(url_for("home"))
#     else:
#         print("==========================")
#         print('login working')
#         print("==========================")
#         return render_template("login.html", session=session)

# @app.route("/profile", methods=["GET"], strict_slashes=False)
# def get_current_user():
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for('login'))
#     user = session["user"]
#     if not user["roadmap_id"]:
#         data = {"user_name": user["first_name"] + " " + user["last_name"]}
#     else:
#         data = {}
#         user_progress = storage.get_user_progress(user_id=user["id"])[0]
#         current_roadmap = storage.get(Roadmap, user_progress["roadmap_id"]).to_dict()
#         data["current_roadmap"] = current_roadmap["title"]
#         roadmap_courses = storage.get_roadmap_courses(user_progress["roadmap_id"])
#         current_course = storage.get(Course, user_progress["course_id"]).to_dict()
#         data["current_course"] = current_course["title"]
#         completed_courses = []
#         for c in roadmap_courses[:int(current_course["order_in_roadmap"]) - 1]:
#             completed_courses.append(c["title"])
#         data["completed_courses"] = completed_courses
#         if user["partner_id"]:
#             partner = storage.get(User, user["partner_id"]).to_dict()
#             partner_name = partner["first_name"] + " " + partner["last_name"]
#         else:
#             partner_name = None
#         data["partner_name"] = partner_name
#         user_name = user["first_name"] + " " + user["last_name"]
#         data["user_name"] = user_name
#     return render_template("profile", data=data, session=session, message_link=None)
#     # data          [dictionary]    || check for each attribute if it exists (current_roadmap, current_course, completed_courses, partner_name, user_name[this is title of the profile page]) if it exists show it's section in page, if not, don't
#     # message_link  [string]        || if True: put it in a "Message User" in an href button || contains a link to start messaging this user.

# @app.route("/profile/<user_id>", methods=["GET"], strict_slashes=False)
# def get_another_user(user_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for('login'))
#     if not storage.get(User, user_id):
#         flash("Invalid user!")
#         return redirect(url_for("get_current_user"))
#     if session.get("user_id") == user_id:
#         return redirect(url_for('get_current_user'))
#     user = storage.get(User, user_id).to_dict()
#     if not user["roadmap_id"]:
#         data = {"user_name": user["first_name"] + " " + user["last_name"]}
#     else:
#         data = {}
#         user_progress = storage.get_user_progress(user_id=user["id"])[0]
#         current_roadmap = storage.get(Roadmap, user_progress["roadmap_id"]).to_dict()
#         data["current_roadmap"] = current_roadmap["title"]
#         roadmap_courses = storage.get_roadmap_courses(user_progress["roadmap_id"])
#         current_course = storage.get(Course, user_progress["course_id"]).to_dict()
#         data["current_course"] = current_course["title"]
#         completed_courses = []
#         for c in roadmap_courses[:int(current_course["order_in_roadmap"]) - 1]:
#             completed_courses.append(c["title"])
#         data["completed_courses"] = completed_courses
#         if user["partner_id"]:
#             partner = storage.get(User, user["partner_id"]).to_dict()
#             partner_name = partner["first_name"] + " " + partner["last_name"]
#         else:
#             partner_name = None
#         data["partner_name"] = partner_name
#         user_name = user["first_name"] + " " + user["last_name"]
#         data["user_name"] = user_name
#     message_link = url_for("single_messaging", user_id=user_id, _external=True)
#     return render_template("profile", data=data, session=session, message_link=message_link)

# @app.route("/signup", methods=["GET", "POST"], strict_slashes=False)
# def create_user():
#     if session.get("logged_in"):
#         flash("You already logged in, how did you get here?")
#         return redirect(url_for("get_current_user"))
#     if request.method == "POST":
#         email = request.form.get('email')
#         first_name = request.form.get('first_name')
#         last_name = request.form.get('last_name')
#         password = request.form.get('password')
#         phone = request.form.get('phone')
#         exists = storage.get_user_by_email(email)
#         if exists:
#             flash('Email address already exists')
#             return redirect(url_for(create_user))
#         new_user = User(email=email, first_name=first_name, last_name=last_name, phone=phone, password=generate_password_hash(password, method="sha256"))
#         new_user.save()
#         storage.save()
#         return redirect(url_for("login"))
#     elif request.method == "GET":
#         return render_template("signup", session=session)

# @app.route('/logout', methods=["POST"], strict_slashes=False)
# def logout():
#     if not session.get("logged_in"):
#         return redirect(url_for("login"))
#     session["logged_in"] = False
#     session["user_id"] = None
#     session["user"] = None
#     return redirect(url_for("home"))

# @app.route('/', methods=["GET"], strict_slashes=False)
# def home():
#     return render_template("", session=session)

# @app.route('/contact-us', methods=["GET"], strict_slashes=False)
# def contact_us():
#     return render_template("contactus", session=session)

# @app.route('/about', methods=["GET"], strict_slashes=False)
# def about():
#     return render_template("about", session=session)

# @app.route("/roadmaps", methods=["GET"], strict_slashes=False)
# def get_all_roadmaps():
#     all_roadmaps = [r.to_dict() for r in storage.all(Roadmap).values()]
#     for r in all_roadmaps:
#         r['link'] = url_for("get_single_roadmap", roadmap_id=r['id'], _external=True)
#     return render_template("roadmaps", session=session, roadmaps=all_roadmaps)
#     # roadmaps      [list of dictionaries]      || for loop over, and for each dictionary take (title, description, link)

# @app.route("/roadmaps/<roadmap_id>", methods=["GET"], strict_slashes=False)
# def get_single_roadmap(roadmap_id):
#     if not storage.get(Roadmap, roadmap_id):
#         flash("Invalid Roadmap")
#         return redirect(url_for("get_all_roadmaps"))
#     other_roadmaps = [r.to_dict() for r in storage.all(Roadmap).values()]
#     roadmap = storage.get(Roadmap, roadmap_id).to_dict()
#     other_roadmaps.remove(roadmap)
#     for r in other_roadmaps:
#         r["link"] = url_for("get_single_roadmap", roadmap_id=r["id"], _external=True)
#     courses = [c.to_dict() for c in storage.get_roadmap_courses(roadmap_id)]
#     for c in courses:
#         c['link'] = url_for("course_details", course_id=c['id'], _external=True)
#     return render_template("single_roadmap", session=session, roadmap=roadmap, other_roadmaps=other_roadmaps, courses=courses)
#     # roadmap               [dictionary]                || take (title, slug, description)
#     # other_roadmaps        [list of dictionaries]      || for loop over, and for each dictionary take (title, slug, link)
#     # courses               [list of dictionaries]      || for loop over, and for each dictionary take (title, description, link)

# @app.route("/roadmaps/<roadmap_id>/enroll", methods=["POST"], strict_slashes=False)
# def enroll_in_roadmap(roadmap_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if not storage.get(Roadmap, roadmap_id):
#         flash("Invalid roadmap!")
#         return redirect(url_for("get_all_roadmaps"))
#     if session.get("user", {}).get("roadmap_id"):
#         passed = storage.get_user_progress(session["user_id"]).to_dict().get('completed_roadmap')
#         if not passed:
#             flash("You already have an active roadmap")
#             return redirect(url_for("progress"))
#     user = storage.get(User, session["user_id"])
#     passed = storage.get_user_progress(session["user_id"]).to_dict().get('completed_roadmap')
#     if passed:
#         progress = storage.get_user_progress(session["user_id"])
#         storage.delete(progress)
#         storage.save()
#         setattr(user, "roadmap_id", None)
#     setattr(user, "roadmap_id", roadmap_id)
#     storage.save()
#     user_id = session["user_id"]
#     active_roadmap = storage.get(Roadmap, roadmap_id).to_dict()['id']
#     active_course = storage.get_active_course_by_roadmap_and_order(roadmap_id).to_dict()['id']
#     active_chapter = storage.get_active_chapter_by_course_and_order(roadmap_id).to_dict()['id']
#     new_progress = Progress(user_id=user_id, roadmap_id=active_roadmap, course_id=active_course, chapter_id=active_chapter, completed_roadmap=0)
#     new_progress.save()
#     storage.save()
#     session["user"] = storage.get(User, session["user_id"]).to_dict()
#     return redirect(url_for("progress"))

# @app.route("/roadmaps/<roadmap_id>/partners", methods=["GET"], strict_slashes=False)
# def get_roadmap_partners(roadmap_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if session.get("user", {}).get("partner_id", ""):
#         flash("One partner is enough")
#         return redirect(url_for("progress"))
#     if session.get("user", {}).get("roadmap_id", "") != roadmap_id:
#         flash("Wrong roadmap")
#         return redirect(url_for("get_all_roadmaps"))
#     if not storage.get(Roadmap, roadmap_id):
#         flash("Invalid roadmap!")
#         return redirect(url_for("get_all_roadmaps"))
#     roadmap = storage.get(Roadmap, roadmap_id).to_dict()
#     roadmap_title = roadmap["title"] + ": Available Partners"
#     partners = [r.to_dict() for r in storage.get_available_partners(roadmap_id) if r.to_dict()['id'] != session.get('user')['id']]
#     for p in partners:
#         p['fullname'] = p['first_name'] + " " + p['last_name']
#         p['link'] = url_for("get_another_user", user_id=p['id'], _external=True)
#         p['button'] = url_for("bind_partners", roadmap_id=roadmap_id, partner_id=p['id'])
#     return render_template("partners", session=session, roadmap_title=roadmap_title, partners=partners)
#     # roadmap_title             [string]                    || title of the page
#     # partners                  [list of dictionaries]      || for loop over, and for each dictionary take (fullname, link, button)
#     #                                                       || when I click on their name, it opens the link (as href)
#     #                                                       || button on the right, when I click it, it sends an empty post request to that url in button attribute


# @app.route("/roadmaps/<roadmap_id>/partners/<partner_id>/bind", methods=["POST"], strict_slashes=False)
# def bind_partners(roadmap_id, partner_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if session.get("user", {}).get("roadmap_id", "") != roadmap_id:
#         flash("Wrong roadmap")
#         return redirect(url_for("get_all_roadmaps"))
#     if session.get("user", {}).get("partner_id", ""):
#         flash("One partner is enough")
#         return redirect(url_for("progress"))
#     partner = storage.get(User, partner_id)
#     if partner.to_dict().get('partner_id'):
#         flash("Partner already binded")
#         return redirect(url_for("get_roadmap_partners", roadmap_id=roadmap_id))
#     if not storage.get(Roadmap, roadmap_id):
#         flash("Invalid roadmap!")
#         return redirect(url_for("get_all_roadmaps"))
#     if not storage.get(User, partner_id):
#         flash("Invalid user!")
#         return redirect(url_for("get_current_user"))
#     user = storage.get(User, session.get('user_id'))
#     setattr(user, "partner_id", partner_id.to_dict()['id'])
#     setattr(partner, "partner_id", user.to_dict()['id'])
#     storage.save()
#     partner_name = partner.to_dict()['first_name'].capitalize() + " " + partner.to_dict()['last_name'].capitalize()
#     user_name = user.to_dict()['first_name'].capitalize() + " " + user.to_dict()['last_name'].capitalize()
#     f_message = f"Successfully Binded with {partner_name}"
#     s_message = f"Successfully Binded with {user_name}"
#     msg_1 = Message(from_user=user.to_dict()['id'], to_user=partner.to_dict()['id'], text=f_message)
#     msg_1.save()
#     msg_2 = Message(from_user=partner.to_dict()['id'], to_user=user.to_dict()['id'], text=s_message)
#     msg_2.save()
#     storage.save()
#     flash(f_message)
#     session["user"] = storage.get(User, session["user_id"]).to_dict()
#     return redirect(url_for("messages"))

# @app.route("/progress", methods=["GET", "POST"], strict_slashes=False)
# def progress():
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if not session.get("user", {}).get("roadmap_id"):
#         flash("Choose a roadmap first")
#         return redirect(url_for("get_all_roadmaps"))
#     if request.method == "GET":
#         my_progress = storage.get_user_progress(session["user_id"]).to_dict()
#         all_courses = storage.get_roadmap_courses(my_progress["roadmap_id"])
#         active_course = storage.get(Course, my_progress["course_id"]).to_dict()
#         all_chapters = storage.get_course_chapters(my_progress["course_id"])
#         active_chapter = storage.get(Chapter, my_progress["chapter_id"]).to_dict()
#         completed_courses = []
#         upcoming_courses = []
#         for c in all_courses[:active_course["order_in_roadmap"]-1]:
#             completed_courses.append(c.to_dict())
#         for c in all_courses[active_course["order_in_roadmap"]:]:
#             upcoming_courses.append(c.to_dict())
#         completed_chapters = []
#         upcoming_chapters = []
#         for c in all_chapters[:active_chapter["order_in_course"]-1]:
#             completed_chapters.append(c.to_dict())
#         for c in all_chapters[active_chapter["order_in_course"]:]:
#             upcoming_chapters.append(c.to_dict())
#         if all_chapters[-1].to_dict()["order_in_course"] == active_chapter["order_in_course"]:
#             message = "Great, start the following course"
#             if all_courses[-1].to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"]:
#                 roadmap_name = storage.get(Roadmap, my_progress["roadmap_id"]).to_dict()["title"]
#                 message = "Great Job, Finishing the {} Roadmap, You may now take a break".format(roadmap_name)
#             flash(message)
#         return render_template("progress", session=session, completed_courses=completed_courses, upcoming_courses=upcoming_courses, completed_chapters=completed_chapters, upcoming_chapters=upcoming_chapters, active_course=active_course, active_chapter=active_chapter)
#         # completed_courses         [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as greeny to mark completed
#         # upcoming_courses          [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as whitey to mark not yet completed
#         # completed_chapters        [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as greeny to mark completed
#         # upcoming_chapters         [list of dictionaries]      || for loop over, and for each dictionary take (title) || if True(exists), show as whitey to mark not yet completed
#         # active_course             [dictionary]                || take title
#         # active_chapter            [dictionary]                || take title
#         # add a button on this page to send an empty form POST to url_for(( progress )) with POST

#     elif request.method == "POST":
#         my_progress = storage.get_user_progress(session["user_id"])
#         if my_progress.to_dict()["completed_roadmap"]:
#             flash("You already completed the roadmap, Congrats")
#             return redirect(url_for("progress"))
#         all_chapters = storage.get_course_chapters(my_progress.to_dict()["course_id"])
#         active_chapter = storage.get(Chapter, my_progress.to_dict()["chapter_id"]).to_dict()
#         if all_chapters[-1]["order_in_course"] == active_chapter["order_in_course"]:
#             all_courses = storage.get_roadmap_courses(my_progress.to_dict()["roadmap_id"])
#             active_course = storage.get(Course, my_progress.to_dict()["course_id"]).to_dict()
#             if all_courses[-1].to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"]:
#                 setattr(my_progress, "completed_roadmap", True)
#                 my_progress.save()
#                 storage.save()
#             else:
#                 next_course = [c.to_dict() for c in all_courses if c.to_dict()["order_in_roadmap"] == active_course["order_in_roadmap"] + 1]
#                 next_course_id = next_course["id"]
#                 all_chapters = storage.get_course_chapters(next_course_id)
#                 active_chapter = [c for c in all_chapters if c.to_dict()['order_in_course'] == 1][0]
#                 next_chapter_id = active_chapter.to_dict()['id']
#                 setattr(my_progress, "course_id", next_course_id)
#                 setattr(my_progress, "chapter_id", next_chapter_id)
#                 my_progress.save()
#                 storage.save()
#         else:
#             desired_chapter = [c.to_dict() for c in all_chapters if c.to_dict()["order_in_course"] == active_chapter["order_in_course"] + 1][0]
#             setattr(my_progress, "chapter_id", desired_chapter["id"])
#             my_progress.save()
#             storage.save()
#         session["user"] = storage.get(User, session["user_id"]).to_dict()
#         return redirect(url_for("progress"))

# @app.route("/course/<course_id>", methods=["GET"], strict_slashes=False)
# def course_details(course_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if not storage.get(Course, course_id):
#         flash("Invalid course!")
#         return redirect(url_for("get_all_roadmaps"))
#     course = storage.get(Course, course_id).to_dict()
#     chapters = storage.get_course_chapters(course_id)
#     chapters = [chapter.to_dict()['title'] for chapter in chapters]
#     vendors = storage.get_course_vendors(course_id)
#     vendors = [vendor.to_dict() for vendor in vendors]
#     return render_template("single_course", session=session, course=course, vendors=vendors, chapters=chapters)
#     # course                [dictionary]                    || take (title, description)
#     # vendors               [list of dictionaries]          || take (name, link, cost)
#     # chapters              [list of dictionaries]          || take (title)

# @app.route("/messages", methods=["GET"], strict_slashes=False)
# def messages():
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     last_messages = storage.get_user_last_messages(session["user_id"])
#     return render_template("messages", session=session, last_messages=last_messages)
#     # last_messages         [list of dictionaries]                    || if not last_messages -> display "You have no messages!" ELSE, do as the following line
#     #                                                                 || for loop over, and for each dictionary take (other_user_name, last_message_sent, time)

# @app.route("/messages/<user_id>", methods=["GET", "POST"], strict_slashes=False)
# def single_messaging(user_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if not storage.get(User, user_id):
#         flash("Invalid user!")
#         return redirect(url_for("get_current_user"))
#     if request.method == "GET":
#         other_user_name = storage.get(User, user_id).to_dict()
#         other_user_name = other_user_name["first_name"] + " " + other_user_name["last_name"]
#         our_user = session["user_id"]
#         messages = storage.get_single_messaging(our_user, user_id)
#         return render_template("single_messaging", session=session, messages=messages, other_user_name=other_user_name)
#         # messages                      [list of dictionaries]              || for loop over, and for each dictionary take (text, sender_same_user)
#         #                                                                   || sender_same_user is (True or False), flag, if True, this means that the current user sent this message, so this message 
#         #                                                                   || is on the right side, if False, this means the other sent this message, so this one is on the left side of the conversation.
#         # other_user_name               [string]                            || other user name
#     elif request.method == "POST":
#         text = request.form.get('text')
#         new_message = Message(from_user=our_user, to_user=user_id, text=text)
#         new_message.save()
#         storage.save()
#         return redirect(url_for("single_messaging", user_id=user_id))

# @app.route("/community", methods=["GET"], strict_slashes=False)
# def community():
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     roadmaps_communities = storage.all(Roadmap).values()
#     roadmaps_communities = [c.to_dict() for c in roadmaps_communities]
#     for c in roadmaps_communities:
#         c['link'] = url_for('single_community', roadmap_id=c['id'], _external=True)
#     return render_template("all_communities", session=session, roadmaps_communities=roadmaps_communities)
#     # roadmaps_communities              [list of dictionaries]              || for loop over, and for each dictionary take (title, description, link)
#     #                                                                       || when I click on title, I go the the href in link

# @app.route("/community/<roadmap_id>", methods=["GET", "POST"], strict_slashes=False)
# def single_community(roadmap_id):
#     if not session.get("logged_in"):
#         flash("You must be logged in to access this content")
#         return redirect(url_for("login"))
#     if not storage.get(Roadmap, roadmap_id):
#         flash("Invalid roadmap!")
#         return redirect(url_for("community"))
#     if not session.get("user", {}).get("roadmap_id") != roadmap_id:
#         ability_to_send = False
#     else:
#         ability_to_send = True
#     if request.method == "GET":
#         our_user = session['user_id']
#         community_messages = storage.get_community_messaging(our_user, roadmap_id)
#         page_title = storage.get(Roadmap, roadmap_id).to_dict()['title']
#         return render_template("single_community", session=session, messages=community_messages, page_title=page_title, ability_to_send=ability_to_send)
#         # messages                      [list of dictionaries]              || for loop over, and for each dictionary take (text, sender_same_user, sender) sender is sender's name
#         # page_title                    [string]                            || title of the page
#         # ability_to_send               [list of dictionaries]              || True or False, if True, show a text box for the user to type a message, and a
#         #                                                                   || send button, that makes a form request, to send the message.
#         #                                                                   || If False, don't show the text box for him/her to send a message

#     elif request.method == "POST":
#         if not ability_to_send:
#             if session.get("user", {}).get("roadmap_id"):
#                 flash("You can't participate in this roadmap conversion")
#                 return redirect(url_for("home"))
#             else:
#                 flash("You can't participate in this roadmap conversion. Please choose your desired roadmap")
#                 return redirect(url_for("get_all_roadmaps"))
#         text = request.form.get('text')
#         our_user = session['user_id']
#         new_message = Message(from_user=our_user, to_roadmap=roadmap_id, text=text)
#         new_message.save()
#         storage.save()
#         return redirect(url_for("single_community", roadmap_id=roadmap_id))


# ####################################################################
# if __name__ == "__main__":
#     app.run(host=api_host, port=api_port, threaded=True, debug=True)
