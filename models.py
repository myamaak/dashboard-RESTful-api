from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
db = SQLAlchemy()
# from app import db

# db = SQLAlchemy(app)
# db.create_all()

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