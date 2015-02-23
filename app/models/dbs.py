# -*- coding: utf-8 -*-
from app import db
from werkzeug.security import generate_password_hash

import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	mail = db.Column(db.String)
	passowrd = db.Column(db.String)
	category = db.Column(db.Enum('master', 'employee'),\
		default='employee')

	def __repr__(self):
		return '<User %r>' % self.name

class Client(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	company = db.Column(db.String)
	email = db.Column(db.String)
	password = db.Column(db.String)
	address = db.Column(db.Text)
	city = db.Column(db.String)
	state = db.Column(db.String)
	phone = db.Column(db.String)

	def __repr__(self):
		return '<Client %r - %r>' % (self.name, self.company)

class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	description = db.Column(db.Text)
	clients = db.Column(db.Integer, db.ForeignKey('client.id'))

	def __repr__(self):
		return '<Project %r>' % self.name

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	content = db.Column(db.String)
	attachments = db.Column(db.String)
	author = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Article %r>' % self.name

class Contract(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	price_hour = db.Column(db.Float)
	total_hours = db.Column(db.Integer, default=1)
	period = db.Column(db.Integer, default=1) #in months
	attachment = db.Column(db.String)

	def __repr__(self):
		return '<Contract %r>' % self.title

class Ticket(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String)
	description = db.Column(db.String)
	priority = db.Column(db.Enum('high', 'normal', \
		'low'), default='normal')
	status = db.Column(db.Enum('open', 'closed', \
		'on hold'), default='open')
	end_time = db.Column(db.DateTime, default=datetime.datetime.now)
	project = db.Column(db.Integer, db.ForeignKey('project.id'))
	client = db.Column(db.Integer, db.ForeignKey('client.id'))
	employee = db.Column(db.Integer, db.ForeignKey('user.id'))
	contract = db.Column(db.Integer, db.ForeignKey('contract.id'))

	def __repr__(self):
		return '<Ticket %r>' % self.title

