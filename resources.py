from flask import jsonify

from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from sqlalchemy.sql.expression import func, select

from werkzeug.exceptions import abort

from models import db
from models import Game
from models import Match

class Matches(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('players', type=int, location='json', required=True)

	def get(self, id):
		match = Match.query.get_or_404(id)
		db.session.commit()
		return jsonify(match.serialize)

	def post(self):
		args = self.reqparse.parse_args()
		game = Game.query.filter(Game.players == args['players']).order_by(func.random()).first()

		if not game:
			abort(404)

		match = game.match()
		db.session.commit()
		return jsonify(match.serialize)

class Cards(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('code', type=str, location='json', required=True)

	def post(self):
		args = self.reqparse.parse_args()

		match = None
		try:
			match = Match.query.filter(Match.code == args['code']).one()
		except:
			abort(404)

		card = match.take_card()
		if not card:
			abort(404)

		db.session.commit()
		return jsonify(card)
