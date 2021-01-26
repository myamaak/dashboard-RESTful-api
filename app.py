from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey

import json
# import config

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity)
from datetime import timedelta, datetime

db_config = {
    'user'     : 'newuser',
    'password' : '0000',
    'host'     : '127.0.0.1',
    'port'     : '3306',
    'database' : 'rest_api'
}

DB_URI = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8" 
#https://velog.io/@inyong_pang/Flask-API-MySQL-%EC%97%B0%EB%8F%99-SQLAlchemy

# db = SQLAlchemy()
# migrate = Migrate()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dev'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #change later
jwt = JWTManager(app)

api = Api(app)

#db settings start
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    boardname = db.Column(db.String(64), nullable=False)
    create_date = db.Column(db.DateTime(timezone=True), default= func.now())
    #https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime -> timestamp sqlalchemy
    user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, boardname, user_id):
        self.boardname = boardname
        self.user_id = user_id

class BoardArticle(db.Model):
    __tablename__ = 'boardArticle'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    board_id = db.Column(db.Integer, ForeignKey('board.id'))
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    create_date = db.Column(db.DateTime(timezone=True), default= func.now())

    def __init__(self, title, content, board_id, user_id):
        self.title = title
        self.content = content
        self.board_id = board_id
        self.user_id = user_id
#db settings end

parser = reqparse.RequestParser()
parser.add_argument("fullname")
parser.add_argument("email")
parser.add_argument("password")
#args["fullname"] 처럼 쓴다.

@app.route("/register", methods=['POST'])
def SignUp():
    args = parser.parse_args()
    username = args["fullname"]
    user_email = args["email"]
    user_password = args["password"]
    if username and user_email and user_password:
        user_password = generate_password_hash(user_password)
        check_user = User.query.filter(User.email == user_email).count()
        print(check_user)
        if check_user == 0:
            new_user = User(username, user_email, user_password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify(status="success", result = {"name": username,"email": user_email})
        else:
            #user already exists
            return jsonify(status = "redirection", result ="user already exists")
    else:
        #error
        return jsonify(status="redirection", result= "fill in the required information to register")

# new = User("this", "success@plz.com" , 1111)
# db.session.add(new)
# db.session.commit()
# class User(Resource):
#     def SignUp(self): #create
#         msg ={"message": "Hello World"}
#         return jsonify(status="success", result=msg)
#     def Login(self):
#         return 
#     def Logout(self):
#         return


# api.add_resource(user_api, '/user')

@app.route('/')
def home():
    members = User.query.all()
    for i in members:
        print(i.username)
    return "hello"

if __name__ == "__main__":
    # app.init_db()
    app.run(debug = True)