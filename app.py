# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_pymongo import PyMongo
from flask import session


# -- Initialization section --
app = Flask(__name__)  # the app

# events = [
#         {"event":"First Day of Classes", "date":"2019-08-21"},
#         {"event":"Winter Break", "date":"2019-12-20"},
#         {"event":"Finals Begin", "date":"2019-12-01"}
#     ]

# name of database
app.config['MONGO_DBNAME'] = 'database'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:Dw84pzbMkdHNBoJs@cluster0.lndrp.mongodb.net/database?retryWrites=true&w=majority'

mongo = PyMongo(app)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# -- Routes section --
# INDEX


@app.route('/')
@app.route('/index')
def index():
    session.clear()
    session["username"] = "huan"
    events = mongo.db.events  # creates events in mongo even though you might not have one
    events = events.find({})
    return render_template('index.html', events=events)


# CONNECT TO DB, ADD DATA

@app.route('/add')
def add():
    # connect to the database
    events = mongo.db.events

    # insert new data
    events.insert({"event": "First Day of Classes",
                   "date": "2021-09-13"})

    events.insert({"event": "birthday",
                   "date": "2003-04-24"})

    # return a message to the user
    return "event added"


@app.route('/events/new', methods=['GET', 'POST'])
def new_event():
    if request.method == 'GET':
        return render_template('newevent.html')
    else:
        event_name = request.form["event_name"]
        event_date = request.form["event_date"]
        user_name = request.form["user_name"]
        events = mongo.db.events
        events.insert({
            "event": event_name,
            "date": event_date,
            "user": user_name
        })
        # events = events.find({})
       # return render_template("index.html", events = events)
        return redirect("/")


# login page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # this creates a user's database in mongo db if it doesn't already exist

        users = mongo.db.users

        # this stores form data into a user's dictionary
        user = {
            "username": request.form["username"],
            "password": request.form["password"]
        }
        users.insert(user)  # add our user data into mongo
       # tell the browser session who the user is
        session["username"] = request.form["username"]
        return "you made an account " + request.form["username"]
        return "You made an account"
