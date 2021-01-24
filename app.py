from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json

# db = SQLAlchemy()
# migrate = Migrate()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument(키 값)
# app.config ['SQLALCHEMY_DATABASE_URI'] = ''#datbase url

# db.init_app(app)
# migrate.init_app(app, db)
# from models import User

class Home(Resource):
    def get(self):
        msg ={"message": "Hello World"}
        return jsonify(status="success", result=msg)


api.add_resource(Home, '/')

if __name__ == "__main__":
    app.run(debug = True)