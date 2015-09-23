import json
import random

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	players = db.Column(db.Integer)
	_cards = db.Column(db.String())
	_numbers = db.Column(db.String())
	_winners = db.Column(db.String())
	matches = db.relationship('Match', backref='game', lazy='dynamic', cascade='all, delete-orphan', order_by='Match.id')

	def __repr__(self):
		return '<Game: {0}>'.format(self.id)

	@property
	def cards(self):
		return json.loads(self._cards)

	@property
	def numbers(self):
		return json.loads(self._numbers)

	@property
	def winners(self):
		return json.loads(self._winners)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'players': self.players,
			'numbers': self.numbers,
			'winners': self.winners
		}

	def create(self, players, data):
		self.players = players
		self._cards = json.dumps(data['cards'])
		self._numbers = json.dumps(data['numbers_drawn'])
		self._winners = json.dumps(data['winners'])

	def match(self):
		match = Match()
		match.game = self
		match.code = ''.join([random.choice('abcdeABCDE12345') for _ in range(4)])
		return match

# api.com/match/

class Match(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	game_id = db.Column(db.Integer, db.ForeignKey('game.id', ondelete='CASCADE'), nullable=False)
	players = db.Column(db.Integer, default=0)
	code = db.Column(db.String(4))
	done = db.Column(db.Boolean())

	def __repr__(self):
		return '<Match: {0}>'.format(self.id)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'players': self.players,
			'code': self.code,
			'game': self.game.serialize
		}

	def take_card(self):
		if self.players + 1 <= self.game.players:
			card = self.game.cards[str(self.players+1)]
			self.players = self.players + 1
			return card
		return None
