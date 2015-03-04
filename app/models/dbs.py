# -*- coding: utf-8 -*-
from app import db
from werkzeug.security import check_password_hash,\
    generate_password_hash

import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    ## user info
    name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    category = db.Column(db.Enum('admin', 'employee', 'client'),\
        default='client')
    role = db.Column(db.String)
    ## company info
    company_name = db.Column(db.String) ## PT-BR: Razão Social
    trade_name = db.Column(db.String) ## PT-BR: Nome Fantasia
    company_federal_id = db.Column(db.String) ## PT-BR: CNPJ
    company_state_id = db.Column(db.String) ## PT-BR: Inscrição Estadual
    ## contact info
    address = db.Column(db.String)
    number = db.Column(db.Integer)
    complement = db.Column(db.String(20))
    zip_code = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    phone = db.Column(db.String)
    celphone = db.Column(db.String)
    ## relationships
    tickets_clients = db.relationship('Ticket', backref='clients', lazy='dynamic', foreign_keys='Ticket.client')
    tickets_employees = db.relationship('Ticket', backref='employees', lazy='dynamic', foreign_keys='Ticket.employee')
    articles = db.relationship('Article', backref='authors', lazy='dynamic')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def get_category(self):
        return self.category

    def __repr__(self):
        return '<User %r>' % self.name


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    attachments = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey(User.id))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Article %r>' % self.title

class Contract(db.Model):
    __tablename__ = 'contracts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    price_hour = db.Column(db.Float)
    total_hours = db.Column(db.Integer, default=1)
    period = db.Column(db.Integer, default=1) #in months
    attachment = db.Column(db.String)
    tickets = db.relationship('Ticket', backref='contracts', lazy='dynamic')

    def __repr__(self):
        return '<Contract %r>' % self.title

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    priority = db.Column(db.Enum('high', 'normal', \
        'low'), default='normal')
    status = db.Column(db.Enum('open', 'closed', \
        'on hold'), default='open')
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    client = db.Column(db.Integer, db.ForeignKey(User.id))
    employee = db.Column(db.Integer, db.ForeignKey(User.id))
    contract = db.Column(db.Integer, db.ForeignKey(Contract.id))

    def __repr__(self):
        return '<Ticket %r>' % self.title
    

