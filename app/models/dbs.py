# -*- coding: utf-8 -*-
from app import db
from werkzeug.security import generate_password_hash

import datetime

def set_password(password):
	return generate_password_hash(password)

class User(db.Document):
	name = db.StringField()
	mail = db.StringField()
	category = db.EnumField(db.StringField(), \
		'master', 'employee', \
		default='employee')

	@db.computed_field(db.StringField())
	def password(pw):
		return set_password(pw)

class Client(db.Document):
	name = db.StringField()
	company = db.StringField(required=False)
	mail = db.StringField()
	address = db.StringField()
	city = db.StringField()
	state = db.StringField()
	phone = db.StringField()

	@db.computed_field(db.StringField())
	def password(pw):
		return set_password(pw)

class Project(db.Document):
	name = db.StringField()
	description = db.StringField(required=False)
	clients = db.DocumentField(Client)

class Article(db.Document):
	name = db.StringField()
	content = db.StringField()
	attachments = db.StringField(required=False)
	author = db.DocumentField(User)

class Contract(db.Document):
	title = db.StringField()
	price_hour = db.FloatField()
	total_hours = db.IntField(default=1)
	period = db.IntField(default=1) #in months
	attachment = db.StringField(required=False)

class Ticket(db.Document):
	title = db.StringField()
	description = db.StringField()
	priority = db.EnumField(db.StringField(), \
		'high', 'normal', 'low', \
		default='normal')
	status = db.EnumField(db.StringField(), \
		'open', 'closed', 'on hold', \
		default='open')
	end_time = db.DateTimeField()
	project = db.DocumentField(Project, required=False)
	client = db.DocumentField(Client, required=False)
	employee = db.DocumentField(User)
	contract = db.DocumentField(Contract)

	@db.computed_field(db.DateTimeField(), one_time=True)
	def start_time(obj):
		return datetime.datetime.now()

