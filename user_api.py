from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from config import config
from models import db, User

import json

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


parser = reqparse.RequestParser()
parser.add_argument("fullname")
parser.add_argument("email")
parser.add_argument("password")
#args["fullname"] 처럼 쓴다.

class SignUp(Resource):
    def post(self):
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
                response = {
                    "status":"success", 
                    "result" : {"name": username,"email": user_email}, 
                    "message" : "successfully signed in"}
                return jsonify(response)
            else:
                #user already exists
                response = {
                    "status" : "error", 
                    "message" :"user already exists"
                }
                return jsonify(response)
        else:
            response = {
                "status" : "error", 
                "message" : "fill in the required information to register"
            }
            return jsonify(response)

class Login(Resource):
    def post(self):
        args = parser.parse_args()
        user_email = args["email"]
        user_password = args["password"]
        #email과 password 둘 다 입력되었는지에 대한 조건문 필요!
        valid_user = User.query.filter_by(email = user_email).first()
        err_response = {
            "status" : "error",
            "message" : "invalid user or a wrong password"
            }
        if valid_user:
            if check_password_hash(valid_user.password, user_password):
                # access_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                # access_token = create_access_token(identity = valid_user.id, expires_delta = access_expires)
                # session.clear() #pop과 차이가 뭐지? 왜 로그인하는데 session을 clear하지?
                #session이 비어있지 않은 상황이면 다른 유저가 로그인 되어있다는거 아닌가???? 그걸 clear해도 되나?
                session['user'] = valid_user.id
                response = {
                    "status" : "success",
                    "result" : valid_user.id,
                    "message" : "user is successfully logged in"
                }
                return jsonify(response)
            else:
                return jsonify(err_response)
        else:
            return jsonify(err_response)

class Logout(Resource):
    def post(self):
        if 'user' in session:
            session.pop('user', None)
            response = {
                "status": "success",
                "message": "user is successfully logged out"
            }
            return jsonify(response)