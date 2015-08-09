# -*- coding: utf-8 -*-
from flask import render_template, redirect,\
	url_for, flash
from flask.ext.babel import gettext
from app import app, db, babel
from app.models.dbs import Config
from app.models.forms import ConfigForm
from app.models.global_functions import requires_roles

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html',
							title=gettext('Home'))

@app.route('/config', methods=['GET', 'POST'])
@requires_roles('admin')
def config():
	if Config.query.count() == 0:
		entry = Config()
		db.session.add(entry)
		db.session.commit()
	config = Config.query.get(1)
	form = ConfigForm(obj=config)
	if form.validate_on_submit():
		Config.query.filter_by(id=1).update(
			form.data
			)
		db.session.commit()
		app.config.update(dict(
			MAIL_SERVER = form.data.mail_server,
			MAIL_PORT = form.data.mail_port,
			MAIL_USERNAME = form.data.mail_username,
			MAIL_PASSWORD = form.data.mail_password,
			DEFAULT_MAIL_SENDER = form.data.mail_sender,
			MAIL_USE_TLS = False,
			MAIL_USE_SSL= True
			))
		flash(gettext("Updated!"), "success")
		return redirect(url_for('config'))
	return render_template('config.html',
							title=gettext('Config'),
							form=form)
