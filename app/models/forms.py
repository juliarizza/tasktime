# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField,\
	IntegerField, FloatField, FileField,\
	SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email,\
	Optional

class LoginForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me')

class ChangePassword(Form):
	old_password = PasswordField('old_password', validators=[DataRequired()])
	new_password = PasswordField('new_password', validators=[DataRequired()])
	new_password_2 = PasswordField('new_password_2', validators=[DataRequired()])

class RegisterClient(Form):
	## user info
	name = StringField('name', validators=[DataRequired()])
	email = StringField('email', validators=[Email()])
	## company info
	company_name = StringField('company_name')
	trade_name = StringField('trade_name')
	company_federal_id = StringField('company_federal_id')
	company_state_id = StringField('company_state_id')
	## contact info
	address = StringField('address')
	number = IntegerField('number', validators=[Optional()])
	complement = StringField('complement')
	zip_code = StringField('zip_code')
	city = StringField('city', validators=[DataRequired()])
	state = StringField('state', validators=[DataRequired()])
	country = StringField('country', validators=[DataRequired()])
	phone = StringField('phone')
	celphone = StringField('celphone')

class RegisterUser(Form):
	## user info
	name = StringField('name', validators=[DataRequired()])
	email = StringField('email', validators=[Email()])
	role = StringField('role', validators=[DataRequired()])
	## company info
	company_name = StringField('company_name')
	trade_name = StringField('trade_name')
	company_federal_id = StringField('company_federal_id')
	company_state_id = StringField('company_state_id')
	## contact info
	address = StringField('address')
	number = IntegerField('number', validators=[Optional()])
	complement = StringField('complement')
	zip_code = StringField('zip_code')
	city = StringField('city', validators=[DataRequired()])
	state = StringField('state', validators=[DataRequired()])
	country = StringField('country', validators=[DataRequired()])
	phone = StringField('phone')
	celphone = StringField('celphone')

class NewContract(Form):
	title = StringField('title', validators=[DataRequired()])
	price_hour = FloatField('price_hour', validators=[DataRequired()])
	total_hours = IntegerField('total_hours', validators=[DataRequired()])
	period = IntegerField('period', validators=[DataRequired()])
	attachment = FileField('attachment', validators=[Optional()])

class NewTicket(Form):
	title = StringField('title', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	priority = SelectField('priority', 
							choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')],
							default='normal',
							validators=[DataRequired()])
	client = SelectField('client', 
						validators=[DataRequired()],
						coerce=int)
	employee = SelectField('employee', 
							validators=[DataRequired()],
							coerce=int)
	contract = SelectField('contract',
							validators=[DataRequired()],
							coerce=int)
class NewTicketClient(Form):
	title = StringField('title', validators=[DataRequired()])
	description = TextAreaField('description', validators=[DataRequired()])
	priority = SelectField('priority', 
							choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')],
							default='normal',
							validators=[DataRequired()])

class NewArticle(Form):
	title = StringField('title', validators=[DataRequired()])
	content = TextAreaField('content', validators=[DataRequired()])
	attachments = FileField('attachments', validators=[Optional()])
	author = SelectField('author',
						validators=[DataRequired()],
						coerce=int)