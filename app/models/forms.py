# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField,\
	IntegerField, FloatField, FileField
from wtforms.validators import DataRequired, Email,\
	Optional

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

class NewContract(Form):
	title = StringField('title', validators=[DataRequired()])
	price_hour = FloatField('price_hour', validators=[DataRequired()])
	total_hours = IntegerField('total_hours', validators=[DataRequired()])
	period = IntegerField('period', validators=[DataRequired()])
	attachment = FileField('attachment', validators=[Optional()])
