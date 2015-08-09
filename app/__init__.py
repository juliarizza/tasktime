    # -*- coding: utf-8 -*-

from flask import Flask, request
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.mail import Mail
from flask.ext.babel import Babel

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

babel = Babel(app)
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

from app.models import dbs, forms
try:
	config_info = dbs.Config.query.get(1)
	app.config.update(dict(
		MAIL_SERVER = config_info.mail_server,
		MAIL_PORT = config_info.mail_port,
		MAIL_USERNAME = config_info.mail_username,
		MAIL_PASSWORD = config_info.mail_password,
		DEFAULT_MAIL_SENDER = config_info.mail_sender,
		MAIL_USE_TLS = False,
		MAIL_USE_SSL= True
		))
except:
	config_info = None

mail = Mail(app)

from app.routes import index, clients, contracts,\
	tickets, users, library

from app.models import tasks

admin = Admin(app)
admin.add_view(ModelView(dbs.User, db.session))
admin.add_view(ModelView(dbs.Article, db.session))
admin.add_view(ModelView(dbs.Contract, db.session))
admin.add_view(ModelView(dbs.Ticket, db.session))
