from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from config import config
from models import db, BoardArticle, Board

import json

parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("title")
parser.add_argument("content")
parser.add_argument("board_id")

class Article(Resource):
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            current_article = BoardArticle.query.filter_by(id=board_article_id).first().to_dict()
            response = {
                "status":"success",
                "result": current_article,
                "message": "printed a selected article"
            }
            return jsonify(response)
        else:
            article_list = BoardArticle.query.filter_by(board_id = board_id)
            article_list = [a.to_dict() for a in article_list]
            response={
                "status": "success",
                "result": article_list,
                "message": "printed list of articles"
            }
            return jsonify(response)
    def post(self, board_id=None):
        args = parser.parse_args()
        author = session.get("user")
        if author :
            new_article = BoardArticle(args["title"], args["content"], board_id,author)
            db.session.add(new_article)
            db.session.commit()
            response = {
                "status":"success",
                "result": {"title": args["title"]},
                "message": "successfully posted a new article"
            }
            return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to post an article"
            }
            return jsonify(response)
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        author = session.get("user")
        if author:
            current_article = BoardArticle.query.filter_by(id=board_article_id).first()
            if current_article.user_id == author:
                current_article.title = args["title"]
                current_article.content = args["content"]
                db.session.commit()
                response = {
                    "status":"success",
                    "result": {"title": args["title"], "content": args["content"]},
                    "message": "successfully updated an article"
                }
                return jsonify(response)
            else:
                response={
                    "status": "error",
                    "message": "the user is not allowed to update current article"
                }
                return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to update an article "
            }
            return jsonify(response)
    def delete(self, board_id=None, board_article_id=None):
        author = session.get("user")
        if author:
            current_article = BoardArticle.query.filter_by(id=board_article_id).first()
            if current_article.user_id == author:
                BoardArticle.query.filter_by(id=board_article_id).delete()
                db.session.commit()
                response ={
                    "status": "success",
                    "result": {
                        "id":board_article_id,
                    },
                    "message": "successfully deleted"
                }
                return jsonify(response)
            else:
                response={
                    "status": "error",
                    "message": "the user is not allowed to delete current article"
                }
                return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to delete an article"
            }
            return jsonify(response)

parser = reqparse.RequestParser()
parser.add_argument("n")

class DashBoard(Resource):
    def get(self):
        result = []
        args = parser.parse_args()
        num = args["n"]
        all_board = Board.query.all()
        for b in all_board:
            board_id = b.id
            articles = BoardArticle.query.filter_by(board_id = board_id).order_by(BoardArticle.create_date.desc()).limit(num)
            # .order_by(BoardArticle.create_date.desc()).limit(num)
            result.extend([a.to_dict() for a in articles])
            # print("id", board_id,"article", len([a.to_dict() for a in articles]))
            response={
                "status":"success",
                "result":result
            }
        return jsonify(response)
