from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from config import config
from models import db, User, Board, BoardArticle

import json

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
# from flask_jwt_extended import (
#     JWTManager, jwt_required, create_access_token, get_jwt_identity, decode_token)
# from datetime import timedelta, datetime

from user_api import SignUp, Login, Logout

# db = SQLAlchemy()
# migrate = Migrate()
# migrate 없어도 되지 않나...? 써야 하는 상황과 쓰지 않아도 되는 상황을 구분하는 법 궁금...

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

# ACCESS_TOKEN_EXPIRE_MINUTES = 60 #change later
# jwt = JWTManager(app)

api = Api(app)


#이거 보고 따라하기!!!!!!config, models 분리
#https://oluchiorji.com/flask-app-authentication-with-jwt/


api.add_resource(SignUp, '/register')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == "__main__":
    # app.init_db()
    app.run(debug = True)