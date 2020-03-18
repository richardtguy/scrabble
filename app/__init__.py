import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

import logging
logging.basicConfig(level=logging.DEBUG, filename='log')

# extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message_category = 'danger'
mail = Mail()

# application factory
def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_pyfile('config.py')

	# log to stdout if deployed to Heroku
	if app.config['LOG_TO_STDOUT']:
		logging.getLogger().addHandler(logging.StreamHandler())

	# initialise extensions
	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)
	mail.init_app(app)

	# register blueprints
	from app.auth import bp as auth_bp
	app.register_blueprint(auth_bp, url_prefix='/auth')
	from app.main import bp as main_bp
	app.register_blueprint(main_bp)

	# add cli commands
	from app.auth.commands import create_user, delete_user
	app.cli.add_command(create_user)
	app.cli.add_command(delete_user)

	# add cli commands
	from app.main.commands import flush
	app.cli.add_command(flush)

	return app
