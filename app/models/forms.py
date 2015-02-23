# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField,\
	IntegerField
from wtforms.validators import DataRequired, Email

class RegisterClient(Form):
	name = StringField('name', validators=[DataRequired()])
	company = StringField('company')
	email = StringField('email', validators=[Email()])
	address = TextAreaField('address')
	city = StringField('city', validators=[DataRequired()])
	state = StringField('state', validators=[DataRequired()])
	phone = IntegerField('phone')