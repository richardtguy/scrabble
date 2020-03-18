"""
Command line functions for back-end administration of users
"""
import click
from flask.cli import with_appcontext

import logging
logger = logging.getLogger(__name__)

from app.models import Game
from app import db

@click.command('flush')
@with_appcontext
def flush():
	"""
	FLush all games from database
	"""
	games = Game.query.all()
	try:
		for game in games:
			db.session.delete(game)
		db.session.commit()
		click.echo("Flushed all games from database")
	except:
		db.session.rollback()
		click.echo("Error! Could not flush database")
	finally:
		db.session.close()
