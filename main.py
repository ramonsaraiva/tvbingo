import json
import requests

from flask import Flask
from flask import send_from_directory

from flask.ext.restful import Api

from models import db
from models import Game

from resources import Matches
from resources import Cards

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
	'SQLALCHEMY_DATABASE_URI': 'postgresql://tvbingo:tvbingo@localhost/tvbingo'
})

db.init_app(app)
api = Api(app)

api.add_resource(Matches, '/matches/', '/matches/<int:id>/')
api.add_resource(Cards, '/matches/cards/')

@app.route('/')
def send_template():
	return send_from_directory('templates', 'base.html')

@app.route('/<path:path>')
def send_static(path):
	return send_from_directory('static', path)

@app.cli.command()
def drop():
	db.drop_all()

@app.cli.command()
def create():
	db.create_all()

@app.cli.command()
def generate():
	players = int(raw_input('Players: '))
	amount = int(raw_input('Amount of games: '))

	headers = {
		'X-Mashape-Key': 'C4UDpRLdVnmshrlrYUufHIF1VDgBp1yrTvejsnoNyCbSYgzbuc',
		'Accept': 'application/json',
		'Content-Type': 'application/json'
	}

	for i in range(amount):
		r = requests.get('https://bingo.p.mashape.com/index.php?cards_number={0}'.format(players), headers=headers)
		data = json.loads(r.text)

		game = Game()
		game.create(players, data)
		db.session.add(game)
		db.session.commit()

		print('Generated game {0} for {1} players..'.format(game, game.players))
