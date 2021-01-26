from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json
# import config

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

#config 파일 연결...헷갈림
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object(config)
db = SQLAlchemy(app)
db.create_all()
# migrate.init_app(app,db)
# api = Api(app)

# def init_db():
#     db.init_app(app)
#     db.app = app
#     with app.app_context():
#         db.create_all()
# from models import User, Board, BoardArticle

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

members = User.query.all()
print(members)
# for m in members:
#     print("printing user", m)
# parser = reqparse.RequestParser()
# parser.add_argument(키 값)

# newuser
# 0000
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


# api.add_resource(Home, '/')
@app.route('/')
def home():
    return "hello"

if __name__ == "__main__":
    # app.init_db()
    app.run(debug = True)