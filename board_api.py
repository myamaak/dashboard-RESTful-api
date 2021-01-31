from flask import Flask, jsonify, request, session
from flask_restful import reqparse, abort, Api, Resource

from config import config
from models import db, Board

import json

parser = reqparse.RequestParser()
parser.add_argument("id")
parser.add_argument("name")
# parser.add_argument("user_id")

class board(Resource):
    def get(self):
        boardlist = Board.query.all()
        #https://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
        #결과를 jsonify 할 수 있게 만들어야됨
        result = [b.to_dict() for b in boardlist]
        response = {
            "status": "success",
            "result": result,
            "message": "printing board list"
        }
        return jsonify(response)
    
    def post(self):
        args = parser.parse_args()
        boardname = args["name"]
        manager = session.get("user")
        if manager:
            new_board = Board(boardname, manager)
            db.session.add(new_board)
            db.session.commit()
            response ={
                "status": "success",
                "result": {"boardname": boardname},
                "message": "new board is added"
            }
            return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to create a board"
            }
            return jsonify(response)
    
    def put(self):
        args = parser.parse_args()
        board_id = args["id"]
        boardname = args["name"]
        manager = session.get("user")
        if manager:
            current_board = Board.query.filter_by(id = board_id).first()
            if current_board.user_id == manager:
                current_board.boardname = boardname
                db.session.commit()
                response ={
                    "status": "success",
                    "result": {
                        "id":board_id,
                        "name": boardname
                    },
                    "message": "successfully changed board name"
                }
                return jsonify(response)
            else:
                response={
                    "status": "error",
                    "message": "the user is not allowed to update current board"
                }
                return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to change board name"
            }
            return jsonify(response)

    def delete(self):
        args = parser.parse_args()
        board_id = args["id"]
        manager = session.get("user")
        if manager:
            current_board = Board.query.filter_by(id = board_id).first()
            if current_board.user_id == manager:
                Board.query.filter_by(id=board_id).delete()
                db.session.commit()
                response ={
                    "status": "success",
                    "result": {
                        "id":board_id,
                    },
                    "message": "successfully deleted"
                }
                return jsonify(response)
            else:
                response={
                    "status": "error",
                    "message": "the user is not allowed to delete current board"
                }
                return jsonify(response)
        else:
            response ={
                "status": "error",
                "message": "you have to login first to delete board"
            }
            return jsonify(response)
