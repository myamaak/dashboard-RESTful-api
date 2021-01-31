from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from config import config
from models import db, User, Board, BoardArticle

import json

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, decode_token)
from datetime import timedelta, datetime


# db = SQLAlchemy()
# migrate = Migrate()
# migrate 없어도 되지 않나...? 써야 하는 상황과 쓰지 않아도 되는 상황을 구분하는 법 궁금...

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

ACCESS_TOKEN_EXPIRE_MINUTES = 60 #change later
jwt = JWTManager(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("fullname")
parser.add_argument("email")
parser.add_argument("password")
#args["fullname"] 처럼 쓴다.

# @app.route("/register", methods=['GET','POST'])
# def SignUp():
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

#이거 보고 따라하기!!!!!!config, models 분리
#https://oluchiorji.com/flask-app-authentication-with-jwt/

          
#token을 왜 사용하는지 
#https://lewisxyz000.tistory.com/25
#create & refresh token 사용하기
# https://blog.tecladocode.com/jwt-authentication-and-token-refreshing-in-rest-apis/
#정 힘들면 session만 이용한 방법도 있음(쉬움)
#https://fenderist.tistory.com/145?category=717421

#logout - blacklist jwt
#https://flask-jwt-extended.readthedocs.io/en/stable/blacklist_and_token_revoking/
#블랙리스트 한국어 예시
#https://blog.oseonsik.com/2020/11/20/flask-jwt-extended%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%9C-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EA%B5%AC%ED%98%84/
# flask jwt blacklist 인증 으로 검색
# @app.route("/login", methods=['GET', 'POST'])
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
                access_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(identity = valid_user.id, expires_delta = access_expires)
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
    def delete(self):
        if 'user' in session:
            session.pop('user', None)
            response = {
                "status": "success",
                "message": "user is successfully logged out"
            }
            return jsonify(response)
    
# api.add_resource(user_api, '/user')

# @app.route('/')
# def home():
    
#     members = User.query.all()
#     for i in members:
#         print(i.username)
#     return "hello"

api.add_resource(SignUp, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == "__main__":
    # app.init_db()
    app.run(debug = True)