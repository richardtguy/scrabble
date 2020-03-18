"""
Database model definitions
"""
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import jwt
import logging
import random
from app import db, login

logger = logging.getLogger(__name__)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
	"""
	Database model for user accounts
	"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_reset_password_token(self, expires_in=600):
		return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
											current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

	@staticmethod
	def verify_reset_password_token(token):
		try:
			id = jwt.decode(token, current_app.config['SECRET_KEY'],
											algorithms=['HS256'])['reset_password']
		except:
			return
		return User.query.get(id)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Game(db.Model):
    """
    Database model for game
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(6), index=True, unique=True)
    bag = db.Column(db.String(128))

    def fill_bag(self):
        english_tiles = [
            ('?', 2),
            ('E', 12),
            ('A', 9),
            ('I', 9),
            ('O', 8),
            ('N', 6),
            ('R', 6),
            ('T', 6),
            ('L', 4),
            ('S', 4),
            ('U', 4),
            ('D', 4),
            ('G', 3),
            ('B', 2),
            ('C', 2),
            ('M', 2),
            ('P', 2),
            ('F', 2),
            ('H', 2),
            ('V', 2),
            ('W', 2),
            ('Y', 2),
            ('K', 1),
            ('J', 1),
            ('X', 1),
            ('Q', 1),
            ('Z', 1)
        ]
        self.bag = ""
        for letter in english_tiles:
            for n in range(letter[1]):
                self.bag += letter[0]

    def draw_tile(self):
        tile = random.choice(self.bag)
        self.bag = self.bag.replace(tile, '', 1)
        return tile

    def __repr__(self):
        return '<Game {}>'.format(self.code)
