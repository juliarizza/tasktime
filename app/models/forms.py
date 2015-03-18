# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField,\
    IntegerField, FloatField, FileField,\
    SelectField, PasswordField, BooleanField,\
    RadioField
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
    price_hour = FloatField('price_hour', validators=[DataRequired()])
    total_hours = IntegerField('total_hours', validators=[DataRequired()])
    client = SelectField('client',
                        validators=[DataRequired()],
                        coerce=int)

class NewTicket(Form):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    priority = RadioField('priority', 
                            choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')],
                            default='normal',
                            validators=[DataRequired()])
    client = SelectField('client', 
                        validators=[DataRequired()],
                        coerce=int)
    employee = SelectField('employee', 
                            validators=[DataRequired()],
                            coerce=int)

class NewTicketClient(Form):
    title = StringField('title', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    priority = RadioField('priority', 
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

class ConfigForm(Form):
    company_name = StringField('company_name', validators=[DataRequired()])
    trade_name = StringField('trade_name', validators=[DataRequired()])
    company_federal_id = StringField('company_federal_id')
    company_state_id = StringField('company_state_id')
    address = StringField('address')
    number = IntegerField('number', validators=[Optional()])
    complement = StringField('complement')
    zip_code = StringField('zip_code')
    city = StringField('city')
    state = StringField('state')
    country = StringField('country')
    phone = StringField('phone')
    celphone = StringField('celphone')
    mail_server = StringField('mail_server')
    mail_port = StringField('mail_port', validators=[Optional()])
    mail_username = StringField('mail_username')
    mail_password = StringField('mail_password')
    mail_sender = StringField('mail_sender')