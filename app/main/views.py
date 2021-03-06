"""
Main application view functions
"""
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
import random
import string

from app import db
from app.main import bp
from app.models import Game

import logging
logger = logging.getLogger(__name__)

def new_game():
	code = ''.join([random.choice(string.ascii_lowercase) for i in range(6)])
	new_game = Game(code=code)
	new_game.fill_bag()
	try:
		db.session.add(new_game)
		db.session.commit()
	except:
		db.session.rollback()
	finally:
		db.session.close()
	return Game.query.filter_by(code=code).first()

def draw_tiles(number, game):
	if number > len(game.bag):
		return None
	tiles = [game.draw_tile() for n in range(number)]
	try:
		db.session.add(game)
		db.session.commit()
		return tiles
	except:
		db.session.rollback()
		return None

@bp.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		if request.form['action'] == 'start':
			new = new_game()
			flash("Started new game! There are {} tiles. Your code is: {}".format(len(new.bag), new.code), "success")
			return redirect(url_for('main.game', code=new.code))
		elif request.form['action'] == 'join':
			join_game = Game.query.filter_by(code=request.form['code']).first()
			if not join_game:
				flash("Game not found", "danger")
				return redirect(url_for('main.index'))
			flash("Welcome to the game!  There are {} tiles left".format(len(join_game.bag)), "success")
			return redirect(url_for('main.game', code=request.form['code']))
	return render_template('index.html')

@bp.route("/game/<code>", methods=["GET", "POST"])
def game(code):
	current_game = Game.query.filter_by(code=code).first()
	if not current_game:
		flash("Game not found", "danger")
		return redirect(url_for('main.index'))
	if request.method == "POST":
		tiles = draw_tiles(int(request.form['tiles']), game=current_game)
		if tiles == None:
			flash("Oops, there was a problem... try again", "danger")
		else:
			flash("Your tiles: {} ({} tiles left)".format(tiles,
				len(current_game.bag)), "success")
		return render_template('game.html')
	else:
		return render_template('game.html', bag=len(current_game.bag))
